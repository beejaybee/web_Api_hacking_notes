# Server-side parameter pollution
- Some systems contain internal APIs that aren't directly accessible from the internet. 
- Server-side parameter pollution occurs when a website embeds user input in a server-side request to an internal API without adequate encoding. 
- This means that an attacker may be able to manipulate or inject parameters, which may enable them to, for example:
    - Override existing parameters.
    - Modify the application behavior.
    - Access unauthorized data.
- You can test any user input for any kind of parameter pollution. 
- For example, query parameters, form fields, headers, and URL path parameters may all be vulnerable.

# Note
- This vulnerability is sometimes called HTTP parameter pollution. 
- However, this term is also used to refer to a web application firewall (WAF) bypass technique. 
- To avoid confusion, in this topic we'll only refer to server-side parameter pollution.
- In addition, despite the similar name, this vulnerability class has very little in common with server-side prototype pollution.

# Testing for server-side parameter pollution in the query string
- To test for server-side parameter pollution in the query string, place query syntax characters like #, &, and = in your input and observe how the application responds.
- Consider a vulnerable application that enables you to search for other users based on their username. 
- When you search for a user, your browser makes the following request:
- GET /userSearch?name=peter&back=/home
- To retrieve user information, the server queries an internal API with the following request:
- GET /users/search?name=peter&publicProfile=true

1. # Truncating query strings
- You can use a URL-encoded # character to attempt to truncate the server-side request. 
- To help you interpret the response, you could also add a string after the # character.
- For example, you could modify the query string to the following:
- GET /userSearch?name=peter%23foo&back=/home
- The front-end will try to access the following URL:
- GET /users/search?name=peter#foo&publicProfile=true
- # Note
- It's essential that you URL-encode the # character. Otherwise the front-end application will interpret it as a fragment identifier and it won't be passed to the internal API.
- Review the response for clues about whether the query has been truncated. 
- For example, if the response returns the user peter, the server-side query may have been truncated. 
- If an Invalid name error message is returned, the application may have treated foo as part of the username. 
- This suggests that the server-side request may not have been truncated.
- If you're able to truncate the server-side request, this removes the requirement for the publicProfile field to be set to true. 
- You may be able to exploit this to return non-public user profiles.

2. # Injecting invalid parameters
- You can use an URL-encoded & character to attempt to add a second parameter to the server-side request.
- For example, you could modify the query string to the following:
- GET /userSearch?name=peter%26foo=xyz&back=/home
- This results in the following server-side request to the internal API:
- GET /users/search?name=peter&foo=xyz&publicProfile=true
- Review the response for clues about how the additional parameter is parsed. 
- For example, if the response is unchanged this may indicate that the parameter was successfully injected but ignored by the application.
- To build up a more complete picture, you'll need to test further. 

3. # Injecting valid parameters
- If you're able to modify the query string, you can then attempt to add a second valid parameter to the server-side request.
- For example, if you've identified the email parameter, you could add it to the query string as follows:
- GET /userSearch?name=peter%26email=foo&back=/home
- This results in the following server-side request to the internal API:
- GET /users/search?name=peter&email=foo&publicProfile=true
- Review the response for clues about how the additional parameter is parsed

4. # Overriding existing parameters
- To confirm whether the application is vulnerable to server-side parameter pollution, you could try to override the original parameter. 
- Do this by injecting a second parameter with the same name.
- For example, you could modify the query string to the following:
- GET /userSearch?name=peter%26name=carlos&back=/home
- This results in the following server-side request to the internal API:
- GET /users/search?name=peter&name=carlos&publicProfile=true
- The internal API interprets two name parameters. 
- The impact of this depends on how the application processes the second parameter. 
- This varies across different web technologies. For example:
- PHP parses the last parameter only. This would result in a user search for carlos.
- ASP.NET combines both parameters. This would result in a user search for peter,carlos, which might result in an Invalid username error message.
- Node.js / express parses the first parameter only. This would result in a user search for peter, giving an unchanged result.
- If you're able to override the original parameter, you may be able to conduct an exploit. For example, you could add name=administrator to the request. 
- This may enable you to log in as the administrator user.

# Lab: Exploiting server-side parameter pollution in a query string
- To solve the lab, log in as the administrator and delete carlos.

# Required knowledge
- To solve this lab, you'll need to know:
- How to use URL query syntax to attempt to change a server-side request.
- How to use error messages to build an understanding of how a server-side API processes user input.

# Solution
- In Burp's browser, trigger a password reset for the administrator user.
- In Proxy > HTTP history, notice the POST /forgot-password request and the related /static/js/forgotPassword.js JavaScript file.
- Right-click the POST /forgot-password request and select Send to Repeater.
- In the Repeater tab, resend the request to confirm that the response is consistent.
- Change the value of the username parameter from administrator to an invalid username, such as administratorx. Send the request. Notice that this results in an Invalid username error message.
- Attempt to add a second parameter-value pair to the server-side request using a URL-encoded & character. For example, add URL-encoded &x=y:
- username=administrator%26x=y
- Send the request. Notice that this returns a Parameter is not supported error message. 
- This suggests that the internal API may have interpreted &x=y as a separate parameter, instead of part of the username.
- Attempt to truncate the server-side query string using a URL-encoded # character:
- username=administrator%23
- Send the request. Notice that this returns a Field not specified error message. 
- This suggests that the server-side query may include an additional parameter called field, which has been removed by the # character.
- Add a field parameter with an invalid value to the request. Truncate the query string after the added parameter-value pair. For example, add URL-encoded &field=x#:
- username=administrator%26field=x%23
- Send the request. Notice that this results in an Invalid field error message. This suggests that the server-side application may recognize the injected field parameter.
- Brute-force the value of the field parameter:
- Right-click the POST /forgot-password request and select Send to Intruder.
- In the Intruder tab, add a payload position to the value of the field parameter as follows:
- username=administrator%26field=§x§%23
- In the Payloads side panel, under Payload configuration, click Add from list. Select the built-in Server-side variable names payload list, then start the attack.
- Review the results. Notice that the requests with the username and email payloads both return a 200 response.
- Change the value of the field parameter from x# to email:
- username=administrator%26field=email%23
- Send the request. Notice that this returns the original response. This suggests that email is a valid field type.
- In Proxy > HTTP history, review the /static/js/forgotPassword.js JavaScript file. Notice the password reset endpoint, which refers to the reset_token parameter: /forgot-password?reset_token=${resetToken}
- In the Repeater tab, change the value of the field parameter from email to reset_token:
- username=administrator%26field=reset_token%23
- Send the request. Notice that this returns a password reset token. Make a note of this.
- In Burp's browser, enter the password reset endpoint in the address bar. Add your password reset token as the value of the reset_token parameter . For example: /forgot-password?reset_token=123456789
- Set a new password.
- Log in as the administrator user using your password.
- Go to the Admin panel and delete carlos to solve the lab.

