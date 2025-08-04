# What is DOM-based denial of service?
- DOM-based denial-of-service vulnerabilities arise when a script passes attacker-controllable data in an unsafe way to a problematic platform API, such as an API whose invocation can cause the user's computer to consume excessive amounts of CPU or disk space. 
- This may result in side effects if the browser restricts the functionality of the website, for example, by rejecting attempts to store data in localStorage or killing busy scripts.

# Which sinks can lead to DOM-based denial-of-service vulnerabilities?
- The following are some of the main sinks can lead to DOM-based denial-of-service vulnerabilities:
- requestFileSystem()
- RegExp()