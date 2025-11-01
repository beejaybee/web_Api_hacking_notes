# Examples of business logic vulnerabilities
- Business logic vulnerabilities are relatively specific to the context in which they occur. 
- However, although individual instances of logic flaws differ hugely, they can share many common themes. 
- In particular, they can be loosely grouped based on the initial mistakes that introduced the vulnerability in the first place.
- In this section, we'll look at examples of some typical mistakes that design and development teams make and show you how they can directly lead to business logic flaws. 
- Whether you're developing your own applications, or auditing existing ones, you can take the lessons learned from these examples and apply the same critical thinking to other applications that you encounter.
- Examples of logic flaws include:
1. Excessive trust in client-side controls LABS
2. Failing to handle unconventional input LABS
3. Making flawed assumptions about user behavior LABS
4. Domain-specific flaws LABS
5. Providing an encryption oracle LABS
6. Email address parser discrepancies LABS


# 1. Excessive trust in client-side controls
- A fundamentally flawed assumption is that users will only interact with the application via the provided web interface. 
- This is especially dangerous because it leads to the further assumption that client-side validation will prevent users from supplying malicious input. 
- However, an attacker can simply use tools such as Burp Proxy to tamper with the data after it has been sent by the browser but before it is passed into the server-side logic. 
- This effectively renders the client-side controls useless.
- Accepting data at face value, without performing proper integrity checks and server-side validation, can allow an attacker to do all kinds of damage with relatively minimal effort. 
- Exactly what they are able to achieve is dependent on the functionality and what it is doing with the controllable data. 
- In the right context, this kind of flaw can have devastating consequences for both business-related functionality and the security of the website itself.

# Lab: Excessive trust in client-side controls
- This lab doesn't adequately validate user input. 
- You can exploit a logic flaw in its purchasing workflow to buy items for an unintended price. 
- To solve the lab, buy a "Lightweight l33t leather jacket".
- You can log in to your own account using the following credentials: wiener:peter

# Solution
- With Burp running, log in and attempt to buy the leather jacket. The order is rejected because you don't have enough store credit.
- In Burp, go to "Proxy" > "HTTP history" and study the order process. 
- Notice that when you add an item to your cart, the corresponding request contains a price parameter. 
- Send the POST /cart request to Burp Repeater.
- In Burp Repeater, change the price to an arbitrary integer and send the request. 
- Refresh the cart and confirm that the price has changed based on your input.
- Repeat this process to set the price to any amount less than your available store credit.
- Complete the order to solve the lab.

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

# Lab Solution
- With Burp running, log in to your own account and investigate the 2FA verification process. 
- Notice that in the POST /login2 request, the verify parameter is used to determine which user's account is being accessed.
- Log out of your account.
- Send the GET /login2 request to Burp Repeater. 
- Change the value of the verify parameter to carlos and send the request. This ensures that a temporary 2FA code is generated for Carlos.
- Go to the login page and enter your username and password. Then, submit an invalid 2FA code.
- Send the POST /login2 request to Burp Intruder.
- In Burp Intruder, set the verify parameter to carlos and add a payload position to the mfa-code parameter. Brute-force the verification code.
- Load the 302 response in the browser.
- Click My account to solve the lab.


