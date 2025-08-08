# What is Dom-based Javascript Injection
- DOM-based JavaScript-injection vulnerabilities arise when a script executes attacker-controllable data as JavaScript. 
- An attacker may be able to use the vulnerability to construct a URL that, if visited by another user, will cause arbitrary JavaScript supplied by the attacker to execute in the context of the user's browser session.
- Users can be induced to visit the attacker's malicious URL in various ways, similar to the usual attack-delivery vectors for reflected cross-site scripting vulnerabilities

# What is the impact of a DOM-based JavaScript-injection attack?
- The attacker-supplied code can perform a wide variety of actions, such as stealing the victim's session token or login credentials, performing arbitrary actions on the victim's behalf, or even logging their keystrokes.

# Which sinks can lead to DOM-based JavaScript-injection vulnerabilities?
- eval()
- Function()
- setTimeout()
- setInterval()
- setImmediate()
- execCommand()
- execScript()
- msSetImmediate()
- range.createContextualFragment()
- crypto.generateCRMFRequest()

