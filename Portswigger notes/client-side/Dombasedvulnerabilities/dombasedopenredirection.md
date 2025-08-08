# What is DOM based open redirection
- DOM-based open-redirection vulnerabilities arise when a script writes attacker-controllable data into a sink that can trigger cross-domain navigation. 
- For example, the following code is vulnerable due to the unsafe way it handles the location.hash property:
```
let url = /https?:\/\/.+/.exec(location.hash);
if (url) {
  location = url[0];
}
```
- An attacker may be able to use this vulnerability to construct a URL that, if visited by another user, will cause a redirection to an arbitrary external domain.

# What is the impact of DOM-based open redirection?
- This behavior can be leveraged to facilitate phishing attacks against users of the website, for example. 
- The ability to use an authentic application URL targeting the correct domain and with a valid TLS certificate (if TLS is used) lends credibility to the phishing attack because many users, even if they verify these features, will not notice the subsequent redirection to a different domain.
- If an attacker is able to control the start of the string that is passed to the redirection API, then it may be possible to escalate this vulnerability into a JavaScript injection attack. 
- An attacker could construct a URL with the javascript: pseudo-protocol to execute arbitrary code when the URL is processed by the browser.

# Lab: DOM-based open redirection
This lab contains a DOM-based open-redirection vulnerability. To solve this lab, exploit this vulnerability and redirect the victim to the exploit server.
- To solve this lab, First look for the source and sinl
- The source is the location.hash
- The sink is location.href
- So after many trials 
- I was able to craft this payload
```
https://0a4700eb033cccf9808b53c3006500b0.web-security-academy.net/post?postId=5&returnUrl?/url=https://exploit-0a99004803adcc35809a526001a400a7.exploit-server.net/exploit#
```
- And the lab was solved
- Take away: Always read the code very well

# Which sinks can lead to DOM-based open-redirection vulnerabilities?
The following are some of the main sinks can lead to DOM-based open-redirection vulnerabilities:
- location
- location.host
- location.hostname
- location.href
- location.pathname
- location.search
- location.protocol
- location.assign()
- location.replace()
- open()
- element.srcdoc
- XMLHttpRequest.open()
- XMLHttpRequest.send()
- jQuery.ajax()
- $.ajax()