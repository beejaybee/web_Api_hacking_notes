# What is DOM-based XPath injection?
- DOM-based XPath-injection vulnerabilities arise when a script incorporates attacker-controllable data into an XPath query. 
- An attacker may be able to use this behavior to construct a URL that, if visited by another application user, will trigger the execution of an arbitrary XPath query, which could cause different data to be retrieved and processed by the website.

# What is the impact of DOM-based XPath injection?
- Depending on the purpose for which the query results are used, it may be possible for the attacker to subvert the website's logic or cause unintended actions on behalf of the user.

# Which sinks can lead to XPath-injection vulnerabilities?
- The following are some of the main sinks that can lead to DOM-based XPath-injection vulnerabilities:
- document.evaluate()
- element.evaluate()

