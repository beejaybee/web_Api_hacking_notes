# What is DOM-based web message manipulation?
- Web message vulnerabilities arise when a script sends attacker-controllable data as a web message to another document within the browser. 
- An attacker may be able to use the web message data as a source by constructing a web page that, if visited by a user, will cause the user's browser to send a web message containing data that is under the attacker's control. 
- For more information about the using web messages as a source, please refer to the Controlling the web-message source page.

# Which sinks can lead to DOM-based web-message manipulation vulnerabilities?
- The postMessage() method for sending web messages can lead to vulnerabilities if the event listener for receiving messages handles the incoming data in an unsafe way.