# 2. Failing to handle unconventional input
- One aim of the application logic is to restrict user input to values that adhere to the business rules. 
- For example, the application may be designed to accept arbitrary values of a certain data type, but the logic determines whether or not this value is acceptable from the perspective of the business. 
- Many applications incorporate numeric limits into their logic. 
- This might include limits designed to manage inventory, apply budgetary restrictions, trigger phases of the supply chain, and so on.
- Let's take the simple example of an online shop. 
- When ordering products, users typically specify the quantity that they want to order. 
- Although any integer is theoretically a valid input, the business logic might prevent users from ordering more units than are currently in stock, for example.
- To implement rules like this, developers need to anticipate all possible scenarios and incorporate ways to handle them into the application logic. 
- In other words, they need to tell the application whether it should allow a given input and how it should react based on various conditions. 
- If there is no explicit logic for handling a given case, this can lead to unexpected and potentially exploitable behavior.
- For example, a numeric data type might accept negative values. 
- Depending on the related functionality, it may not make sense for the business logic to allow this. 
- However, if the application doesn't perform adequate server-side validation and reject this input, an attacker may be able to pass in a negative value and induce unwanted behavior.
- Consider a funds transfer between two bank accounts. This functionality will almost certainly check whether the sender has sufficient funds before completing the transfer:
```
$transferAmount = $_POST['amount'];
$currentBalance = $user->getBalance();

if ($transferAmount <= $currentBalance) {
    // Complete the transfer
} else {
    // Block the transfer: insufficient funds
}
```
- But if the logic doesn't sufficiently prevent users from supplying a negative value in the amount parameter, this could be exploited by an attacker to both bypass the balance check and transfer funds in the "wrong" direction. 
- If the attacker sent -$1000 to the victim's account, this might result in them receiving $1000 from the victim instead. 
- The logic would always evaluate that -1000 is less than the current balance and approve the transfer.
- Simple logic flaws like this can be devastating if they occur in the right functionality. 
- They are also easy to miss during both development and testing, especially given that such inputs may be blocked by client-side controls on the web interface.
- When auditing an application, you should use tools such as Burp Proxy and Repeater to try submitting unconventional values. 
- In particular, try input in ranges that legitimate users are unlikely to ever enter. 
- This includes exceptionally high or exceptionally low numeric inputs and abnormally long strings for text-based fields. 
- You can even try unexpected data types. 
- By observing the application's response, you should try and answer the following questions:
- Are there any limits that are imposed on the data?
- What happens when you reach those limits?
- Is any transformation or normalization being performed on your input?
- This may expose weak input validation that allows you to manipulate the application in unusual ways. 
- Keep in mind that if you find one form on the target website that fails to safely handle unconventional input, it's likely that other forms will have the same issues.

# Lab: High-level logic vulnerability
- This lab doesn't adequately validate user input. 
- You can exploit a logic flaw in its purchasing workflow to buy items for an unintended price. 
- To solve the lab, buy a "Lightweight l33t leather jacket".
- You can log in to your own account using the following credentials: wiener:peter

Solution
- With Burp running, log in and add a cheap item to your cart.
- In Burp, go to "Proxy" > "HTTP history" and study the corresponding HTTP messages. 
- Notice that the quantity is determined by a parameter in the POST /cart request.
- Go to the "Intercept" tab and turn on interception. Add another item to your cart and go to the intercepted POST /cart request in Burp.
- Change the quantity parameter to an arbitrary integer, then forward any remaining requests. 
- Observe that the quantity in the cart was successfully updated based on your input.
- Repeat this process, but request a negative quantity this time. 
- Check that this is successfully deducted from the cart quantity.
- Request a suitable negative quantity to remove more units from the cart than it currently contains. 
- Confirm that you have successfully forced the cart to contain a negative quantity of the product. 
- Go to your cart and notice that the total price is now also a negative amount.
- Add the leather jacket to your cart as normal. 
- Add a suitable negative quantity of the another item to reduce the total price to less than your remaining store credit.
- Place the order to solve the lab.

# Lab: Low-level logic flaw
- This lab doesn't adequately validate user input. 
- You can exploit a logic flaw in its purchasing workflow to buy items for an unintended price. 
- To solve the lab, buy a "Lightweight l33t leather jacket".
- You can log in to your own account using the following credentials: wiener:peter

