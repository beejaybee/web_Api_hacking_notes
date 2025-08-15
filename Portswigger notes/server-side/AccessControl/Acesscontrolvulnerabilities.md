# Access control vulnerabilities and privilege escalation
- In this section, we describe:
    - Privilege escalation.
    - The types of vulnerabilities that can arise with access control.
    - How to prevent access control vulnerabilities.

# What is access control?
- Access control is the application of constraints on who or what is authorized to perform actions or access resources. 
- In the context of web applications, access control is dependent on authentication and session management:
- Authentication confirms that the user is who they say they are.
- Session management identifies which subsequent HTTP requests are being made by that same user.
- Access control determines whether the user is allowed to carry out the action that they are attempting to perform.
- Broken access controls are common and often present a critical security vulnerability. 
- Design and management of access controls is a complex and dynamic problem that applies business, organizational, and legal constraints to a technical implementation. 
- Access control design decisions have to be made by humans so the potential for errors is high.

# Vertical access controls
- Vertical access controls are mechanisms that restrict access to sensitive functionality to specific types of users.
- With vertical access controls, different types of users have access to different application functions. 
- For example, an administrator might be able to modify or delete any user's account, while an ordinary user has no access to these actions. 
- Vertical access controls can be more fine-grained implementations of security models designed to enforce business policies such as separation of duties and least privilege.

# Horizontal access controls
- Horizontal access controls are mechanisms that restrict access to resources to specific users.
- With horizontal access controls, different users have access to a subset of resources of the same type. 
- For example, a banking application will allow a user to view transactions and make payments from their own accounts, but not the accounts of any other user.

# Context-dependent access controls
- Context-dependent access controls restrict access to functionality and resources based upon the state of the application or the user's interaction with it.
- Context-dependent access controls prevent a user performing actions in the wrong order. For example, a retail website might prevent users from modifying the contents of their shopping cart after they have made payment.

# Examples of broken access controls
- Broken access control vulnerabilities exist when a user can access resources or perform actions that they are not supposed to be able to.

# Vertical privilege escalation
- If a user can gain access to functionality that they are not permitted to access then this is vertical privilege escalation. 
- For example, if a non-administrative user can gain access to an admin page where they can delete user accounts, then this is vertical privilege escalation.

# Unprotected functionality
- At its most basic, vertical privilege escalation arises where an application does not enforce any protection for sensitive functionality. 
- For example, administrative functions might be linked from an administrator's welcome page but not from a user's welcome page. However, a user might be able to access the administrative functions by browsing to the relevant admin URL.
- For example, a website might host sensitive functionality at the following URL: https://insecure-website.com/admin
- This might be accessible by any user, not only administrative users who have a link to the functionality in their user interface. 
- In some cases, the administrative URL might be disclosed in other locations, such as the robots.txt file: https://insecure-website.com/robots.txt
- Even if the URL isn't disclosed anywhere, an attacker may be able to use a wordlist to brute-force the location of the sensitive functionality.

# Lab: Unprotected admin functionality
- This lab has an unprotected admin panel.
- Solve the lab by deleting the user carlos.

# Solution
- Go to the lab and view robots.txt by appending /robots.txt to the lab URL. 
- Notice that the Disallow line discloses the path to the admin panel.
- In the URL bar, replace /robots.txt with /administrator-panel to load the admin panel.
- Delete carlos

# Continuation
- In some cases, sensitive functionality is concealed by giving it a less predictable URL. 
- This is an example of so-called "security by obscurity". 
- However, hiding sensitive functionality does not provide effective access control because users might discover the obfuscated URL in a number of ways.
- Imagine an application that hosts administrative functions at the following URL: https://insecure-website.com/administrator-panel-yb556
- This might not be directly guessable by an attacker. 
- However, the application might still leak the URL to users. 
- The URL might be disclosed in JavaScript that constructs the user interface based on the user's role:
```
<script>
	var isAdmin = false;
	if (isAdmin) {
		...
		var adminPanelTag = document.createElement('a');
		adminPanelTag.setAttribute('href', 'https://insecure-website.com/administrator-panel-yb556');
		adminPanelTag.innerText = 'Admin panel';
		...
	}
</script>
```
- This script adds a link to the user's UI if they are an admin user. However, the script containing the URL is visible to all users regardless of their role.

