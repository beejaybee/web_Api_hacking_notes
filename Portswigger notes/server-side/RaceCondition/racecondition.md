# Race conditions
- Race conditions are a common type of vulnerability closely related to business logic flaws. 
- They occur when websites process requests concurrently without adequate safeguards. 
- This can lead to multiple distinct threads interacting with the same data at the same time, resulting in a "collision" that causes unintended behavior in the application. 
- A race condition attack uses carefully timed requests to cause intentional collisions and exploit this unintended behavior for malicious purposes.
- The period of time during which a collision is possible is known as the "race window". 
- This could be the fraction of a second between two interactions with the database, for example.
- Like other logic flaws, the impact of a race condition is heavily dependent on the application and the specific functionality in which it occurs.
- In this section, I'll learn how to identify and exploit different types of race condition. 
- I'll learn how Burp Suite's built-in tooling can help me to overcome the challenges of performing classic attacks, plus a tried and tested methodology that enables me to detect novel classes of race condition in hidden multi-step processes. 
- These go far beyond the limit overruns that I may be familiar with already.

# Limit overrun race conditions
- The most well-known type of race condition enables you to exceed some kind of limit imposed by the business logic of the application.
- For example, consider an online store that lets you enter a promotional code during checkout to get a one-time discount on your order. 
- To apply this discount, the application may perform the following high-level steps:
1. Check that you haven't already used this code.
2. Apply the discount to the order total.
3. Update the record in the database to reflect the fact that you've now used this code.

- There are many variations of this kind of attack, including:

- Redeeming a gift card multiple times
- Rating a product multiple times
- Withdrawing or transferring cash in excess of your account balance
- Reusing a single CAPTCHA solution
- Bypassing an anti-brute-force rate limit
- Limit overruns are a subtype of so-called "time-of-check to time-of-use" (TOCTOU) flaws. 

- Later in this topic, we'll look at some examples of race condition vulnerabilities that don't fall into either of these categories.

# Detecting and exploiting limit overrun race conditions with Burp Repeater
- The process of detecting and exploiting limit overrun race conditions is relatively simple. 
- In high-level terms, all you need to do is:
- Identify a single-use or rate-limited endpoint that has some kind of security impact or other useful purpose.
- Issue multiple requests to this endpoint in quick succession to see if you can overrun this limit.
- The primary challenge is timing the requests so that at least two race windows line up, causing a collision. 
- This window is often just milliseconds and can be even shorter.
- Even if you send all of the requests at exactly the same time, in practice there are various uncontrollable and unpredictable external factors that affect when the server processes each request and in which order.

- Burp Suite 2023.9 adds powerful new capabilities to Burp Repeater that enable you to easily send a group of parallel requests in a way that greatly reduces the impact of one of these factors, namely network jitter. 
- Burp automatically adjusts the technique it uses to suit the HTTP version supported by the server:
- For HTTP/1, it uses the classic last-byte synchronization technique.
- For HTTP/2, it uses the single-packet attack technique, first demonstrated by PortSwigger Research at Black Hat USA 2023.
- The single-packet attack enables you to completely neutralize interference from network jitter by using a single TCP packet to complete 20-30 requests simultaneously.
- Although you can often use just two requests to trigger an exploit, sending a large number of requests like this helps to mitigate internal latency, also known as server-side jitter. 
- This is especially useful during the initial discovery phase. 
- We'll cover this methodology in more detail.

