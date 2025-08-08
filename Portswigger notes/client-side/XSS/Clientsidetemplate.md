# Client-side template injection

# XSS without HTML: Client-Side Template Injection with AngularJS
- INTRODUCTION
- AngularJS is an MVC client side framework written by Google. 
- With Angular, the HTML pages you see via view-source or Burp containing 'ng-app' are actually templates, and will be rendered by Angular. 
- This means that if user input is directly embedded into a page, the application may be vulnerable to client-side template injection. 
- This is true even if the user input is HTML-encoded and inside an attribute.
- Angular templates can contain expressions - JavaScript-like code snippets inside double curly braces. To see how they work have a look at the following jsfiddle:http://jsfiddle.net/2zs2yv7o/
- The text input {{1+1}} is evaluated by Angular, which then displays the output: 2.
- This means anyone able to inject double curly braces can execute Angular expressions. 
- Angular expressions can't do much harm on their own, but when combined with a sandbox escape we can execute arbitrary JavaScript and do some serious damage.
- The following two snippets show the essence of the vulnerability. 
- The first page dynamically embeds user input, but is not vulnerable to XSS because it uses htmlspecialchars to HTML encode the input:
```
<html>
<body>
<p>
<?php
$q = $_GET['q'];
echo htmlspecialchars($q,ENT_QUOTES);
?>
</p>
</body>
</html>
```
- The second page is almost identical, but the Angular import means it can be exploited by injecting an Angular expression, and with a sandbox escape we can get XSS.
```
<html ng-app>
<head>
<script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.4.7/angular.js"></script>
</head>
<body>
<p>
<?php
$q = $_GET['q'];
echo htmlspecialchars($q,ENT_QUOTES);?>
</p>   
</body>
</html>
```
- Note that you need to have "ng-app" above the expression in the DOM tree. 
- Usually an Angular site will use it in the root HTML or body tag.
- In other words, if a page is an Angular template, we're going to have a much easier time XSSing it. 
- There's only one catch - the sandbox. Fortunately, there is a solution.

# The Sandbox
- Angular expressions are sandboxed 'to maintain a proper separation of application responsibilities'.
- In order to exploit users, we need to break out of the sandbox and execute arbitrary JavaScript.
- Let's reuse the fiddle from earlier and place a breakpoint at line 13275 inside angular.js in the sources tab in Chrome. 
- In the watches window, add a new watch expression of "fnString". 
- This will display our transformed output. 1+1 gets transformed to:
```
"use strict";
var fn = function(s, l, a, i) {
    return plus(1, 1);
};
return fn;
```
- So the expression is getting parsed and rewritten then executed by Angular. 
- Let's try to get the Function constructor: http://jsfiddle.net/2zs2yv7o/1/
- This is where things get a little more interesting, here is the rewritten output:

```"use strict";
var fn = function(s, l, a, i) {
    var v0, v1, v2, v3, v4 = l && ('constructor' in l),
        v5;
    if (!(v4)) {
        if (s) {
            v3 = s.constructor;
        }
    } else {
        v3 = l.constructor;
    }
    ensureSafeObject(v3, text);
    if (v3 != null) {
        v2 = ensureSafeObject(v3.constructor, text);
    } else {
        v2 = undefined;
    }
    if (v2 != null) {
        ensureSafeFunction(v2, text);
        v5 = 'alert\u00281\u0029';
        ensureSafeObject(v3, text);
        v1 = ensureSafeObject(v3.constructor(ensureSafeObject('alert\u00281\u0029', text)), text);
    } else {
        v1 = undefined;
    }
    if (v1 != null) {
        ensureSafeFunction(v1, text);
        v0 = ensureSafeObject(v1(), text);
    } else {
        v0 = undefined;
    }
    return v0;
};
return fn;
```
- As you can see, Angular goes through each object in turn and checks it using the ensureSafeObject function. 
- The ensureSafeObject function checks if the object is the Function constructor, the window object, a DOM element or the Object constructor. 
- If any of the checks are true it will raise an exception and stop executing the expression. 
- It also prevents access to global variables by making all references for globals look at a object property instead.
- Angular also has a couple of other functions that do security checks such as ensureSafeMemberName and ensureSafeFunction. 
- ensureSafeMemberName checks a JavaScript property and makes sure it doesn't match ```__proto__``` etc and ensureSafeFunction checks function calls do not call the Function constructor or call, apply and bind.
- I did not understand any of the above, so i'm skipping 