# My Solution
- With burp runing, I sent a Post /cart with the cheapeast product or any product
- In Burp, I sent the request to burp repeater and noticed that I can only add a two digit quantity
- I changed the quantity to 99 and sent the request to burp turbo intuder, in intruder I used the code below
```python
def queueRequests(target, wordlists):

    # if the target supports HTTP/2, use engine=Engine.BURP2 to trigger the single-packet attack
    # if they only support HTTP/1, use Engine.THREADED or Engine.BURP instead
    # for more information, check out https://portswigger.net/research/smashing-the-state-machine
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1000,
                           engine=Engine.BURP2
                           )

    # the 'gate' argument withholds part of each request until openGate is invoked
    # if you see a negative timestamp, the server responded before the request was complete
    for i in range(100000):
        engine.queue(target.req)

    # once every 'race1' tagged request has been queued
    # invoke engine.openGate() to send them in sync


def handleResponse(req, interesting):
    table.add(req)
```
- I kept refreshing the page until I noticed the price changed to negative value
- I stopped the attack and add another product to the cart and sent that request to burp turbo intruder too.
- I noticed that the price is moving towards zero
- I made sure the price is close to -1200 or so then I added a the jacket, the price is now within the $100 price
- I placed the other and the lab was solved

# Lab Solution
- With Burp running, log in and attempt to buy the leather jacket. 
- The order is rejected because you don't have enough store credit. 
- In the proxy history, study the order process. 
- Send the POST /cart request to Burp Repeater.
- In Burp Repeater, notice that you can only add a 2-digit quantity with each request. 
- Send the request to Burp Intruder.
- Go to Intruder and set the quantity parameter to 99.
- In the Payloads side panel, select the payload type Null payloads. 
- Under Payload configuration, select Continue indefinitely. Start the attack.
- While the attack is running, go to your cart. 
- Keep refreshing the page every so often and monitor the total price. 
- Eventually, notice that the price suddenly switches to a large negative integer and starts counting up towards 0. 
- The price has exceeded the maximum value permitted for an integer in the back-end programming language (2,147,483,647). 
- As a result, the value has looped back around to the minimum possible value (-2,147,483,648).
- Clear your cart. 
- In the next few steps, we'll try to add enough units so that the price loops back around and settles between $0 and the $100 of your remaining store credit. 
- This is not mathematically possible using only the leather jacket. Note that the price of the jacket is stored in cents (133700).
- Create the same Intruder attack again, but this time under Payload configuration, choose to generate exactly 323 payloads.
- Click  Resource pool to open the Resource pool tab. Add the attack to a resource pool with the Maximum concurrent requests set to 1. Start the attack.
- When the Intruder attack finishes, go to the POST /cart request in Burp Repeater and send a single request for 47 jackets. The total price of the order should now be -$1221.96.
- Use Burp Repeater to add a suitable quantity of another item to your cart so that the total falls between $0 and $100.
- Place the order to solve the lab.
- **I DID NOT UNDERSTAND THIS SOLUTION THOUGH**

# Trusted users won't always remain trustworthy
- Applications may appear to be secure because they implement seemingly robust measures to enforce the business rules. 
- Unfortunately, some applications make the mistake of assuming that, having passed these strict controls initially, the user and their data can be trusted indefinitely. 
- This can result in relatively lax enforcement of the same controls from that point on.
- If business rules and security measures are not applied consistently throughout the application, this can lead to potentially dangerous loopholes that may be exploited by an attacker.

# Solution
- Open the lab then go to the "Target" > "Site map" tab in Burp. Right-click on the lab domain and select "Engagement tools" > "Discover content" to open the content discovery tool.
- Use Turbo intruder instead
- Click "Session is not running" to start the content discovery. After a short while, look at the "Site map" tab in the dialog. Notice that it discovered the path /admin.
- Try and browse to /admin. Although you don't have access, the error message indicates that DontWannaCry users do.
- Go to the account registration page. Notice the message telling DontWannaCry employees to use their company email address. Register with an arbitrary email address in the format:
- anything@your-email-id.web-security-academy.net
- You can find your email domain name by clicking the "Email client" button.
- Go to the email client and click the link in the confirmation email to complete the registration.
- Log in using your new account and go to the "My account" page. Notice that you have the option to change your email address. Change your email address to an arbitrary @dontwannacry.com address.
- Notice that you now have access to the admin panel, where you can delete carlos to solve the lab.

