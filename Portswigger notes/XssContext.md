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
# LAB 4: Reflected Xss with event handlers and href attribute blocked
- First lets search for the whitlisted tags
- The following tags are whitelisted, a, image, title and svg
- All I am trying has not worked, I will continue to tomorrow, Insha aa Allah


# LAB 5: Reflected XSS with some svg markup allowed
- When solving this lab, I asked chatgpt to give over 200 svg tags
- I used the tags as payload to view successful ones
- I got animateTransform
- I asked it to give me all the event handlers of animateTransform and I got onbegin
- I asked it to fire alert with onbegin, and here is the final payload
```
<svg><rect+><animateTransform+onbegin%3D"alert%28%27Animation+started%27%29"+%29"%2F><%2Frect><%2Fsvg>
```
