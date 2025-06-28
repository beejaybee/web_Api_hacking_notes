Sites often use HTTP or URL parameters to redirect users to a specified URL without any user action. While this behavior can be useful, it can also cause open redirects, which happen when an attacker is able to manipulate the value of this parameter to redirect the user offsite.


# MECHANISMS
- Websites often need to automatically redirect their users. For example, this scenario commonly occurs when unauthenticated users try to access a page that requires logging in. The website will usually redirect those users to the login page, and then return them to their original location after they’re authenticated.
- For example, when these users visit their account dashboards at https://example.com/dashboard, the application might redirect them to the login page at https://example.com/login.
- To later redirect users to their previous location, the site needs to remember which page they intended to access before they were redirected to the login page. 
- Therefore, the site uses some sort of redirect URL parameter appended to the URL to keep track of the user’s original location. This 
parameter determines where to redirect the user after login. 
For example, the URL https://example.com/login?redirect=https://example.com/dashboard will redirect to the user’s dashboard, located at https://example.com/dashboard, after login. 
- Or if the user was originally trying to browse their account settings page, the site would redirect the user to the settings page after login, and the URL would look like this: https://example.com/login?redirect=https://example.com/settings. 
- Redirecting users automatically saves them time and improves their experience, so you’ll find many applications that implement this functionality.
- During an open-redirect attack, an attacker tricks the user into visiting an external site by providing them with a URL from the legitimate site that redirects somewhere else, like this: https://example.com/login?redirect=https://attacker.com. 
- A URL like this one could trick victims into clicking the link, because they’ll believe it leads to a page on the legitimate site,example.com. 
- But in reality, this page automatically redirects to a malicious page. 
- Attackers can then launch a social engineering attack and trick users into entering their example.com credentials on the attacker’s site. 


# Hunting for open-redirects
You can find open redirects by using a few recon tricks to discover vulnerable endpoints and confirm the open redirect manually.

## STEP 1: LOOK FOR REDIRECT PARAMETERS

- Start by searching for the parameters used for redirects. These often show up as URL parameters like the ones in below here:
```code
https://example.com/login?redirect=https://example.com/dashboard
https://example.com/login?redir=https://example.com/dashboard
https://example.com/login?next=https://example.com/dashboard
https://example.com/login?next=/dashboard
```
- Open your proxy while you browse the website. Then, in your HTTP history, look for any parameter that contains absolute or relative URLs. 
- An absolute URL is complete and contains all the components necessary to locate the resource it points to, like https://example.com/login. 
- Absolute URLs contain at least the URL scheme, hostname, and path of a resource. 
- A relative URL must be concatenated with another URL by the server in order to be ussed.
- These typically contain only the path component of a URL, like /login. 
- Some redirect URLs will even omit the first slash (/) character of the relative URL, as in https://example.com/login?next=dashboard
- Note that not all redirect parameters have straightforward names like redirect or redir. 
- For example, I’ve seen redirect parameters named RelayState, next, u, n, and forward. 
- You should record all parameters that seem to be used for redirect, regardless of their parameter names.
- In addition, take note of the pages that don’t contain redirect parameters in their URLs but still automatically redirect their users.
- These pages are candidates for referer-based open redirects. 
- To find these pages, you can keep an eye out for 3XX response codes like 301 and 302. 
- These response codes indicate a redirect.

## STEP 2: USE GOOGLE DORKS TO FIND ADDITIONAL REDIRECT PARAMETERS

- Google dork techniques are an efficient way to find redirect parameters. 
- To look for redirect parameters on a target site by using Google dorks, start by setting the site search term to your target site:
```site:example.com```
- Then look for pages that contain URLs in their URL parameters, making use of %3D, the URL-encoded version of the equal sign (=). 
By adding %3D in your search term, you can search for terms like =http and =https, which are indicators of URLs in a parameter. 
- The following searches for URL parameters that contain absolute URLs:
```code
inurl:%3Dhttp site:example.com
```
- Also try using %2F, the URL-encoded version of the slash (/). 
- The following search term searches URLs that contain =/, and therefore returns URL parameters that contain relative URLs:
```
inurl:%3D%2F site:example.com
```
- This search term will find URLs such as this one: ```https://example.com/login?n=/dashboard```
- Alternatively, you can search for the names of common URL redirect parameters. 
- Here are a few search terms that will likely reveal parameters used for a redirect:
```code
inurl:redir site:example.com
inurl:redirect site:example.com
inurl:redirecturi site:example.com
inurl:redirect_uri site:example.com
inurl:redirecturl site:example.com
inurl:redirect_uri site:example.com
inurl:return site:example.com
inurl:returnurl site:example.com
inurl:relaystate site:example.com
inurl:forward site:example.com
inurl:forwardurl site:example.com
inurl:forward_url site:example.com
inurl:url site:example.com
inurl:uri site:example.com
inurl:dest site:example.com
inurl:destination site:example.com
inurl:next site:example.com
```
- Note the new parameters you’ve discovered, along with the ones found in step 1.

## STEP 3: TEST FOR PARAMETER-BASED OPEN REDIRECT
- Next, pay attention to the functionality of each redirect parameter you’ve found and test each one for an open redirect. 
- Insert a random hostname, or a hostname you own, into the redirect parameters; then see if the site automatically redirects to the site you specified:
```
https://example.com/login?n=http://google.com
https://example.com/login?n=http://attacker.com
```
- Some sites will redirect to the destination site immediately after you visit the URL, without any user interaction. 
- But for a lot of pages, the redirect won’t happen until after a user action, like registration, login, or logout. 
- In those cases, be sure to carry out the required user interactions before checking for the redirect.

## STEP 4: TEST FOR REFERER-BASED OPEN REDIRECT
- Finally, test for referer-based open redirects on any pages you found in step 1 that redirected users despite not containing a redirect URL parameter. 
To test for these, set up a page on a domain you own and host this HTML page:
```
<html>
 <a href="https://example.com/login">Click on this link!</a>
</html>
```
- Replace the linked URL with the target page. 
- Then reload and visit your HTML page. 
- Click the link and see if you get redirected to your site automatically or after the required user interactions.


# BYPASSING OPEN REDIRECT PROTECTION
- Here, you can see the components of a URL. The way the browser redirects the user depends on how the browser differentiates between these components:
```
scheme://userinfo@hostname:port/path?query#fragment
```
- The URL validator needs to predict how the browser will redirect the user and reject URLs that will result in a redirect offsite. 
- Browsers redirect users to the location indicated by the hostname section of the URL. 
However, URLs don’t always follow the strict format shown in this example. 
They can be malformed, have their components out of order, contain characters that the browser does not know how to decode, or have extra or missing components. 
- For example, how would the browser redirect this URL? https://user:password:8080/example.com@attacker.com
- When you visit this link in different browsers, you will see that different browsers handle this URL differently. 
- Sometimes validators don’t account for all the edge cases that can cause the browser to behave unexpectedly. 
- In this case, you could try to bypass the protection by using a few strategies 

## Using Browser Autocorrect
- First, you can use browser autocorrect features to construct alternative URLs that redirect offsite. 
- Modern browsers often autocorrect URLs that don’t have the correct components, in order to correct mangled URLs caused by user typos. 
- For example, Chrome will interpret all of these URLs as pointing to https://attacker.com:
```
https:attacker.com
https;attacker.com
https:\/\/attacker.com
https:/\/\attacker.com
```
- 