# What is client-side template injection?
- Client-side template injection vulnerabilities arise when applications using a client-side template framework dynamically embed user input in web pages. 
- When rendering a page, the framework scans it for template expressions and executes any that it encounters. 
- An attacker can exploit this by supplying a malicious template expression that launches a cross-site scripting (XSS) attack.

# What is the AngularJS sandbox?
- The AngularJS sandbox is a mechanism that prevents access to potentially dangerous objects, such as window or document, in AngularJS template expressions. 
- It also prevents access to potentially dangerous properties, such as ```__proto__```. 
- Despite not being considered a security boundary by the AngularJS team, the wider developer community generally thinks otherwise. 
- Although bypassing the sandbox was initially challenging, security researchers have discovered numerous ways of doing so. 
- As a result, it was eventually removed from AngularJS in version 1.6. However, many legacy applications still use older versions of AngularJS and may be vulnerable as a result.

# How does the AngularJS sandbox work?
- The sandbox works by parsing an expression, rewriting the JavaScript, and then using various functions to test whether the rewritten code contains any dangerous objects. 
- For example, the ensureSafeObject() function checks whether a given object references itself. 
- This is one way to detect the window object, for example. 
- The Function constructor is detected in roughly the same way, by checking whether the constructor property references itself.
- The ensureSafeMemberName() function checks each property access of the object and, if it contains dangerous properties such as __proto__ or __lookupGetter__, the object will be blocked. 
- The ensureSafeFunction()function prevents call(), apply(), bind(), or constructor() from being called.
- You can see the sandbox in action for yourself by visiting this fiddle and setting a breakpoint at line 13275 of the angular.js file. 
- The variable fnString contains your rewritten code, so you can look at how AngularJS transforms it.

# How does an AngularJS sandbox escape work?
- A sandbox escape involves tricking the sandbox into thinking the malicious expression is benign. 
- The most well-known escape uses the modified charAt() function globally within an expression:
```
'a'.constructor.prototype.charAt=[].join
```
- When it was initially discovered, AngularJS did not prevent this modification. 
-The attack works by overwriting the function using the [].join method, which causes the charAt() function to return all the characters sent to it, rather than a specific single character. 
- Due to the logic of the isIdent() function in AngularJS, it compares what it thinks is a single character against multiple characters. 
- As single characters are always less than multiple characters, the isIdent() function always returns true, as demonstrated by the following example:
```
isIdent = function(ch) {
    return ('a' <= ch && ch <= 'z' || 'A' <= ch && ch <= 'Z' || '_' === ch || ch === '$');
}

isIdent('x9=9a9l9e9r9t9(919)')
```
- Once the isIdent() function is fooled, you can inject malicious JavaScript. 
- For example, an expression such as $eval('x=alert(1)') would be allowed because AngularJS treats every character as an identifier. 
- Note that we need to use AngularJS's $eval() function because overwriting the charAt() function will only take effect once the sandboxed code is executed. 
- This technique would then bypass the sandbox and allow arbitrary JavaScript execution. 
- PortSwigger Research broke the AngularJS sandbox comprehensively, multiple times.

# Constructing an advanced AngularJS sandbox escape
So you've learned how a basic sandbox escape works, but you may encounter sites that are more restrictive with which characters they allow. 
- For example, a site may prevent you from using double or single quotes. In this situation, you need to use functions such as String.fromCharCode() to generate your characters. 
- Although AngularJS prevents access to the String constructor within an expression, you can get round this by using the constructor property of a string instead. 
- This obviously requires a string, so to construct an attack like this, you would need to find a way of creating a string without using single or double quotes.
- In a standard sandbox escape, you would use $eval() to execute your JavaScript payload, but in the lab below, the $eval() function is undefined. 
- Fortunately, we can use the orderBy filter instead. The typical syntax of an orderBy filter is as follows:
```
[123]|orderBy:'Some string'
```
- Note that the | operator has a different meaning than in JavaScript. 
- Normally, this is a bitwise OR operation, but in AngularJS it indicates a filter operation. 
- In the code above, we are sending the array ```[123]``` on the left to the orderBy filter on the right. 
- The colon signifies an argument to send to the filter, which in this case is a string. 
- The orderBy filter is normally used to sort an object, but it also accepts an expression, which means we can use it to pass a payload.
- You should now have all the tools you need to tackle the next lab.