# Lab: Unprotected admin functionality with unpredictable URL
- This lab has an unprotected admin panel. 
- It's located at an unpredictable location, but the location is disclosed somewhere in the application.
- Solve the lab by accessing the admin panel, and using it to delete the user carlos.

# Solution
- Read javascript files
- Review the lab home page's source using Burp Suite or your web browser's developer tools.
- Observe that it contains some JavaScript that discloses the URL of the admin panel.
- Load the admin panel and delete carlos.

# Parameter-based access control methods
- Some applications determine the user's access rights or role at login, and then store this information in a user-controllable location. 
- This could be:
    1. A hidden field.
    2. A cookie.
    3. A preset query string parameter.
- The application makes access control decisions based on the submitted value. 
- For example: https://insecure-website.com/login/home.jsp?admin=true, https://insecure-website.com/login/home.jsp?role=1
- This approach is insecure because a user can modify the value and access functionality they're not authorized to, such as administrative functions.

# Lab: User role controlled by request parameter
- This lab has an admin panel at /admin, which identifies administrators using a forgeable cookie.
- Solve the lab by accessing the admin panel and using it to delete the user carlos.
- You can log in to your own account using the following credentials: wiener:peter

# My Solution
- I Notice that after logging in, every request has an admin=false in the cookie
- Then I requested for the admin lab 
- I was asked to login
- I put on intercept and intercepted the request
- Then I change the admin=false to true on every request made
- Then I could see the admin panel
- I tried deleting carlos with intercept on, and changed the admin=false to true and carlos was deleted

# Lab Solution
- Browse to /admin and observe that you can't access the admin panel.
- Browse to the login page.
- In Burp Proxy, turn interception on and enable response interception.
- Complete and submit the login page, and forward the resulting request in Burp.
- Observe that the response sets the cookie Admin=false. Change it to Admin=true.
- Load the admin panel and delete carlos.

# Lab: User role can be modified in user profile
- This lab has an admin panel at /admin. 
- It's only accessible to logged-in users with a roleid of 2.
- Solve the lab by accessing the admin panel and using it to delete the user carlos.
- You can log in to your own account using the following credentials: wiener:peter

# My Solution
- I solved this by doing the following
    1. I browsed throughout the app 
    2. There was no user input that has roleid
    3. Then I tried changing the email, and I notice that mass assignment might be possible
    4. I added roleid:2 along with the email parameter
    5. The role was accepted and the admin panel button was included in the UI
    6. I deleted carlos and the lab was solved

# Lab Solution
- Log in using the supplied credentials and access your account page.
- Use the provided feature to update the email address associated with your account.
- Observe that the response contains your role ID.
- Send the email submission request to Burp Repeater, add "roleid":2 into the JSON in the request body, and resend it.
- Observe that the response shows your roleid has changed to 2.
- Browse to /admin and delete carlos.

# Broken access control resulting from platform misconfiguration
- Some applications enforce access controls at the platform layer. 
- they do this by restricting access to specific URLs and HTTP methods based on the user's role. 
- For example, an application might configure a rule as follows:
```
DENY: POST, /admin/deleteUser, managers
```
- This rule denies access to the POST method on the URL /admin/deleteUser, for users in the managers group. 
- Various things can go wrong in this situation, leading to access control bypasses.
- Some application frameworks support various non-standard HTTP headers that can be used to override the URL in the original request, such as ```X-Original-URL``` and ```X-Rewrite-URL```. 
- If a website uses rigorous front-end controls to restrict access based on the URL, but the application allows the URL to be overridden via a request header, then it might be possible to bypass the access controls using a request like the following:
```
POST / HTTP/1.1
X-Original-URL: /admin/deleteUser
...
```
# Lab: URL-based access control can be circumvented
- This website has an unauthenticated admin panel at /admin, but a front-end system has been configured to block external access to that path. 
- However, the back-end application is built on a framework that supports the X-Original-URL header.
- To solve the lab, access the admin panel and delete the user carlos.