# Testing for server-side parameter pollution in REST paths
- A RESTful API may place parameter names and values in the URL path, rather than the query string. For example, consider the following path:
```
/api/users/123
```
- The URL path might be broken down as follows:
- /api is the root API endpoint.
- /users represents a resource, in this case users.
- /123 represents a parameter, here an identifier for the specific user.
- Consider an application that enables you to edit user profiles based on their username. Requests are sent to the following endpoint:
```
GET /edit_profile.php?name=peter
```
- This results in the following server-side request:
```
GET /api/private/users/peter
```
- An attacker may be able to manipulate server-side URL path parameters to exploit the API. 
- To test for this vulnerability, add path traversal sequences to modify parameters and observe how the application responds.
- You could submit URL-encoded peter/../admin as the value of the name parameter:
```
GET /edit_profile.php?name=peter%2f..%2fadmin
```
- This may result in the following server-side request:
```
GET /api/private/users/peter/../admin
```
- If the server-side client or back-end API normalize this path, it may be resolved to /api/private/users/admin.

# Lab: Exploiting server-side parameter pollution in a REST URL
- To solve the lab, log in as the administrator and delete carlos.

# Solution
1. # Study the behavior
- In Burp's browser, trigger a password reset for the administrator user.
- In Proxy > HTTP history, notice the POST /forgot-password request and the related /static/js/forgotPassword.js JavaScript file.
- Right-click the POST /forgot-password request and select Send to Repeater.
- In the Repeater tab, resend the request to confirm that the response is consistent.
- Send a variety of requests with a modified username parameter value to determine whether the input is placed in the URL path of a server-side request without escaping:
- Submit URL-encoded administrator# as the value of the username parameter.
- Notice that this returns an Invalid route error message. 
- This suggests that the server may have placed the input in the path of a server-side request, and that the fragment has truncated some trailing data. 
- Observe that the message also refers to an API definition.
- Change the value of the username parameter from administrator%23 to URL-encoded administrator?, then send the request.
- Notice that this also returns an Invalid route error message. This suggests that the input may be placed in a URL path, as the ? character indicates the start of the query string and therefore truncates the URL path.
- Change the value of the username parameter from administrator%3F to ./administrator then send the request.
- Notice that this returns the original response. This suggests that the request may have accessed the same URL path as the original request. This further indicates that the input may be placed in the URL path.
- Change the value of the username parameter from ./administrator to ../administrator, then send the request.
- Notice that this returns an Invalid route error message. This suggests that the request may have accessed an invalid URL path.

2. Navigate to the API definition
- Change the value of the username parameter from ../administrator to ../%23. Notice the Invalid route response.
- Incrementally add further ../ sequences until you reach ../../../../%23 Notice that this returns a Not found response. This indicates that you've navigated outside the API root.
- At this level, add some common API definition filenames to the URL path. For example, submit the following:
- username=../../../../openapi.json%23
- Notice that this returns an error message, which contains the following API endpoint for finding users:
- /api/internal/v1/users/{username}/field/{field}
- Notice that this endpoint indicates that the URL path includes a parameter called field.

3. # Exploit the vulnerability
- Update the value of the username parameter, using the structure of the identified endpoint. Add an invalid value for the field parameter:

- username=administrator/field/foo%23
- Send the request. Notice that this returns an error message, because the API only supports the email field.
- Add email as the value of the field parameter:
- username=administrator/field/email%23
- Send the request. Notice that this returns the original response. This may indicate that the server-side application recognizes the injected field parameter and that email is a valid field type.
- In Proxy > HTTP history, review the /static/js/forgotPassword.js JavaScript file. Identify the password reset endpoint, which refers to the passwordResetToken parameter: /forgot-password?passwordResetToken=${resetToken}
- In the Repeater tab, change the value of the field parameter from email to passwordResetToken:
- username=administrator/field/passwordResetToken%23
- Send the request. Notice that this returns an error message, because the passwordResetToken parameter is not supported by the version of the API that is set by the application.
- Using the /api/ endpoint that you identified earlier, change the version of the API in the value of the username parameter:
- username=../../v1/users/administrator/field/passwordResetToken%23
- Send the request. Notice that this returns a password reset token. Make a note of this.
- In Burp's browser, enter the password reset endpoint in the address bar. Add your password reset token as the value of the reset_token parameter. For example: /forgot-password?passwordResetToken=123456789
- Set a new password.
- Log in as the administrator using your password.
- Go to the Admin panel and delete carlos to solve the lab.