# Lab: Limit overrun race conditions
- This lab's purchasing flow contains a race condition that enables you to purchase items for an unintended price.
- To solve the lab, successfully purchase a Lightweight L33t Leather Jacket.
- You can log in to your account with the following credentials: wiener:peter.
# Solution From the Lab
- Predict a potential collision
    - Log in and buy the cheapest item possible, making sure to use the provided discount code so that you can study the purchasing flow.
    - Consider that the shopping cart mechanism and, in particular, the restrictions that determine what you are allowed to order, are worth trying to bypass.
    - In Burp, from the proxy history, identify all endpoints that enable you to interact with the cart. 
    - For example, a POST /cart request adds items to the cart and a POST /cart/coupon request applies the discount code.
    - Try to identify any restrictions that are in place on these endpoints. 
    - For example, observe that if you try applying the discount code more than once, you receive a Coupon already applied response.
    - Make sure you have an item to your cart, then send the GET /cart request to Burp Repeater.
    - In Repeater, try sending the GET /cart request both with and without your session cookie. 
    - Confirm that without the session cookie, you can only access an empty cart. From this, you can infer that:
    - The state of the cart is stored server-side in your session.
    - Any operations on the cart are keyed on your session ID or the associated user ID.
    - This indicates that there is potential for a collision.
    - Consider that there may be a race window between when you first apply a discount code and when the database is updated to reflect that you've done this already.
- Benchmark the behavior
    - Make sure there is no discount code currently applied to your cart.
    - Send the request for applying the discount code (POST /cart/coupon) to Repeater.
    - In Repeater, send the POST /cart/coupon request twice.
    - Observe that the first response confirms that the discount was successfully applied, but the second response rejects the code with the same Coupon already applied message.
- Probe for clues
    - Remove the discount code from your cart.

    - In Repeater, open the Custom actions side panel.

    - Click New > From template, then select Trigger race condition.

    - Save the template to the Custom actions side panel without making any modifications.

    - Click  beside the Trigger race condition custom action. The request is sent 20 times in parallel.

    - In the browser, refresh your cart and confirm that the 20% reduction has been applied more than once, resulting in a significantly cheaper order

# Detecting and exploiting limit overrun race conditions with Turbo Intruder
- In addition to providing native support for the single-packet attack in Burp Repeater, we've also enhanced the Turbo Intruder extension to support this technique. 
- You can download the latest version from the BApp Store.
- Turbo Intruder requires some proficiency in Python, but is suited to more complex attacks, such as ones that require multiple retries, staggered request timing, or an extremely large number of requests.
- To use the single-packet attack in Turbo Intruder:
- Ensure that the target supports HTTP/2. The single-packet attack is incompatible with HTTP/1.
- Set the engine=Engine.BURP2 and concurrentConnections=1 configuration options for the request engine.
- When queueing your requests, group them by assigning them to a named gate using the gate argument for the engine.queue() method.
- To send all of the requests in a given group, open the respective gate with the engine.openGate() method.
```
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                            concurrentConnections=1,
                            engine=Engine.BURP2
                            )
    
    # queue 20 requests in gate '1'
    for i in range(20):
        engine.queue(target.req, gate='1')
    
    # send all requests in gate '1' in parallel
    engine.openGate('1')
```

# Lab: Bypassing rate limits via race conditions
- This lab's login mechanism uses rate limiting to defend against brute-force attacks. However, this can be bypassed due to a race condition.
- To solve the lab:
    - Work out how to exploit the race condition to bypass the rate limit.
    - Successfully brute-force the password for the user carlos.
    - Log in and access the admin panel.
    - Delete the user carlos.

# Solving the lab
- Try to login to carlos account and notice that there is a rate limit in place
- Send the POST login request and send the request to burp intruder
- Use the code below in burp turbo intruder
- Change the password value in the request with %s
- Start the attack and check response

```
def queueRequests(target, wordlists):

    # if the target supports HTTP/2, use engine=Engine.BURP2 to trigger the single-packet attack
    # if they only support HTTP/1, use Engine.THREADED or Engine.BURP instead
    # for more information, check out https://portswigger.net/research/smashing-the-state-machine
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=1,
                           engine=Engine.BURP2
                           )

    # the 'gate' argument withholds part of each request until openGate is invoked
    # if you see a negative timestamp, the server responded before the request was complete
    passwords = [p.strip() for p in open('/home/kali/password', 'r').readlines()]
    
    for password in passwords:
        engine.queue(target.req, password, gate='1')
    # once every 'race1' tagged request has been queued
    # invoke engine.openGate() to send them in sync
    engine.openGate('1')


def handleResponse(req, interesting):
    table.add(req)

```

