# What is DOM-data manipulation?
- DOM-data manipulation vulnerabilities arise when a script writes attacker-controllable data to a field within the DOM that is used within the visible UI or client-side logic. 
- An attacker may be able to use this vulnerability to construct a URL that, if visited by another user, will modify the appearance or behavior of the client-side UI. 
- DOM-data manipulation vulnerabilities can be exploited by both reflected and stored DOM-based attacks.

# What is the impact of DOM-data manipulation?
- At the lesser end of the scale, an attacker may be able to leverage this vulnerability to perform virtual defacement of the website, such as changing text or images that are displayed on a particular page. 
- However, attacks can be more severe. 
- For example, if the attacker is able to change the src property of an element, they could potentially induce the user to perform unintended actions by importing a malicious JavaScript file.

# Which sinks can lead to DOM-data manipulation vulnerabilities?
The following are some of the main sinks that can lead to DOM-data manipulation vulnerabilities:

- script.src
- script.text
- script.textContent
- script.innerText
- element.setAttribute()
- element.search
- element.text
- element.textContent
- element.innerText
- element.outerText
- element.value
- element.name
- element.target
- element.method
- element.type
- element.backgroundImage
- element.cssText
- element.codebase
- document.title
- document.implementation.createHTMLDocument()
- history.pushState()
- history.replaceState()