# Users won't always supply mandatory input
- One misconception is that users will always supply values for mandatory input fields. 
- Browsers may prevent ordinary users from submitting a form without a required input, but as we know, attackers can tamper with parameters in transit. 
- This even extends to removing parameters entirely.
- This is a particular issue in cases where multiple functions are implemented within the same server-side script. 
- In this case, the presence or absence of a particular parameter may determine which code is executed. 
- Removing parameter values may allow an attacker to access code paths that are supposed to be out of reach.
- When probing for logic flaws, you should try removing each parameter in turn and observing what effect this has on the response. You should make sure to:
- Only remove one parameter at a time to ensure all relevant code paths are reached.
- Try deleting the name of the parameter as well as the value. The server will typically handle both cases differently.
- Follow multi-stage processes through to completion. 
- Sometimes tampering with a parameter in one step will have an effect on another step further along in the workflow.
- This applies to both URL and POST parameters, but don't forget to check the cookies too. 
- This simple process can reveal some bizarre application behavior that may be exploitable.


# Lab: Weak isolation on dual-use endpoint

- This lab makes a flawed assumption about the user's privilege level based on their input. 
- As a result, you can exploit the logic of its account management features to gain access to arbitrary users' accounts. 
- To solve the lab, access the administrator account and delete the user carlos.
- You can log in to your own account using the following credentials: wiener:peter

# Solution
- With Burp running, log in and access your account page.
- Change your password.
- Study the POST /my-account/change-password request in Burp Repeater.
- Notice that if you remove the current-password parameter entirely, you are able to successfully change your password without providing your current one.
- Observe that the user whose password is changed is determined by the username parameter. Set username=administrator and send the request again.
- Log out and notice that you can now successfully log in as the administrator using the password you just set.
- Go to the admin panel and delete carlos to solve the lab.

# Lab: Password reset broken logic
- This lab's password reset functionality is vulnerable. 
- To solve the lab, reset Carlos's password then log in and access his "My account" page.
- Your credentials: wiener:peter
- Victim's username: carlos

# Solution
- With Burp running, click the Forgot your password? link and enter your own username.
- Click the Email client button to view the password reset email that was sent. 
- Click the link in the email and reset your password to whatever you want.
- In Burp, go to Proxy > HTTP history and study the requests and responses for the password reset functionality. 
- Observe that the reset token is provided as a URL query parameter in the reset email. 
- Notice that when you submit your new password, the POST /forgot-password?temp-forgot-password-token request contains the username as hidden input. Send this request to Burp Repeater.
- In Burp Repeater, observe that the password reset functionality still works even if you delete the value of the temp-forgot-password-token parameter in both the URL and request body. This confirms that the token is not being checked when you submit the new password.
- In the browser, request a new password reset and change your password again. Send the POST /forgot-password?temp-forgot-password-token request to Burp Repeater again.
- In Burp Repeater, delete the value of the temp-forgot-password-token parameter in both the URL and request body. Change the username parameter to carlos. Set the new password to whatever you want and send the request.
- In the browser, log in to Carlos's account using the new password you just set. Click My account to solve the lab.

# Users won't always follow the intended sequence
- Many transactions rely on predefined workflows consisting of a sequence of steps. 
- The web interface will typically guide users through this process, taking them to the next step of the workflow each time they complete the current one. 
- However, attackers won't necessarily adhere to this intended sequence. Failing to account for this possibility can lead to dangerous flaws that may be relatively simple to exploit.
- For example, many websites that implement two-factor authentication (2FA) require users to log in on one page before entering a verification code on a separate page. 
- Assuming that users will always follow this process through to completion and, as a result, not verifying that they do, may allow attackers to bypass the 2FA step entirely.

# Lab: 2FA simple bypass
- This lab's two-factor authentication can be bypassed. 
- You have already obtained a valid username and password, but do not have access to the user's 2FA verification code. 
- To solve the lab, access Carlos's account page.
- Your credentials: wiener:peter
- Victim's credentials carlos:montoya

# Solution
- Log in to your own account. Your 2FA verification code will be sent to you by email. 
- Click the Email client button to access your emails.
- Go to your account page and make a note of the URL.
- Log out of your account.
- Log in using the victim's credentials.
- When prompted for the verification code, manually change the URL to navigate to /my-account. The lab is solved when the page loads.

