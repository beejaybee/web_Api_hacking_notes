# Attacking JWT tokens

- Get the request that get the API JWT token
- Send it to burp repeater and send to sequencer
- Go to configure and Highligt the JWT token and click on ok
- Then click to start the live capture, and wait for the process to complete
- Or you can use the analyse now button to see result
- Sequencer is great at showing that some complex tokens are actually very predictable.


## JWT Attack

JSON Web Tokens (JWTs) are one of the most prevalent API token types because they operate across a wide variety of programming languages, including Python, Java, Node.js, and Ruby. These tokens are susceptible to all sorts of misconfiguration mistakes that can leave the tokens vulnerable to several additional attacks.
These attacks could provide you with sensitive information, grant you basic unauthorized access, or even administrative access to an API. 
JWTs consist of three parts, all of which are base64 encoded and separated by periods: the header, payload, and signature

## Using Jwt_tools

- jwt_tool -h
    This command will allow you to see all the various command you can run on jwt
- jwt_tool your_jwt_token
    This command allows you to see all the data inside your token
- jwt_tool -t http://target-name.com/ -rh "Authorization: Bearer JWT_Token" -M pb
    This command allows you to scan your jwt token for common vulnurabilities
- jwt_tool JWT_token -X a "None"
    This will change this to a none signature
- jwt-tool JWT_token -X b
    This will set the signature to blank
- Once the command is successful, try use the generated JWT_token to access your data
- copy the JWT_token and paste in postman or burpsuite
- If the JWT_token is valid, change your details (email) to other user details 
- And paste it to postman or burpsuite
- If successful, You have an Authentication bug

- Always jot down what worked and what doesn't work

- jwt_tool TOKEN -X k -pk public-key.pem
    If you can get the public key of the RS256 algorithm
Once you run the command, JWT_Tool will provide you with a new token to use against the API provider. If the provider is vulnerable, you’ll be able to hijack other tokens, since you now have the key required to sign tokens. Try repeating the process, this time creating a new token based on other API users (other discovered users or generic admin users).

## JWT crack Attack
