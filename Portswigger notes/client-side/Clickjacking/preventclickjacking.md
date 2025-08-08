# How to prevent clickjacking attacks
- We have discussed a commonly encountered browser-side prevention mechanism, namely frame busting scripts. 
- However, we have seen that it is often straightforward for an attacker to circumvent these protections. 
- Consequently, server driven protocols have been devised that constrain browser iframe usage and mitigate against clickjacking.
- Clickjacking is a browser-side behavior and its success or otherwise depends upon browser functionality and conformity to prevailing web standards and best practice. 
- Server-side protection against clickjacking is provided by defining and communicating constraints over the use of components such as iframes. 
- However, implementation of protection depends upon browser compliance and enforcement of these constraints. 
- Two mechanisms for server-side clickjacking protection are X-Frame-Options and Content Security Policy.

# X-Frame-Options
- X-Frame-Options was originally introduced as an unofficial response header in Internet Explorer 8 and it was rapidly adopted within other browsers. 
- The header provides the website owner with control over the use of iframes or objects so that inclusion of a web page within a frame can be prohibited with the deny directive:
```
X-Frame-Options: deny
```
- Alternatively, framing can be restricted to the same origin as the website using the sameorigin directive
```
X-Frame-Options: sameorigin
```
- or to a named website using the allow-from directive:
```
X-Frame-Options: allow-from https://normal-website.com
```
- X-Frame-Options is not implemented consistently across browsers (the allow-from directive is not supported in Chrome version 76 or Safari 12 for example). 
- However, when properly applied in conjunction with Content Security Policy as part of a multi-layer defense strategy it can provide effective protection against clickjacking attacks.

# Content Security Policy (CSP)
- Content Security Policy (CSP) is a detection and prevention mechanism that provides mitigation against attacks such as XSS and clickjacking. 
- CSP is usually implemented in the web server as a return header of the form:
```
Content-Security-Policy: policy
```
- where policy is a string of policy directives separated by semicolons. 
- The CSP provides the client browser with information about permitted sources of web resources that the browser can apply to the detection and interception of malicious behaviors.
- The recommended clickjacking protection is to incorporate the frame-ancestors directive in the application's Content Security Policy. 
- The ```frame-ancestors 'none'``` directive is similar in behavior to the X-Frame-Options deny directive. 
- The ```frame-ancestors 'self'``` directive is broadly equivalent to the X-Frame-Options sameorigin directive. 
- The following CSP whitelists frames to the same domain only:
```
Content-Security-Policy: frame-ancestors 'self';
```
- Alternatively, framing can be restricted to named sites:
```
Content-Security-Policy: frame-ancestors normal-website.com;
```
- To be effective against clickjacking and XSS, CSPs need careful development, implementation and testing and should be used as part of a multi-layer defense strategy.