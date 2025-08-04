# What is DOM-based HTML5-storage manipulation?
- HTML5-storage manipulation vulnerabilities arise when a script stores attacker-controllable data in the HTML5 storage of the web browser (either localStorage or sessionStorage). 
- An attacker may be able to use this behavior to construct a URL that, if visited by another user, will cause the user's browser to store attacker-controllable data.
- This behavior does not in itself constitute a security vulnerability. 
- However, if the application later reads data back from storage and processes it in an unsafe way, an attacker may be able to leverage the storage mechanism to deliver other DOM-based attacks, such as cross-site scripting and JavaScript injection.

# Which sinks can lead to DOM-based HTML5-storage manipulation vulnerabilities?
- The following are some of the main sinks that can lead to DOM-based HTML5-storage manipulation vulnerabilities:
- sessionStorage.setItem()
- localStorage.setItem()