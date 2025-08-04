# What is DOM-based JSON injection?
- DOM-based JSON-injection vulnerabilities arise when a script incorporates attacker-controllable data into a string that is parsed as a JSON data structure and then processed by the application. 
- An attacker may be able to use this behavior to construct a URL that, if visited by another user, will cause arbitrary JSON data to be processed.

# What is the impact of a DOM-based JSON-injection attack?
- Depending on the purpose for which this data is used, it may be possible for an attacker to subvert the website's logic, or cause unintended actions on behalf of another user.

# Which sinks can lead to DOM-based JSON-injection vulnerabilities?
- JSON.parse()
- jQuery.parseJSON()
- $.parseJSON()