# Continuation
- Making assumptions about the sequence of events can lead to a wide range of issues even within the same workflow or functionality. 
- Using tools like Burp Proxy and Repeater, once an attacker has seen a request, they can replay it at will and use forced browsing to perform any interactions with the server in any order they want. 
- This allows them to complete different actions while the application is in an unexpected state.
- To identify these kinds of flaws, you should use forced browsing to submit requests in an unintended sequence. 
- For example, you might skip certain steps, access a single step more than once, return to earlier steps, and so on. 
- Take note of how different steps are accessed. 
- Although you often just submit a GET or POST request to a specific URL, sometimes you can access steps by submitting different sets of parameters to the same URL. 
- As with all logic flaws, try to identify what assumptions the developers have made and where the attack surface lies. 
- You can then look for ways of violating these assumptions.
- Note that this kind of testing will often cause exceptions because expected variables have null or uninitialized values. 
- Arriving at a location in a partly defined or inconsistent state is also likely to cause the application to complain. 
- In this case, be sure to pay close attention to any error messages or debug information that you encounter. 
- These can be a valuable source of information disclosure, which can help you fine-tune your attack and understand key details about the back-end behavior.

# Lab: Insufficient workflow validation
- This lab makes flawed assumptions about the sequence of events in the purchasing workflow. 
- To solve the lab, exploit this flaw to buy a "Lightweight l33t leather jacket".
- You can log in to your own account using the following credentials: wiener:peter

# Solution
- With Burp running, log in and buy any item that you can afford with your store credit.
- Study the proxy history. 
- Observe that when you place an order, the POST /cart/checkout request redirects you to an order confirmation page. 
- Send GET /cart/order-confirmation?order-confirmation=true to Burp Repeater.
- Add the leather jacket to your basket.
- In Burp Repeater, resend the order confirmation request. 
- Observe that the order is completed without the cost being deducted from your store credit and the lab is solved.

# Lab: Authentication bypass via flawed state machine
- This lab makes flawed assumptions about the sequence of events in the login process. 
- To solve the lab, exploit this flaw to bypass the lab's authentication, access the admin interface, and delete the user carlos.
- You can log in to your own account using the following credentials: wiener:peter

# Solution
- With Burp running, complete the login process and notice that you need to select your role before you are taken to the home page.
- Use the content discovery tool to identify the /admin path.
- Try browsing to /admin directly from the role selection page and observe that this doesn't work.
- Log out and then go back to the login page. In Burp, turn on proxy intercept then log in.
- Forward the POST /login request. 
- The next request is GET /role-selector. 
- Drop this request and then browse to the lab's home page. Observe that your role has defaulted to the administrator role and you have access to the admin panel.
- Delete carlos to solve the lab.

# Domain-specific flaws
- In many cases, you will encounter logic flaws that are specific to the business domain or the purpose of the site.
- The discounting functionality of online shops is a classic attack surface when hunting for logic flaws. 
- This can be a potential gold mine for an attacker, with all kinds of basic logic flaws occurring in the way discounts are applied.
- For example, consider an online shop that offers a 10% discount on orders over $1000. 
- This could be vulnerable to abuse if the business logic fails to check whether the order was changed after the discount is applied. 
- In this case, an attacker could simply add items to their cart until they hit the $1000 threshold, then remove the items they don't want before placing the order. 
- They would then receive the discount on their order even though it no longer satisfies the intended criteria.
- You should pay particular attention to any situation where prices or other sensitive values are adjusted based on criteria determined by user actions. 
- Try to understand what algorithms the application uses to make these adjustments and at what point these adjustments are made. 
- This often involves manipulating the application so that it is in a state where the applied adjustments do not correspond to the original criteria intended by the developers.
- To identify these vulnerabilities, you need to think carefully about what objectives an attacker might have and try to find different ways of achieving this using the provided functionality. 
- This may require a certain level of domain-specific knowledge in order to understand what might be advantageous in a given context. 
- To use a simple example, you need to understand social media to understand the benefits of forcing a large number of users to follow you.
- Without this knowledge of the domain, you may dismiss dangerous behavior because you simply aren't aware of its potential knock-on effects. 
- Likewise, you may struggle to join the dots and notice how two functions can be combined in a harmful way. 
- For simplicity, the examples used in this topic are specific to a domain that all users will already be familiar with, namely an online shop. 
- However, whether you're bug bounty hunting, pentesting, or even just a developer trying to write more secure code, you may at some point encounter applications from less familiar domains. 
- In this case, you should read as much documentation as possible and, where available, talk to subject-matter experts from the domain to get their insight. 
- This may sound like a lot of work, but the more obscure the domain is, the more likely other testers will have missed plenty of bugs.


