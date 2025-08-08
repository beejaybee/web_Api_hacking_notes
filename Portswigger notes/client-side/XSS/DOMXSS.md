# What is DOM-based cross-site scripting?
- DOM-based XSS vulnerabilities usually arise when JavaScript takes data from an attacker-controllable source, such as the URL, and passes it to a sink that supports dynamic code execution, such as eval() or innerHTML. 
- This enables attackers to execute malicious JavaScript, which typically allows them to hijack other users' accounts.
- To deliver a DOM-based XSS attack, you need to place data into a source so that it is propagated to a sink and causes execution of arbitrary JavaScript.
- The most common source for DOM XSS is the URL, which is typically accessed with the window.location object. 
- An attacker can construct a link to send a victim to a vulnerable page with a payload in the query string and fragment portions of the URL. 
- In certain circumstances, such as when targeting a 404 page or a website running PHP, the payload can also be placed in the path.

# How to test for DOM-based cross-site scripting
- To test for DOM-based cross-site scripting manually, you generally need to use a browser with developer tools, such as Chrome. 
- You need to work through each available source in turn, and test each one individually.

# Testing HTML sinks
- To test for DOM XSS in an HTML sink, place a random alphanumeric string into the source (such as location.search), then use developer tools to inspect the HTML and find where your string appears. 
- Note that the browser's "View source" option won't work for DOM XSS testing because it doesn't take account of changes that have been performed in the HTML by JavaScript. 
- In Chrome's developer tools, you can use Control+F (or Command+F on MacOS) to search the DOM for your string.
- For each location where your string appears within the DOM, you need to identify the context. 
- Based on this context, you need to refine your input to see how it is processed. 
- For example, if your string appears within a double-quoted attribute then try to inject double quotes in your string to see if you can break out of the attribute.
- Note that browsers behave differently with regards to URL-encoding, Chrome, Firefox, and Safari will URL-encode location.search and location.hash, while IE11 and Microsoft Edge (pre-Chromium) will not URL-encode these sources. 
- If your data gets URL-encoded before being processed, then an XSS attack is unlikely to work.

# Testing JavaScript execution sinks
- Testing JavaScript execution sinks for DOM-based XSS is a little harder. 
- With these sinks, your input doesn't necessarily appear anywhere within the DOM, so you can't search for it. 
- Instead you'll need to use the JavaScript debugger to determine whether and how your input is sent to a sink.
- For each potential source, such as location, you first need to find cases within the page's JavaScript code where the source is being referenced. 
- In Chrome's developer tools, you can use Control+Shift+F (or Command+Alt+F on MacOS) to search all the page's JavaScript code for the source.
- Once you've found where the source is being read, you can use the JavaScript debugger to add a break point and follow how the source's value is used. 
- You might find that the source gets assigned to other variables. 
- If this is the case, you'll need to use the search function again to track these variables and see if they're passed to a sink. 
- When you find a sink that is being assigned data that originated from the source, you can use the debugger to inspect the value by hovering over the variable to show its value before it is sent to the sink. 
- Then, as with HTML sinks, you need to refine your input to see if you can deliver a successful XSS attack.

# Testing for DOM XSS using DOM Invader
- Identifying and exploiting DOM XSS in the wild can be a tedious process, often requiring you to manually trawl through complex, minified JavaScript. 
- If you use Burp's browser, however, you can take advantage of its built-in DOM Invader extension, which does a lot of the hard work for you.

# Exploiting DOM XSS with different sources and sinks
- In principle, a website is vulnerable to DOM-based cross-site scripting if there is an executable path via which data can propagate from source to sink. 
- In practice, different sources and sinks have differing properties and behavior that can affect exploitability, and determine what techniques are necessary. 
- Additionally, the website's scripts might perform validation or other processing of data that must be accommodated when attempting to exploit a vulnerability. 
- There are a variety of sinks that are relevant to DOM-based vulnerabilities. 
- Please refer to the list below for details.
- The document.write sink works with script elements, so you can use a simple payload, such as the one below:
```
document.write('... <script>alert(document.domain)</script> ...');
```
# Which sinks can lead to DOM-XSS vulnerabilities?
## The following are some of the main sinks that can lead to DOM-XSS vulnerabilities:
- document.write()
- document.writeln()
- document.domain
- element.innerHTML
- element.outerHTML
- element.insertAdjacentHTML
- element.onevent