# Hidden multi-step sequences
- In practice, a single request may initiate an entire multi-step sequence behind the scenes, transitioning the application through multiple hidden states that it enters and then exits again before request processing is complete. 
- We'll refer to these as "sub-states".
- If you can identify one or more HTTP requests that cause an interaction with the same data, you can potentially abuse these sub-states to expose time-sensitive variations of the kinds of logic flaws that are common in multi-step workflows. 
- This enables race condition exploits that go far beyond limit overruns.
- For example, you may be familiar with flawed multi-factor authentication (MFA) workflows that let you perform the first part of the login using known credentials, then navigate straight to the application via forced browsing, effectively bypassing MFA entirely.
- The following pseudo-code demonstrates how a website could be vulnerable to a race variation of this attack:

```
    session['userid'] = user.userid
    if user.mfa_enabled:
    session['enforce_mfa'] = True
    # generate and send MFA code to user
    # redirect browser to MFA code entry form
```
- As you can see, this is in fact a multi-step sequence within the span of a single request. 
- Most importantly, it transitions through a sub-state in which the user temporarily has a valid logged-in session, but MFA isn't yet being enforced. 
- An attacker could potentially exploit this by sending a login request along with a request to a sensitive, authenticated endpoint


# Methodology
- To detect and exploit hidden multi-step sequences, the following is recommended
1. Predict
2. Probe
3. Prove

# Predict potential collisions
- Testing every endpoint is impractical. 
- After mapping out the target site as normal, you can reduce the number of endpoints that you need to test by asking yourself the following questions:

- Is this endpoint security critical? Many endpoints don't touch critical functionality, so they're not worth testing.
- Is there any collision potential? For a successful collision, you typically need two or more requests that trigger operations on the same record. 
- For example, consider the following variations of a password reset implementation:
        session=b94 userid=hacker   ---> hackerToken
        session=b94 userid=victim   ---> victimToken

        session=b94 userid=hacker   -\------\  sessionid userid token 
        session=b94 userid=victim   -/------/     b94     ???     ???

- With the first example, requesting parallel password resets for two different users is unlikely to cause a collision as it results in changes to two different records. 
- However, the second implementation enables you to edit the same record with requests for two different users.