# Lab: Flawed enforcement of business rules
- This lab has a logic flaw in its purchasing workflow. 
- To solve the lab, exploit this flaw to buy a "Lightweight l33t leather jacket".
- You can log in to your own account using the following credentials: wiener:peter

# Solution
- Log in and notice that there is a coupon code, NEWCUST5.
- At the bottom of the page, sign up to the newsletter. You receive another coupon code, SIGNUP30.
- Add the leather jacket to your cart.
- Go to the checkout and apply both of the coupon codes to get a discount on your order.
- Try applying the codes more than once. 
- Notice that if you enter the same code twice in a row, it is rejected because the coupon has already been applied. 
- However, if you alternate between the two codes, you can bypass this control.
- Reuse the two codes enough times to reduce your order total to less than your remaining store credit. Complete the order to solve the lab.

# Lab: Infinite money logic flaw
- This lab has a logic flaw in its purchasing workflow. 
- To solve the lab, exploit this flaw to buy a "Lightweight l33t leather jacket".
- You can log in to your own account using the following credentials: wiener:peter

# Solution
- This solution uses Burp Intruder to automate the process of buying and redeeming gift cards. 
- Users proficient in Python might prefer to use the Turbo Intruder extension instead.
- With Burp running, log in and sign up for the newsletter to obtain a coupon code, SIGNUP30. 
- Notice that you can buy $10 gift cards and redeem them from the My account page.
- Add a gift card to your basket and proceed to the checkout. 
- Apply the coupon code to get a 30% discount. 
- Complete the order and copy the gift card code to your clipboard.
- Go to your account page and redeem the gift card. 
- Observe that this entire process has added $3 to your store credit. 
- Now you need to try and automate this process.
- Study the proxy history and notice that you redeem your gift card by supplying the code in the gift-card parameter of the POST /gift-card request.
- Click  Settings in the top toolbar. The Settings dialog opens.
- Click Sessions. In the Session handling rules panel, click Add. The Session handling rule editor dialog opens.
- In the dialog, go to the Scope tab. Under URL scope, select Include all URLs.
- Go back to the Details tab. Under Rule actions, click Add > Run a macro. Under Select macro, click Add again to open the Macro Recorder.
- Select the following sequence of requests:
```
POST /cart
POST /cart/coupon
POST /cart/checkout
GET /cart/order-confirmation?order-confirmed=true
POST /gift-card
```
- Then, click OK. The Macro Editor opens.
- In the list of requests, select GET /cart/order-confirmation?order-confirmed=true.
- Click Configure item. In the dialog that opens, click Add to create a custom parameter. 
- Name the parameter gift-card and highlight the gift card code at the bottom of the response. 
- Click OK twice to go back to the Macro Editor.
- Select the POST /gift-card request and click Configure item again. 
- In the Parameter handling section, use the drop-down menus to specify that the gift-card parameter should be derived from the prior response (response 4). Click OK.
- In the Macro Editor, click Test macro. Look at the response to GET /cart/order-confirmation?order-confirmation=true and note the gift card code that was generated. 
- Look at the POST /gift-card request. Make sure that the gift-card parameter matches and confirm that it received a 302 response. Keep clicking OK until you get back to the main Burp window.
- Send the GET /my-account request to Burp Intruder. Make sure that Sniper attack is selected.
- In the Payloads side panel, under Payload configuration, select the payload type Null payloads. Choose to generate 412 payloads.
- Click on  Resource pool to open the Resource pool side panel. Add the attack to a resource pool with the Maximum concurrent requests set to 1. Start the attack.
- When the attack finishes, you will have enough store credit to buy the jacket and solve the lab