## The following jQuery functions are also sinks that can lead to DOM-XSS vulnerabilities:
- add()
- after()
- append()
- animate()
- insertAfter()
- insertBefore()
- before()
- html()
- prepend()
- replaceAll()
- replaceWith()
- wrap()
- wrapInner()
- wrapAll()
- has()
- constructor()
- init()
- index()
- jQuery.parseHTML()
- $.parseHTML()

# Lab: DOM XSS in document.write sink using source location.search
- This lab contains a DOM-based cross-site scripting vulnerability in the search query tracking functionality.
- It uses the JavaScript document.write function, which writes data out to the page. 
- The document.write function is called with data from location.search, which you can control using the website URL.
- Solving the lab go thus
1. Search for Alphanumeric values: 
1. Open the developer tools by inspecting the page
1. Search for the alphanumeric values in the HTML inspect page
1. Notice all places that the value is passed 
1. Notice the script function that passes the alphanumeric value and check if it uses sink and source, like document.write and source location.search
1. You can copy the code for further analysis
```
function trackSearch(query) {
    document.write('<img src="/resources/images/tracker.gif?searchTerms='+query+'">');
}
var query = (new URLSearchParams(window.location.search)).get('search');
if(query) {
    trackSearch(query);
}
```
1. Notice How the query is passed in an unsafe manner
1. Notice that the alphanumeric value will be reflected in the context of src with double quotes
1. Change the values to see if you can control the document.write function by adding double quotes to the search query : ```"><h1>XssbyBeejay</h1>```
1. Notice that You have successfuly closed the img tag and opened a new tag
1. Solve the lab by adding script tags instead of h1 element
```
"><script>alert(1)</script>
```

- Note, however, that in some situations the content that is written to document.write includes some surrounding context that you need to take account of in your exploit. 
- For example, you might need to close some existing elements before using your JavaScript payload.

# Lab: DOM XSS in document.write sink using source location.search inside a select element
- This lab contains a DOM-based cross-site scripting vulnerability in the stock checker functionality. 
- It uses the JavaScript document.write function, which writes data out to the page. 
- The document.write function is called with data from location.search which you can control using the website URL. 
- The data is enclosed within a select element.
- Solving this lab, we start by searching alphanumeric values 'Xssbybeejay'
- Now I understand what location.search means, It means the search bar
- I almost gave up on this lab, then I read the instructions again, and I notice that the location.search can be controlled by me
- This puzzled me for sometime until I thought what if I add & to the /product/productId
- No errors this time around, So I continue putting more queries, And I noticed it is being added to the DOM
- So I crafted something like this, Which first close the options tag and the close the select tag, then finally my script tag 
```
?productId=2&storeId=xssbtbee</option></select><script>alert(1)</script>
```
- Interesting Right?
- After checking the community video, I noticed that to carry out a successful DOM XSS we must understand what the javascript is doing

- One thing here is that, You can't see all these from these from the view source or the raw output from burpsuite, You have to do this from the browser, chrome or burp chromium

# Source InnerHTML
- The innerHTML sink doesn't accept script elements on any modern browser, nor will svg onload events fire. 
- This means you will need to use alternative elements like img or iframe. 
- Event handlers such as onload and onerror can be used in conjunction with these elements. For example:
```
element.innerHTML='... <img src=1 onerror=alert(document.domain)> ...'
```

# Lab: DOM XSS in innerHTML sink using source location.search
- This lab contains a DOM-based cross-site scripting vulnerability in the search blog functionality. 
- It uses an innerHTML assignment, which changes the HTML contents of a div element, using data from location.search.
- To solve this lab, perform a cross-site scripting attack that calls the alert function.
- The Sink is innerHTML, the source is location.search
- Then let's search for XssbyBeejay
- here is the function
```
<script>
    
    function doSearchQuery(query) {
        document.getElementById('searchMessage').innerHTML = query;
    }
    var query = (new URLSearchParams(window.location.search)).get('search');
    if(query) {
        doSearchQuery(query);
    }
                        
</script>
```
- Now we can just put ```<img src=x onerror=alert(1)>```
- Lab solved

# Sources and sinks in third-party dependencies
- Modern web applications are typically built using a number of third-party libraries and frameworks, which often provide additional functions and capabilities for developers. 
- It's important to remember that some of these are also potential sources and sinks for DOM XSS.

