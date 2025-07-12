# What is reflected cross-site scripting?
- Reflected cross-site scripting (or XSS) arises when an application receives data in an HTTP request and includes that data within the immediate response in an unsafe way.
- Suppose a website has a search function which receives the user-supplied search term in a URL parameter: https://insecure-website.com/search?term=gift
- Reflected cross-site scripting (or XSS) arises when an application receives data in an HTTP request and includes that data within the immediate response in an unsafe way.
- Suppose a website has a search function which receives the user-supplied search term in a URL parameter:
https://insecure-website.com/search?term=gift
- Reflected cross-site scripting (or XSS) arises when an application receives data in an HTTP request and includes that data within the immediate response in an unsafe way.
- Suppose a website has a search function which receives the user-supplied search term in a URL parameter:
https://insecure-website.com/search?term=gift
- Solving The lab ```<script>alert(1)</script>``` was the script use

# Impact of reflected XSS attacks
- If an attacker can control a script that is executed in the victim's browser, then they can typically fully compromise that user. Amongst other things, the attacker can:
    - Perform any action within the application that the user can perform.
    - View any information that the user is able to view.
    - Modify any information that the user is able to modify.
    - Initiate interactions with other application users, including malicious attacks, that will appear to originate from the initial victim user.
- There are various means by which an attacker might induce a victim user to make a request that they control, to deliver a reflected XSS attack. 
- These include placing links on a website controlled by the attacker, or on another website that allows content to be generated, or by sending a link in an email, tweet or other message. 
- The attack could be targeted directly against a known user, or could be an indiscriminate attack against any users of the application.
- The need for an external delivery mechanism for the attack means that the impact of reflected XSS is generally less severe than stored XSS, where a self-contained attack can be delivered within the vulnerable application itself.

- Read more on **Exploiting Cross-site-Scripting Vulnerabilities**

# Reflected XSS in different contexts
- There are many different varieties of reflected cross-site scripting. 
- The location of the reflected data within the application's response determines what type of payload is required to exploit it and might also affect the impact of the vulnerability.
- In addition, if the application performs any validation or other processing on the submitted data before it is reflected, this will generally affect what kind of XSS payload is needed.

- Read More on **Cross-site scripting context"**

# How to find and test for reflected XSS vulnerabilities
1. Test every entry point. 
- Test separately every entry point for data within the application's HTTP requests. 
- This includes parameters or other data within the URL query string and message body, and the URL file path. 
- It also includes HTTP headers, although XSS-like behavior that can only be triggered via certain HTTP headers may not be exploitable in practice.

2. Submit random alphanumeric values. 
- For each entry point, submit a unique random value and determine whether the value is reflected in the response. 
- The value should be designed to survive most input validation, so needs to be fairly short and contain only alphanumeric characters. 
- But it needs to be long enough to make accidental matches within the response highly unlikely. A random alphanumeric value of around 8 characters is normally idea.

3. Determine the reflection context. 
- For each location within the response where the random value is reflected, determine its context. 
- This might be in text between HTML tags, within a tag attribute which might be quoted, within a JavaScript string, etc.

4. Test a candidate payload. 
- Based on the context of the reflection, test an initial candidate XSS payload that will trigger JavaScript execution if it is reflected unmodified within the response. 
- The easiest way to test payloads is to send the request to Burp Repeater, modify the request to insert the candidate payload, issue the request, and then review the response to see if the payload worked. 
- An efficient way to work is to leave the original random value in the request and place the candidate XSS payload before or after it. 
- Then set the random value as the search term in Burp Repeater's response view. 
- Burp will highlight each location where the search term appears, letting you quickly locate the reflection.

5. Test alternative payloads. 
- If the candidate XSS payload was modified by the application, or blocked altogether, then you will need to test alternative payloads and techniques that might deliver a working XSS attack based on the context of the reflection and the type of input validation that is being performed. 
- For more details, see cross-site scripting contexts

6. Test the attack in a browser. 
- Finally, if you succeed in finding a payload that appears to work within Burp Repeater, transfer the attack to a real browser by pasting the URL into the address bar, or by modifying the request in Burp Proxy's intercept view, and see if the injected JavaScript is indeed executed. 
- Often, it is best to execute some simple JavaScript like alert(document.domain) which will trigger a visible popup within the browser if the attack succeeds.

# 