# Providing an encryption oracle
- Dangerous scenarios can occur when user-controllable input is encrypted and the resulting ciphertext is then made available to the user in some way. 
- This kind of input is sometimes known as an "encryption oracle". 
- An attacker can use this input to encrypt arbitrary data using the correct algorithm and asymmetric key.
- This becomes dangerous when there are other user-controllable inputs in the application that expect data encrypted with the same algorithm. 
- In this case, an attacker could potentially use the encryption oracle to generate valid, encrypted input and then pass it into other sensitive functions.
- This issue can be compounded if there is another user-controllable input on the site that provides the reverse function. 
- This would enable the attacker to decrypt other data to identify the expected structure. 
- This saves them some of the work involved in creating their malicious data but is not necessarily required to craft a successful exploit.
- The severity of an encryption oracle depends on what functionality also uses the same algorithm as the oracle.

# Lab: Authentication bypass via encryption oracle
- This lab contains a logic flaw that exposes an encryption oracle to users. 
- To solve the lab, exploit this flaw to gain access to the admin panel and delete the user carlos.
- You can log in to your own account using the following credentials: wiener:peter

# Solution
- Log in with the "Stay logged in" option enabled and post a comment. Study the corresponding requests and responses using Burp's manual testing tools. Observe that the stay-logged-in cookie is encrypted.
- Notice that when you try and submit a comment using an invalid email address, the response sets an encrypted notification cookie before redirecting you to the blog post.
- Notice that the error message reflects your input from the email parameter in cleartext:
- Invalid email address: your-invalid-email
- Deduce that this must be decrypted from the notification cookie. Send the POST /post/comment and the subsequent GET /post?postId=x request (containing the notification cookie) to Burp Repeater.
- In Repeater, observe that you can use the email parameter of the POST request to encrypt arbitrary data and reflect the corresponding ciphertext in the Set-Cookie header. 
- Likewise, you can use the notification cookie in the GET request to decrypt arbitrary ciphertext and reflect the output in the error message. 
- For simplicity, double-click the tab for each request and rename the tabs encrypt and decrypt respectively.
- In the decrypt request, copy your stay-logged-in cookie and paste it into the notification cookie. 
- Send the request. Instead of the error message, the response now contains the decrypted stay-logged-in cookie, for example: wiener:1598530205184
- This reveals that the cookie should be in the format username:timestamp. Copy the timestamp to your clipboard.
- Go to the encrypt request and change the email parameter to administrator:your-timestamp. Send the request and then copy the new notification cookie from the response.
- Decrypt this new cookie and observe that the 23-character "Invalid email address: " prefix is automatically added to any value you pass in using the email parameter. Send the notification cookie to Burp Decoder.
- In Decoder, URL-decode and Base64-decode the cookie.
- In Burp Repeater, switch to the message editor's "Hex" tab. Select the first 23 bytes, then right-click and select "Delete selected bytes".
- Re-encode the data and copy the result into the notification cookie of the decrypt request. 
- When you send the request, observe that an error message indicates that a block-based encryption algorithm is used and that the input length must be a multiple of 16. 
- You need to pad the "Invalid email address: " prefix with enough bytes so that the number of bytes you will remove is a multiple of 16.
- In Burp Repeater, go back to the encrypt request and add 9 characters to the start of the intended cookie value, for example: xxxxxxxxxadministrator:your-timestamp
- Encrypt this input and use the decrypt request to test that it can be successfully decrypted.
- Send the new ciphertext to Decoder, then URL and Base64-decode it. 
- This time, delete 32 bytes from the start of the data. 
- Re-encode the data and paste it into the notification parameter in the decrypt request. 
- Check the response to confirm that your input was successfully decrypted and, crucially, no longer contains the "Invalid email address: " prefix. 
- You should only see administrator:your-timestamp.
- From the proxy history, send the GET / request to Burp Repeater. Delete the session cookie entirely, and replace the stay-logged-in cookie with the ciphertext of your self-made cookie. 
- Send the request. Observe that you are now logged in as the administrator and have access to the admin panel.
- Using Burp Repeater, browse to /admin and notice the option for deleting users. Browse to /admin/delete?username=carlos to solve the lab.