# Probe for clues
- To recognize clues, you first need to benchmark how the endpoint behaves under normal conditions. 
- You can do this in Burp Repeater by grouping all of your requests and using the Send group in sequence (separate connections) option.
- Next, send the same group of requests at once using the single-packet attack (or last-byte sync if HTTP/2 isn't supported) to minimize network jitter. 
- You can do this in Burp Repeater by selecting the Send group in parallel option. 
- Alternatively, you can use the Turbo Intruder extension.
- Anything at all can be a clue. 
- Just look for some form of deviation from what you observed during benchmarking. 
- This includes a change in one or more responses, but don't forget second-order effects like different email contents or a visible change in the application's behavior afterward.



# Prove the concept
- Try to understand what's happening, remove superfluous requests, and make sure you can still replicate the effects.
- Advanced race conditions can cause unusual and unique primitives, so the path to maximum impact isn't always immediately obvious. 
- It may help to think of each race condition as a structural weakness rather than an isolated vulnerability.

# Multi-endpoint race conditions
- Perhaps the most intuitive form of these race conditions are those that involve sending requests to multiple endpoints at the same time.
- Think about the classic logic flaw in online stores where you add an item to your basket or cart, pay for it, then add more items to the cart before force-browsing to the order confirmation page.
- A variation of this vulnerability can occur when payment validation and order confirmation are performed during the processing of a single request.

# Aligning multi-endpoint race windows
- When testing for multi-endpoint race conditions, you may encounter issues trying to line up the race windows for each request, even if you send them all at exactly the same time using the single-packet technique.
- This common problem is primarily caused by the following two factors:
- Delays introduced by network architecture - For example, there may be a delay whenever the front-end server establishes a new connection to the back-end. 
- The protocol used can also have a major impact.
- Delays introduced by endpoint-specific processing - Different endpoints inherently vary in their processing times, sometimes significantly so, depending on what operations they trigger.
- Fortunately, there are potential workarounds to both of these issues.

# Connection warming
- Back-end connection delays don't usually interfere with race condition attacks because they typically delay parallel requests equally, so the requests stay in sync.
- It's essential to be able to distinguish these delays from those caused by endpoint-specific factors. 
- One way to do this is by "warming" the connection with one or more inconsequential requests to see if this smoothes out the remaining processing times. 
- In Burp Repeater, you can try adding a GET request for the homepage to the start of your tab group, then using the Send group in sequence (single connection) option.
- If the first request still has a longer processing time, but the rest of the requests are now processed within a short window, you can ignore the apparent delay and continue testing as normal.

# Lab: Multi-endpoint race conditions
- This lab's purchasing flow contains a race condition that enables you to purchase items for an unintended price.
- To solve the lab, successfully purchase a Lightweight L33t Leather Jacket.
- You can log into your account with the following credentials: wiener:peter.

# Solution
- Predict a potential collision
    - Log in and purchase a gift card so you can study the purchasing flow.
    - Consider that the shopping cart mechanism and, in particular, the restrictions that determine what you are allowed to order, are worth trying to bypass.
    - From the proxy history, identify all endpoints that enable you to interact with the cart. For example, a POST /cart request adds items to the cart and a POST /cart/checkout request submits your order.
    - Add another gift card to your cart, then send the GET /cart request to Burp Repeater.
    - In Repeater, try sending the GET /cart request both with and without your session cookie. 
    - Confirm that without the session cookie, you can only access an empty cart. From this, you can infer that:
        - The state of the cart is stored server-side in your session.
        - Any operations on the cart are keyed on your session ID or the associated user ID.
        - This indicates that there is potential for a collision.

    - Notice that submitting and receiving confirmation of a successful order takes place over a single request/response cycle.
    - Consider that there may be a race window between when your order is validated and when it is confirmed. 
    - This could enable you to add more items to the order after the server checks whether you have enough store credit.


# Benchmark the behavior
- Send both the POST /cart and POST /cart/checkout request to Burp Repeater.
- In Repeater, add the two tabs to a new group. For details on how to do this, see Creating a new tab group
- Send the two requests in sequence over a single connection a few times. 
- Notice from the response times that the first request consistently takes significantly longer than the second one. 
- For details on how to do this, see Sending requests in sequence.
- Add a GET request for the homepage to the start of your tab group.
- Send all three requests in sequence over a single connection. 
- Observe that the first request still takes longer, but by "warming" the connection in this way, the second and third requests are now completed within a much smaller window.
- Deduce that this delay is caused by the back-end network architecture rather than the respective processing time of the each endpoint. 
- Therefore, it is not likely to interfere with your attack.
- Remove the GET request for the homepage from your tab group.
- Make sure you have a single gift card in your cart.
- In Repeater, modify the POST /cart request in your tab group so that the productId parameter is set to 1, that is, the ID of the Lightweight L33t Leather Jacket.
- Send the requests in sequence again.
- Observe that the order is rejected due to insufficient funds, as you would expect.

# Prove the concept
- Remove the jacket from your cart and add another gift card.
- In Repeater, try sending the requests again, but this time in parallel. 
- Look at the response to the POST /cart/checkout request:
- If you received the same "insufficient funds" response, remove the jacket from your cart and repeat the attack. 
- This may take several attempts.
- If you received a 200 response, check whether you successfully purchased the leather jacket. If so, the lab is solved.

# After solving the lab
- If you still see inconsistent response times on a single endpoint, even when using the single-packet technique, this is an indication that the back-end delay is interfering with your attack. 
- You may be able to work around this by using Turbo Intruder to send some connection warming requests before following up with your main attack requests.

# Abusing rate or resource limits
- If connection warming doesn't make any difference, there are various solutions to this problem.
- Using Turbo Intruder, you can introduce a short client-side delay. 
- However, as this involves splitting your actual attack requests across multiple TCP packets, you won't be able to use the single-packet attack technique. 
- As a result, on high-jitter targets, the attack is unlikely to work reliably regardless of what delay you set.
- Instead, you may be able to solve this problem by abusing a common security feature.
- Web servers often delay the processing of requests if too many are sent too quickly. 
- By sending a large number of dummy requests to intentionally trigger the rate or resource limit, you may be able to cause a suitable server-side delay. 
- This makes the single-packet attack viable even when delayed execution is required.

# Single-endpoint race conditions
- Sending parallel requests with different values to a single endpoint can sometimes trigger powerful race conditions.
- Consider a password reset mechanism that stores the user ID and reset token in the user's session.
- In this scenario, sending two parallel password reset requests from the same session, but with two different usernames, could potentially cause the following collision:
https://portswigger.net/web-security/race-conditions/images/race-conditions-password-reset-collision.png

- Note the final state when all operations are complete:
```
session['reset-user'] = victim
session['reset-token'] = 1234
```
- The session now contains the victim's user ID, but the valid reset token is sent to the attacker.
- Note
    - For this attack to work, the different operations performed by each process must occur in just the right order. 
    - It would likely require multiple attempts, or a bit of luck, to achieve the desired outcome.

- Email address confirmations, or any email-based operations, are generally a good target for single-endpoint race conditions. 
- Emails are often sent in a background thread after the server issues the HTTP response to the client, making race conditions more likely.

# Lab: Single-endpoint race conditions
- This lab's email change feature contains a race condition that enables you to associate an arbitrary email address with your account.
- Someone with the address carlos@ginandjuice.shop has a pending invite to be an administrator for the site, but they have not yet created an account. Therefore, any user who successfully claims this address will automatically inherit admin privileges.
- To solve the lab:
- Identify a race condition that lets you claim an arbitrary email address.
- Change your email address to carlos@ginandjuice.shop.
- Access the admin panel.
- Delete the user carlos

# Predict a potential collision
- Log in and attempt to change your email to anything@exploit-<YOUR-EXPLOIT-SERVER-ID>.exploit-server.net. 
- Observe that a confirmation email is sent to your intended new address, and you're prompted to click a link containing a unique token to confirm the change.
- Complete the process and confirm that your email address has been updated on your account page.
- Try submitting two different @exploit-<YOUR-EXPLOIT-SERVER-ID>.exploit-server.net email addresses in succession, then go to the email client.
- Notice that if you try to use the first confirmation link you received, this is no longer valid. From this, you can infer that the website only stores one pending email address at a time. 
- As submitting a new email address edits this entry in the database rather than appending to it, there is potential for a collision.

# Benchmark the behavior
- Send the POST /my-account/change-email request to Repeater.
- In Repeater, add the new tab to a group. 
- Right-click the grouped tab, then select Duplicate tab. Create 19 duplicate tabs. The new tabs are automatically added to the group.
- In each tab, modify the first part of the email address so that it is unique to each request, for example, test1@exploit-<YOUR-EXPLOIT-SERVER-ID>.exploit-server.net, test2@..., test3@... and so on.
- Send the group of requests in sequence over separate connections. 
- Go back to the email client and observe that you have received a single confirmation email for each of the email change requests.

# Benchmark the behavior
- Send the POST /my-account/change-email request to Repeater.
- In Repeater, add the new tab to a group. For details on how to do this, see Creating a new tab group.
- Right-click the grouped tab, then select Duplicate tab. Create 19 duplicate tabs. 
- The new tabs are automatically added to the group.
- In each tab, modify the first part of the email address so that it is unique to each request, for example, test1@exploit-<YOUR-EXPLOIT-SERVER-ID>.exploit-server.net, test2@..., test3@... and so on.
- Send the group of requests in sequence over separate connections. 
- Go back to the email client and observe that you have received a single confirmation email for each of the email change requests.

# Prove the concept
- In Repeater, create a new group containing two copies of the POST /my-account/change-email request.
- Change the email parameter of one request to anything@exploit-<YOUR-EXPLOIT-SERVER-ID>.exploit-server.net.
- Change the email parameter of the other request to carlos@ginandjuice.shop.
- Send the requests in parallel.
- Check your inbox:
- If you received a confirmation email in which the address in the body matches your own address, resend the requests in parallel and try again.
- If you received a confirmation email in which the address in the body is carlos@ginandjuice.shop, click the confirmation link to update your address accordingly.
- Go to your account page and notice that you now see a link for accessing the admin panel.
- Visit the admin panel and delete the user carlos to solve the lab.

#  Session-based locking mechanisms
- Some frameworks attempt to prevent accidental data corruption by using some form of request locking. 
- For example, PHP's native session handler module only processes one request per session at a time.
- It's extremely important to spot this kind of behavior as it can otherwise mask trivially exploitable vulnerabilities. 
- If you notice that all of your requests are being processed sequentially, try sending each of them using a different session token.

# Partial construction race conditions
- Many applications create objects in multiple steps, which may introduce a temporary middle state in which the object is exploitable.
- For example, when registering a new user, an application may create the user in the database and set their API key using two separate SQL statements. This leaves a tiny window in which the user exists, but their API key is uninitialized.
- This kind of behavior paves the way for exploits whereby you inject an input value that returns something matching the uninitialized database value, such as an empty string, or null in JSON, and this is compared as part of a security control.
- Frameworks often let you pass in arrays and other non-string data structures using non-standard syntax. For example, in PHP:
```
param[]=foo is equivalent to param = ['foo']
param[]=foo&param[]=bar is equivalent to param = ['foo', 'bar']
param[] is equivalent to param = []
```
- Ruby on Rails lets you do something similar by providing a query or POST parameter with a key but no value. 
- In other words ```param[key]``` results in the following server-side object:

```
    params = {"param"=>{"key"=>nil}}
``` 
- In the example above, this means that during the race window, you could potentially make authenticated API requests as follows:
```

    GET /api/user/info?user=victim&api-key[]= HTTP/2
    Host: vulnerable-website.com
``` 
- Note
    - It's possible to cause similar partial construction collisions with a password rather than an API key. 
    - However, as passwords are hashed, this means you need to inject a value that makes the hash digest match the uninitialized value.

# Lab: Partial construction race conditions
- This lab contains a user registration mechanism. A race condition enables you to bypass email verification and register with an arbitrary email address that you do not own.
- To solve the lab, exploit this race condition to create an account, then log in and delete the user carlos.

# SOLUTION
# Predict a potential collision
- Study the user registration mechanism. Observe that:
- You can only register using @ginandjuice.shop email addresses.
- To complete the registration, you need to visit the confirmation link, which is sent via email.
- As you don't have access to an @ginandjuice.shop email account, you don't appear to have a way to access a valid confirmation link.
- In Burp, from the proxy history, notice that there is a request to fetch /resources/static/users.js.
- Study the JavaScript and notice that this dynamically generates a form for the confirmation page, which is presumably linked from the confirmation email. This leaks the fact that the final confirmation is submitted via a POST request to /confirm, with the token provided in the query string.
- In Burp Repeater, create an equivalent request to what your browser might send when clicking the confirmation link. For example:
```HTTP
POST /confirm?token=1 HTTP/2
Host: YOUR-LAB-ID.web-security-academy.net
Content-Type: x-www-form-urlencoded
Content-Length: 0
```
- Experiment with the token parameter in your newly crafted confirmation request. Observe that:

    - If you submit an arbitrary token, you receive an Incorrect token: <YOUR-TOKEN> response.
    - If you remove the parameter altogether, you receive a Missing parameter: token response.
    - If you submit an empty token parameter, you receive a Forbidden response.
- Consider that this Forbidden response may indicate that the developers have patched a vulnerability that could be exploited by sending an empty token parameter.
- Consider that there may be a small race window between:
- When you submit a request to register a user.
- When the newly generated registration token is actually stored in the database.
- If so, there may be a temporary sub-state in which null (or equivalent) is a valid token for confirming the user's registration.
- Experiment with different ways of submitting a token parameter with a value equivalent to null. For example, some frameworks let you to pass an empty array as follows:
```POST /confirm?token[]=```
- Observe that this time, instead of the Forbidden response, you receive an Invalid token: Array response. 
- This shows that you've successfully passed in an empty array, which could potentially match an uninitialized registration token.

# Benchmark the behavior
- Send the POST /register request to Burp Repeater.
- In Burp Repeater, experiment with the registration request. 
- Observe that if you attempt to register the same username more than once, you get a different response.
- In a separate Repeater tab, use what you've learned from the JavaScript import to construct a confirmation request with an arbitrary token. For example:
```

    POST /confirm?token=1 HTTP/2
    Host: YOUR-LAB-ID.web-security-academy.net
    Cookie: phpsessionid=YOUR-SESSION-ID
    Content-Type: application/x-www-form-urlencoded
    Content-Length: 0
```                         
- Add both requests to a new tab group.
- Try sending both requests sequentially and in parallel several times, making sure to change the username in the registration request each time to avoid hitting the separate Account already exists with this name code path.
- Notice that the confirmation response consistently arrives much quicker than the response to the registration request.

# Prove the concept
- Note that you need the server to begin creating the pending user in the database, then compare the token you send in the confirmation request before the user creation is complete.
- Consider that as the confirmation response is always processed much more quickly, you need to delay this so that it falls within the race window.
- In the POST /register request, highlight the value of the username parameter, then right-click and select Extensions > Turbo Intruder > Send to turbo intruder.
- In Turbo Intruder, in the request editor:
- Notice that the value of the username parameter is automatically marked as a payload position with the %s placeholder.
- Make sure the email parameter is set to an arbitrary @ginandjuice.shop address that is not likely to already be registered on the site.
- Make a note of the static value of the password parameter. You'll need this later.
- From the drop-down menu, select the examples/race-single-packet-attack.py template.
- In the Python editor, modify the main body of the template as follows:
- Define a variable containing the confirmation request you've been testing in Repeater.
- Create a loop that queues a single registration request using a new username for each attempt. Set the gate argument to match the current iteration.
- Create a nested loop that queues a large number of confirmation requests for each attempt. These should also use the same release gate.
- Open the gate for all the requests in each attempt at the same time.
- The resulting script should look something like this:
```
def queueRequests(target, wordlists):

    engine = RequestEngine(endpoint=target.endpoint,
                            concurrentConnections=1,
                            engine=Engine.BURP2
                            )
    
    confirmationRequest = '''POST /confirm?token[]= HTTP/2
Host: YOUR-LAB-ID.web-security-academy.net
Cookie: phpsessionid=YOUR-SESSION-TOKEN
Content-Length: 0

'''
    for attempt in range(20):
        currentAttempt = str(attempt)
        username = 'Beejay' + currentAttempt
    
        # queue a single registration request
        engine.queue(target.req, username, gate=currentAttempt)
        
        # queue 50 confirmation requests - note that this will probably sent in two separate packets
        for i in range(50):
            engine.queue(confirmationReq, gate=currentAttempt)
        
        # send all the queued requests for this attempt
        engine.openGate(currentAttempt)

def handleResponse(req, interesting):
    table.add(req)
```
- Launch the attack.
- In the results table, sort the results by the Length column.
- If the attack was successful, you should see one or more 200 responses to your confirmation request containing the message Account registration for user ```<USERNAME>``` successful.
- Make a note of the username from one of these responses. If you used the example script above, this will be something like User4.
- In the browser, log in using this username and the static password you used in the registration request.
- Access the admin panel and delete carlos to solve the lab.


# Time-sensitive attacks
- Sometimes you may not find race conditions, but the techniques for delivering requests with precise timing can still reveal the presence of other vulnerabilities.
- One such example is when high-resolution timestamps are used instead of cryptographically secure random strings to generate security tokens.
- Consider a password reset token that is only randomized using a timestamp. 
- In this case, it might be possible to trigger two password resets for two different users, which both use the same token. 
- All you need to do is time the requests so that they generate the same timestamp.

# Lab: Exploiting time-sensitive vulnerabilities
- This lab contains a password reset mechanism. 
- Although it doesn't contain a race condition, you can exploit the mechanism's broken cryptography by sending carefully timed requests.
- To solve the lab:
- Identify the vulnerability in the way the website generates password reset tokens.
- Obtain a valid password reset token for the user carlos.
- Log in as carlos.
- Access the admin panel and delete the user carlos.
- You can log into your account with the following credentials: wiener:peter.

# Solution
- Study the behavior
    1. Study the password reset process by submitting a password reset for your own account and observe that you're sent an email containing a reset link. The query string of this link includes your username and a token.

    2. Send the POST /forgot-password request to Burp Repeater.

    3. In Repeater, send the request a few times, then check your inbox again.

    4. Observe that every reset request results in a link with a different token.

    - Consider the following:

        1. The token is of a consistent length. This suggests that it's either a randomly generated string with a fixed number of characters, or could be a hash of some unknown data, which may be predictable.
        2. The fact that the token is different each time indicates that, if it is in fact a hash digest, it must contain some kind of internal state, such as an RNG, a counter, or a timestamp.
    
    5. Duplicate the Repeater tab and add both tabs to a new group. 

    6. Send the pair of reset requests in parallel a few times. 
    7. Observe that there is still a significant delay between each response and that you still get a different token in each confirmation email. Infer that your requests are still being processed in sequence rather than concurrently.

- Bypass the per-session locking restriction
    1. Notice that your session cookie suggests that the website uses a PHP back-end. This could mean that the server only processes one request at a time per session.
    2. Send the GET /forgot-password request to Burp Repeater, remove the session cookie from the request, then send it.
    3. From the response, copy the newly issued session cookie and CSRF token and use them to replace the respective values in one of the two POST /forgot-password requests. You now have a pair of password reset requests from two different sessions.
    4. Send the two POST requests in parallel a few times and observe that the processing times are now much more closely aligned, and sometimes identical.

- Confirm the vulnerability
    1. Go back to your inbox and notice that when the response times match for the pair of reset requests, this results in two confirmation emails that use an identical token. This confirms that a timestamp must be one of the inputs for the hash.

    2. Consider that this also means the token would be predictable if you knew the other inputs for the hash function.

    3. Notice the separate username parameter. This suggests that the username might not be included in the hash, which means that two different usernames could theoretically have the same token.

    4. In Repeater, go to the pair of POST /forgot-password requests and change the username parameter in one of them to carlos.

    5. Resend the two requests in parallel. If the attack worked, both users should be assigned the same reset token, although you won't be able to see this.

    6. Check your inbox again and observe that, this time, you've only received one new confirmation email. Infer that the other email, hopefully containing the same token, has been sent to Carlos.

    7. Copy the link from the email and change the username in the query string to carlos.

    8. Visit the URL in the browser and observe that you're taken to the form for setting a new password as normal.

    9. Set the password to something you'll remember and submit the form.

    10. Try logging in as carlos using the password you just set.

    11. If you can't log in, resend the pair of password reset emails and repeat the process.
    12. If you successfully log in, visit the admin panel and delete the user carlos to solve the lab.