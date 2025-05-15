# INTRO

Server-Side Request Forgery (SSRF) is a vulnerability that takes place when an application retrieves remote resources without validating user input. An attacker can supply their own input, in the form of a URL, to control the remote resources that are retrieved by the targeted server. When you have control over what resources a server requests then you can gain access to sensitive data or worse completely compromise a vulnerable host. SSRF is number 10 on the 2021 OWASP Top 10 list and is a growing threat to APIs.

# SSRF IMPACT

The impact of this vulnerability is that an attacker would be able to leverage the target server to perform and process requests that they supply. The attacker could supply URLs that expose private data, scan the target's internal network, or compromise the target through remote code execution.

# TYPES OF SSRF

1. In_Band SSRF
2. Blind SSRF

## In Band SSRF

For an In-Band SSRF, a URL is specified as an attack. The request is sent and the content of your supplied URL is displayed back to you in a response

### Example

# Intercepted Request:

    POST api/v1/store/products

    headers…

    {

    "inventory":"http://store.com/api/v3/inventory/item/12345"

    }

 

# Attack:

    POST api/v1/store/products

    headers…

    {

    "inventory":"§http://localhost/secrets§"

    }

 

# Response:

    HTTP/1.1 200 OK
    headers...
    {

    "secret_token":"crapi-admin"

    }

Once you have discovered an In-Band SSRF vulnerability you could leverage control over the URL to scan the internal network environment, gather sensitive information from the localhost, or attempt to perform a remote code execution attack.

## BLIND SSRF

Blind (or Out of Band) SSRF takes place when a vulnerable server performs a request from user input but does not send a response back to the user indicating a successful attack. The app does not provide an unusual response to the user, but the server does make the request to the URL specified by the attacker. In this case, to know if the request was made you will need to have some control over the web server that is specified in the attack.

### Example

# Intercepted Request:

    POST api/v1/store/products

    headers…

    {

    "inventory":"http://store.com/api/v3/inventory/item/12345"

    }

# Attack:

    POST api/v1/store/products

    headers…

    {

    "inventory:"§http://localhost/secrets§"

    } 

# Response:

    HTTP/1.1 200 OK
    headers...
    {}

In this case, the response is returned and we do not have any indication that the server is vulnerable. Instead of http://localhost/secrets, we will need to provide the URL to a web server that will let us see if a request is actually made. Burp Suite Pro has a great tool called Burp Suite Collaborator. Collaborator can be leveraged to set up a web server that will provide us with the details of any requests that are made to our random URL.

To stick with free tools, we will leverage
    - http://webhook.site
    - http://pingb.in/ 
    - https://requestbin.com/ 
    - https://canarytokens.org/


# Ingredients For SSRF

When targeting an API for SSRF vulnerabilities, you will want to look for requests that have any of the following:

    - Include full URLs in the POST body or parameters
    - Include URL paths (or partial URLs) in the POST body or parameters
    - Headers that include URLs like Referer
    - Allows for user input that may result in a server retrieving resources

# TESTING FOR SSRF

- Either using Postman or the web browser, proxy the requests that you are targeting to Burp Suite.
- Next, send the request over to Repeater to get an idea of a typical response.
- SEND TO INTRUDER, and use ssrf payload from payloadallthethings

- Check server tools, to see if you have positive result 