# Email address parser discrepancies
- Some websites parse email addresses to extract the domain and determine which organization the email owner belongs to. 
- While this process may initially seem straightforward, it is actually very complex, even for valid RFC-compliant addresses.
- Discrepancies in how email addresses are parsed can undermine this logic. 
- These discrepancies arise when different parts of the application handle email addresses differently.
- An attacker can exploit these discrepancies using encoding techniques to disguise parts of the email address. 
- This enables the attacker to create email addresses that pass initial validation checks but are interpreted differently by the server's parsing logic.
- The main impact of email address parser discrepancies is unauthorized access. 
- Attackers can register accounts using seemingly valid email addresses from restricted domains. 
- This enables them to gain access to sensitive areas of the application, such as admin panels or restricted user functions.

# RESEARCH: Splitting the email atom: exploiting parsers to bypass access controls
- Read the research paper

# Lab: Bypassing access controls using email address parsing discrepancies
- This lab validates email addresses to prevent attackers from registering addresses from unauthorized domains. 
- There is a parser discrepancy in the validation logic and library used to parse email addresses.
- To solve the lab, exploit this flaw to register an account and delete carlos.

# Solution

1. # Identify the registration restriction
- Open the lab and click Register.
- Attempt to register an account with the email foo@exploit-server.net.
- Notice that the application blocks the request and displays an error message stating that the email domain must be ginandjuice.shop. 
- This indicates the server enforces a domain check during registration.
- Investigate encoding discrepancies
- Try to register an account with the following email:
```
=?iso-8859-1?q?=61=62=63?=foo@ginandjuice.shop.
```
- This is the email abcfoo@ginandjuice.shop, with the abc portion encoded using Q encoding, which is part of the "encoded-word" standard.
- Notice that the registration is blocked with the error: "Registration blocked for security reasons."
- Try to register an account with the following UTF-8 encoded email:
```
=?utf-8?q?=61=62=63?=foo@ginandjuice.shop.
```
- Notice that the registration is blocked with the same error message. 
- This suggests that the server is detecting and rejecting attempts to manipulate the registration email with encoded word encoding. 
- It is possible that less common encoding formats may not be picked up by the server's validation.
- Try to register an account with the following UTF-7 encoded email:
```
=?utf-7?q?&AGEAYgBj-?=foo@ginandjuice.shop.
```
- Notice that this attempt doesn't trigger an error. 
- This suggests that the server doesn't recognize UTF-7 encoding as a security threat. 
- Because UTF-7 encoding appears to bypass the server's validation, you may be able to use it to craft an attack that tricks the server into sending a confirmation email to your exploit server email address while appearing to still satisfy the ginandjuice.shop domain requirement.

2. # Exploit the vulnerability using UTF-7
- Register an account with the following UTF-7 encoded email:
```
=?utf-7?q?attacker&AEA-[YOUR-EXPLOIT-SERVER_ID]&ACA-?=@ginandjuice.shop.
```
- This is the string attacker@[YOUR-EXPLOIT-SERVER-ID] ?=@ginandjuice.shop, with the @ symbol and space encoded in UTF-7.
- Click Email client. Notice that you have been sent a registration validation email. This is because the encoded email address has passed validation due to the @ginandjuice.shop portion at the end, but the email server has interpreted the registration email as attacker@[YOUR-EXPLOIT-SERVER-ID].
- Click the confirmation link to activate the account.

3. # Gain admin access
- Click My account and log in using the details you registered.
- Click Admin panel to access the list of users.
- Delete the carlos user to solve the lab.