# DOM XSS in jQuery
- If a JavaScript library such as jQuery is being used, look out for sinks that can alter DOM elements on the page. 
- For instance, jQuery's attr() function can change the attributes of DOM elements. 
- If data is read from a user-controlled source like the URL, then passed to the attr() function, then it may be possible to manipulate the value sent to cause XSS. 
- For example, here we have some JavaScript that changes an anchor element's href attribute using data from the URL:

```
$(function() {
	$('#backLink').attr("href",(new URLSearchParams(window.location.search)).get('returnUrl'));
});
```
- You can exploit this by modifying the URL so that the location.search source contains a malicious JavaScript URL. 
- After the page's JavaScript applies this malicious URL to the back link's href, clicking on the back link will execute it:
```
?returnUrl=javascript:alert(document.domain)
```

# Lab: DOM XSS in jQuery anchor href attribute sink using location.search source
- This lab contains a DOM-based cross-site scripting vulnerability in the submit feedback page. 
- It uses the jQuery library's $ selector function to find an anchor element, and changes its href attribute using data from location.search.
- To solve this lab, make the "back" link alert document.cookie.
- Solving the lab requires checking the javascript script in the DOM, it uses the attribute sink and source location.search
- If you try to get to the feedback from the post you won't be able to solve the lab, but if you try to get to the feedback from the hompage you can do this:
```
https://0a7b00430339270b8020080800cc0072.web-security-academy.net/feedback?returnPath=javascript:alert(1)
```
# Another Potential Sink
- Another potential sink to look out for is jQuery's $() selector function, which can be used to inject malicious objects into the DOM.
- jQuery used to be extremely popular, and a classic DOM XSS vulnerability was caused by websites using this selector in conjunction with the location.hash source for animations or auto-scrolling to a particular element on the page. 
- This behavior was often implemented using a vulnerable hashchange event handler, similar to the following:
```
$(window).on('hashchange', function() {
	var element = $(location.hash);
	element[0].scrollIntoView();
});
```
- As the hash is user controllable, an attacker could use this to inject an XSS vector into the $() selector sink. 
- More recent versions of jQuery have patched this particular vulnerability by preventing you from injecting HTML into a selector when the input begins with a hash character (#). 
- However, you may still find vulnerable code in the wild.
- To actually exploit this classic vulnerability, you'll need to find a way to trigger a hashchange event without user interaction. 
- One of the simplest ways of doing this is to deliver your exploit via an iframe:
```
<iframe src="https://vulnerable-website.com#" onload="this.src+='<img src=1 onerror=alert(1)>'">
```
- In this example, the src attribute points to the vulnerable page with an empty hash value. 
- When the iframe is loaded, an XSS vector is appended to the hash, causing the hashchange event to fire.

# Note
- Even newer versions of jQuery can still be vulnerable via the $() selector sink, provided you have full control over its input from a source that doesn't require a # prefix.

# Lab: DOM XSS in jQuery selector sink using a hashchange event
- This lab contains a DOM-based cross-site scripting vulnerability on the home page. 
- It uses jQuery's $() selector function to auto-scroll to a given post, whose title is passed via the location.hash property.
- To solve the lab, deliver an exploit to the victim that calls the print() function in their browser.
- This lab is crazy, to solve it read the javascript code and notice the location.hash function
```
$(window).on('hashchange', function(){
    var post = $('section.blog-list h2:contains(' + decodeURIComponent(window.location.hash.slice(1)) + ')');
    if (post) post.get(0).scrollIntoView();
});
```                 
- Notice how h2 is being used
- Add #any-h2-on-the-page and see how it works
- Then if successful add ```<img src=x onerror=alert()>``` to the end 
- If it was successful solve the lab by 
```
<iframe src="https://0abe000b048c0ab480580da000be00ce.web-security-academy.net/#" onload="this.src+='Passwords%20<img%20src=1%20onerror=print()>'">

</iframe>
```
# DOM XSS in AngularJS
- If a framework like AngularJS is used, it may be possible to execute JavaScript without angle brackets or events. 
- When a site uses the ng-app attribute on an HTML element, it will be processed by AngularJS. 
- In this case, AngularJS will execute JavaScript inside double curly braces that can occur directly in HTML or inside attributes.

# Lab: DOM XSS in AngularJS expression with angle brackets and double quotes HTML-encoded
- This lab contains a DOM-based cross-site scripting vulnerability in a AngularJS expression within the search functionality.
- AngularJS is a popular JavaScript library, which scans the contents of HTML nodes containing the ng-app attribute (also known as an AngularJS directive). 
- When a directive is added to the HTML code, you can execute JavaScript expressions within double curly braces.
- This technique is useful when angle brackets are being encoded.
- To solve this lab, perform a cross-site scripting attack that executes an AngularJS expression and calls the alert function.
-Because I dont know anything about angularjs expression, I only serached for angularjs expression that can cause xss and I got this
```
1. {{constructor.constructor('alert(1)')()}}
2. {{ [].pop.constructor('alert(1)')() }}
3. {{ $on.constructor('alert(1)')()}}
4. {{ $eval.constructor('alert(1)')()}}
```
- and an alert was called, lab solved 

# DOM XSS combined with reflected and stored data
- Some pure DOM-based vulnerabilities are self-contained within a single page. 
- If a script reads some data from the URL and writes it to a dangerous sink, then the vulnerability is entirely client-side.
- However, sources aren't limited to data that is directly exposed by browsers - they can also originate from the website. 
- For example, websites often reflect URL parameters in the HTML response from the server. This is commonly associated with normal XSS, but it can also lead to reflected DOM XSS vulnerabilities.
- In a reflected DOM XSS vulnerability, the server processes data from the request, and echoes the data into the response. 
- The reflected data might be placed into a JavaScript string literal, or a data item within the DOM, such as a form field. 
- A script on the page then processes the reflected data in an unsafe way, ultimately writing it to a dangerous sink.
```
eval('var data = "reflected string"');
```

# DOM XSS combined with reflected and stored data
- Some pure DOM-based vulnerabilities are self-contained within a single page. 
- If a script reads some data from the URL and writes it to a dangerous sink, then the vulnerability is entirely client-side.
- However, sources aren't limited to data that is directly exposed by browsers - they can also originate from the website. 
- For example, websites often reflect URL parameters in the HTML response from the server. This is commonly associated with normal XSS, but it can also lead to reflected DOM XSS vulnerabilities.
- In a reflected DOM XSS vulnerability, the server processes data from the request, and echoes the data into the response. The reflected data might be placed into a JavaScript string literal, or a data item within the DOM, such as a form field. A script on the page then processes the reflected data in an unsafe way, ultimately writing it to a dangerous sink.
```
eval('var data = "reflected string"');
```

# LAB: REFLECTED DOM XSS
- This lab demonstrates a reflected DOM vulnerability. 
- Reflected DOM vulnerabilities occur when the server-side application processes data from a request and echoes the data in the response. 
- A script on the page then processes the reflected data in an unsafe way, ultimately writing it to a dangerous sink.
- To solve this lab, create an injection that calls the alert() function.
- This lab is kind of sleek, at first I was not looking into burp only into chrome dev tools and and source code
- The search term was included in another request  
- And no matter how I tried, I could not get XSS coz the filter were filtering everything out
- In burp suite, I tried different ways to close the returned json object, but none workded
- So, I noticed that " are being escaped with \, and I added my own.
- It breaked the JSON object so, I tried ```\"``` and the response returned ```\\"``` unescaping the " this time
- SO finally I crafted ```\"};%20alert(1)};//```
- The ```\"};``` closed the javascript object
- The ```%20alert(1)};``` added a new javascript function and lastly the // commented out the trailing ```"}```
- But when I searched it using the search bar, I got nothing the filter were working
- So I embeded it into the link directly and the lab was solved. 
- Looking at the javascript, It was visible that the code said location.search
- So the sink was eval and the source was location.search

# Stored DOM XSS
- Websites may also store data on the server and reflect it elsewhere. 
- In a stored DOM XSS vulnerability, the server receives data from one request, stores it, and then includes the data in a later response. 
- A script within the later response contains a sink which then processes the data in an unsafe way.
```
element.innerHTML = comment.author
```

# Lab: Stored DOM XSS
- This lab demonstrates a stored DOM vulnerability in the blog comment functionality. 
- To solve this lab, exploit this vulnerability to call the alert() function.
- On this lab I solved with this payload
```
<>%3cimg%20src='x'%20onerror='alert'%3e
```
- So this is what happens, The app is only escaping the first set of angle brackets by using  replace(strings) instead of regex. 
- That was the reason xss was able to fire because the replace(string) only escapes the first string occurrence






