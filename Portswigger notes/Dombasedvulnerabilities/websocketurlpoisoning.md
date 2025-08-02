# What is DOM-based WebSocket-URL poisoning?
- WebSocket-URL poisoning occurs when a script uses controllable data as the target URL of a WebSocket connection. 
- An attacker may be able to use this vulnerability to construct a URL that, if visited by another user, will cause the user's browser to open a WebSocket connection to a URL that is under the attacker's control.

# What is the impact of WebSocket-URL poisoning?
- The potential impact of WebSocket-URL poisoning depends on how the website uses WebSockets. 
- If the website transmits sensitive data from the user's browser to the WebSocket server, then the attacker may be able to capture this data.
- If the application reads data from the WebSocket server and processes it in some way, the attacker may be able to subvert the website's logic or deliver client-side attacks against the user.

# Which sinks can lead to WebSocket-URL poisoning vulnerabilities?
- The WebSocket constructor can lead to WebSocket-URL poisoning vulnerabilities.