# JWT attacks
- Design issues and flawed handling of JSON web tokens (JWTs) can leave websites vulnerable to a variety of high-severity attacks. 
- As JWTs are most commonly used in authentication, session management, and access control mechanisms, these vulnerabilities can potentially compromise the entire website and its users.

# What are JWTs?
- JSON web tokens (JWTs) are a standardized format for sending cryptographically signed JSON data between systems. 
- They can theoretically contain any kind of data, but are most commonly used to send information ("claims") about users as part of authentication, session handling, and access control mechanisms.
- Unlike with classic session tokens, all of the data that a server needs is stored client-side within the JWT itself. 
- This makes JWTs a popular choice for highly distributed websites where users need to interact seamlessly with multiple back-end servers.

# JWT format
- A JWT consists of 3 parts: a header, a payload, and a signature. These are each separated by a dot, as shown in the following example:
```
eyJraWQiOiI5MTM2ZGRiMy1jYjBhLTRhMTktYTA3ZS1lYWRmNWE0NGM4YjUiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTY0ODAzNzE2NCwibmFtZSI6IkNhcmxvcyBNb250b3lhIiwic3ViIjoiY2FybG9zIiwicm9sZSI6ImJsb2dfYXV0aG9yIiwiZW1haWwiOiJjYXJsb3NAY2FybG9zLW1vbnRveWEubmV0IiwiaWF0IjoxNTE2MjM5MDIyfQ.SYZBPIBg2CRjXAJ8vCER0LA_ENjII1JakvNQoP-Hw6GG1zfl4JyngsZReIfqRvIAEi5L4HV0q7_9qGhQZvy9ZdxEJbwTxRs_6Lb-fZTDpW6lKYNdMyjw45_alSCZ1fypsMWz_2mTpQzil0lOtps5Ei_z7mM7M8gCwe_AGpI53JxduQOaB5HkT5gVrv9cKu9CsW5MS6ZbqYXpGyOG5ehoxqm8DL5tFYaW3lB50ELxi0KsuTKEbD0t5BCl0aCR2MBJWAbN-xeLwEenaqBiwPVvKixYleeDQiBEIylFdNNIMviKRgXiYuAvMziVPbwSgkZVHeEdF5MQP1Oe2Spac-6IfA
```
- The header and payload parts of a JWT are just base64url-encoded JSON objects. 
- The header contains metadata about the token itself, while the payload contains the actual "claims" about the user. 
- For example, you can decode the payload from the token above to reveal the following claims:
```json
{
    "iss": "portswigger",
    "exp": 1648037164,
    "name": "Carlos Montoya",
    "sub": "carlos",
    "role": "blog_author",
    "email": "carlos@carlos-montoya.net",
    "iat": 1516239022
}
```
- In most cases, this data can be easily read or modified by anyone with access to the token. 
- Therefore, the security of any JWT-based mechanism is heavily reliant on the cryptographic signature.

# JWT signature
- The server that issues the token typically generates the signature by hashing the header and payload. 
- In some cases, they also encrypt the resulting hash. 
- Either way, this process involves a secret signing key. 
- This mechanism provides a way for servers to verify that none of the data within the token has been tampered with since it was issued:
- As the signature is directly derived from the rest of the token, changing a single byte of the header or payload results in a mismatched signature.
- Without knowing the server's secret signing key, it shouldn't be possible to generate the correct signature for a given header or payload.

# Tip
- If you want to gain a better understanding of how JWTs are constructed, you can use the debugger on jwt.io to experiment with arbitrary tokens. 

# JWT vs JWS vs JWE
- The JWT specification is actually very limited. 
- It only defines a format for representing information ("claims") as a JSON object that can be transferred between two parties. 
- In practice, JWTs aren't really used as a standalone entity. 
- The JWT spec is extended by both the JSON Web Signature (JWS) and JSON Web Encryption (JWE) specifications, which define concrete ways of actually implementing JWTs.
- In other words, a JWT is usually either a JWS or JWE token. 
- When people use the term "JWT", they almost always mean a JWS token. 
- JWEs are very similar, except that the actual contents of the token are encrypted rather than just encoded.

# What are JWT attacks?
- JWT attacks involve a user sending modified JWTs to the server in order to achieve a malicious goal. 
- Typically, this goal is to bypass authentication and access controls by impersonating another user who has already been authenticated.

# What is the impact of JWT attacks?
- The impact of JWT attacks is usually severe. 
- If an attacker is able to create their own valid tokens with arbitrary values, they may be able to escalate their own privileges or impersonate other users, taking full control of their accounts.

# How do vulnerabilities to JWT attacks arise?
- JWT vulnerabilities typically arise due to flawed JWT handling within the application itself. 
- The various specifications related to JWTs are relatively flexible by design, allowing website developers to decide many implementation details for themselves. 
- This can result in them accidentally introducing vulnerabilities even when using battle-hardened libraries.
- These implementation flaws usually mean that the signature of the JWT is not verified properly. 
- This enables an attacker to tamper with the values passed to the application via the token's payload. 
- Even if the signature is robustly verified, whether it can truly be trusted relies heavily on the server's secret key remaining a secret. 
- If this key is leaked in some way, or can be guessed or brute-forced, an attacker can generate a valid signature for any arbitrary token, compromising the entire mechanism.

# Exploiting flawed JWT signature verification
- By design, servers don't usually store any information about the JWTs that they issue. 
- Instead, each token is an entirely self-contained entity. 
- This has several advantages, but also introduces a fundamental problem - the server doesn't actually know anything about the original contents of the token, or even what the original signature was. 
- Therefore, if the server doesn't verify the signature properly, there's nothing to stop an attacker from making arbitrary changes to the rest of the token.
- For example, consider a JWT containing the following claims:
```
{
    "username": "carlos",
    "isAdmin": false
}
```
- If the server identifies the session based on this username, modifying its value might enable an attacker to impersonate other logged-in users. 
- Similarly, if the isAdmin value is used for access control, this could provide a simple vector for privilege escalation.
- In the first couple of labs, you'll see some examples of how these vulnerabilities might look in real-world applications.

# Accepting arbitrary signatures
- JWT libraries typically provide one method for verifying tokens and another that just decodes them. 
- For example, the Node.js library jsonwebtoken has verify() and decode().
- Occasionally, developers confuse these two methods and only pass incoming tokens to the decode() method. 
- This effectively means that the application doesn't verify the signature at all.

# Lab: JWT authentication bypass via unverified signature
- This lab uses a JWT-based mechanism for handling sessions. 
- Due to implementation flaws, the server doesn't verify the signature of any JWTs that it receives.
- To solve the lab, modify your session token to gain access to the admin panel at /admin, then delete the user carlos.
- You can log in to your own account using the following credentials: wiener:peter

# Solution
- In the lab, log in to your own account.
- In Burp, go to the Proxy > HTTP history tab and look at the post-login GET /my-account request. Observe that your session cookie is a JWT.
- Double-click the payload part of the token to view its decoded JSON form in the Inspector panel. Notice that the sub claim contains your username. Send this request to Burp Repeater.
- In Burp Repeater, change the path to /admin and send the request. Observe that the admin panel is only accessible when logged in as the administrator user.
- Select the payload of the JWT again. In the Inspector panel, change the value of the sub claim from wiener to administrator, then click Apply changes.
- Send the request again. Observe that you have successfully accessed the admin panel.
- In the response, find the URL for deleting carlos (/admin/delete?username=carlos). Send the request to this endpoint to solve the lab.

# Command Line Solution
- In the lab, log in to your own account.
- In Burp, go to the Proxy > HTTP history tab and look at the post-login GET /my-account request. Observe that your session cookie is a JWT.
- Copy the jwt and go to your command line
- Assuming you have the JWT tool Install
- Do the following code :
```
jwt_tool "eyJraWQiOiIzMDU0ZGViMC1lNTM0LTRhOTYtOTkzZC0wNTlkNzVlZjM4YzIiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc1ODI4Mjg0Mywic3ViIjoid2llbmVyIn0.umFu1lAgRS-vKhmpVINGsfK1L1CfliQMBlHnojqqzWCEzNcPnh-nrUY0gYcn8a_qcPTOjIbm13s1unfMg844LbnYiUCB_ipunbyIidLOYIBIzHga_J1zZLzsCAHpASHz5CCWHqKHq-cZFGFJAJm1IlKy3_gYkCmhSQwPUj8WHg01kORFT6D_xG5YROEXUjGwQfRF864Lix1J3rS8kbX0dL8jZFDYhz-eFRIq6ldtr616yowlpvBds03eL0LDfSJe7Ykfg1m6PHFSQcSurmmLkpVRX_T6jtITxEKdgWRxu7ZdGgFmbquN7HIP2dnvp1uMykY_UTwfSujDAAXnUaQwMA" -T
```
- The -T allows us to tamper with the JWT
- You can tamper with the Payload and change wiener to administrator
- You will have a new JWT
- Go back to burp and replace the old JWT with the tampered one
- You will notice that it is acceptable, GO on and delete carlos

# Accepting tokens with no signature

- Among other things, the JWT header contains an alg parameter. 
- This tells the server which algorithm was used to sign the token and, therefore, which algorithm it needs to use when verifying the signature.
```
{
    "alg": "HS256",
    "typ": "JWT"
}
```
- This is inherently flawed because the server has no option but to implicitly trust user-controllable input from the token which, at this point, hasn't been verified at all. 
- In other words, an attacker can directly influence how the server checks whether the token is trustworthy.
- JWTs can be signed using a range of different algorithms, but can also be left unsigned. 
- In this case, the alg parameter is set to none, which indicates a so-called "unsecured JWT". 
- Due to the obvious dangers of this, servers usually reject tokens with no signature. 
- However, as this kind of filtering relies on string parsing, you can sometimes bypass these filters using classic obfuscation techniques, such as mixed capitalization and unexpected encodings

# Note
- Even if the token is unsigned, the payload part must still be terminated with a trailing dot.

# Lab: JWT authentication bypass via flawed signature verification
- This lab uses a JWT-based mechanism for handling sessions. The server is insecurely configured to accept unsigned JWTs.
- To solve the lab, modify your session token to gain access to the admin panel at /admin, then delete the user carlos.
- You can log in to your own account using the following credentials: wiener:peter

# Solution
- In the lab, log in to your own account.
- In Burp, go to the Proxy > HTTP history tab and look at the post-login GET /my-account request. Observe that your session cookie is a JWT.
- Double-click the payload part of the token to view its decoded JSON form in the Inspector panel. 
- Notice that the sub claim contains your username. Send this request to Burp Repeater.
- In Burp Repeater, change the path to /admin and send the request. Observe that the admin panel is only accessible when logged in as the administrator user.
- Select the payload of the JWT again. In the Inspector panel, change the value of the sub claim to administrator, then click Apply changes.
- Select the header of the JWT, then use the Inspector to change the value of the alg parameter to none. Click Apply changes.
- In the message editor, remove the signature from the JWT, but remember to leave the trailing dot after the payload.
- Send the request and observe that you have successfully accessed the admin panel.
- In the response, find the URL for deleting carlos (/admin/delete?username=carlos). Send the request to this endpoint to solve the lab.
- We can just Use the none Attack feature of the JWT editor

# Solution Using JWT_TOOL
- In the lab, Log into your own account.
- In Burp, go to the Proxy > HTTP history tab and look at the post-login GET /my-account request. Observe that your session cookie is a JWT.
- Double-click the payload part of the token to view its decoded JSON form in the Inspector panel. 
- Notice that the sub claim contains your username. Send this request to Burp Repeater.
- In Burp Repeater, change the path to /admin and send the request. Observe that the admin panel is only accessible when logged in as the administrator user.
- Copy the jwt and do the following
- Convert the algorithm to none by doing the following command
```
jwt_tool "eyJraWQiOiI1MTFjZjA1NC02OGUwLTQxNGItYWUwZi1iMjg4MGNhMGFlNDkiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc1ODI5MjA2NSwic3ViIjoid2llbmVyIn0.DDl-wRMBbGHAkS5Dqf9wV2nNCKZgNxYkAa59xt8Lv-l2sIeGIBWSSf473uXI5tB5MoQYaZ84jw0edSWBwMrafZ-MsMRaFTUNcjrY6Aux05li5Oi5o3BDYzrPJ6d2wzNDIC9jaZ9L0TsQP8zOAHaAzHMv7Fb15Oj_5NWxME-mobIWPnnj97COXgixu8jKUenuZILiohx7Az39TXut6GmOCrcSR6aFVNCoyKX-jAu6bGhoJP2E2ahAX_xBoIz4d_y-ttRQb9-sgz7zq-1RfM63Y6xLhAtQe52K98AdUk1nmQRfmQam6GXfXlPJ34_e-Pax1_irnjnt0ZSRpe5dspOe4A" -X a
```
- You can try all the available options but none is the only one that will work
- Notice that the token now has a very short length
- Copy the token and tamper the sub value to administrator
```
jwt_tool "eyJraWQiOiI1MTFjZjA1NC02OGUwLTQxNGItYWUwZi1iMjg4MGNhMGFlNDkiLCJhbGciOiJub25lIn0.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc1ODI5MjA2NSwic3ViIjoid2llbmVyIn0." -T
```
- Paste the resulting token into burp repeater and request the /admin enpoint
- Delete carlos

# Brute-forcing secret keys
- Some signing algorithms, such as HS256 (HMAC + SHA-256), use an arbitrary, standalone string as the secret key. 
- Just like a password, it's crucial that this secret can't be easily guessed or brute-forced by an attacker. 
- Otherwise, they may be able to create JWTs with any header and payload values they like, then use the key to re-sign the token with a valid signature.
- When implementing JWT applications, developers sometimes make mistakes like forgetting to change default or placeholder secrets. 
- They may even copy and paste code snippets they find online, then forget to change a hardcoded secret that's provided as an example. 
- In this case, it can be trivial for an attacker to brute-force a server's secret using a wordlist of well-known secrets. (https://github.com/wallarm/jwt-secrets/blob/master/jwt.secrets.list)

# Brute-forcing secret keys using hashcat
- We recommend using hashcat to brute-force secret keys. 
- You can install hashcat manually, but it also comes pre-installed and ready to use on Kali Linux.
- If you're using the pre-built VirtualBox image for Kali rather than the bare metal installer version, this may not have enough memory allocated to run hashcat
- You just need a valid, signed JWT from the target server and a wordlist of well-known secrets. 
- You can then run the following command, passing in the JWT and wordlist as arguments:
```
hashcat -a 0 -m 16500 <jwt> <wordlist>
```
- Hashcat signs the header and payload from the JWT using each secret in the wordlist, then compares the resulting signature with the original one from the server. 
- If any of the signatures match, hashcat outputs the identified secret in the following format, along with various other details:
```
<jwt>:<identified-secret>
```
- # Note
- If you run the command more than once, you need to include the --show flag to output the results.
- As hashcat runs locally on your machine and doesn't rely on sending requests to the server, this process is extremely quick, even when using a huge wordlist.
- Once you have identified the secret key, you can use it to generate a valid signature for any JWT header and payload that you like.

# Lab: JWT authentication bypass via weak signing key
- This lab uses a JWT-based mechanism for handling sessions. It uses an extremely weak secret key to both sign and verify tokens. 
- This can be easily brute-forced using a wordlist of common secrets.
- To solve the lab, first brute-force the website's secret key. 
- Once you've obtained this, use it to sign a modified session token that gives you access to the admin panel at /admin, then delete the user carlos.
- You can log in to your own account using the following credentials: wiener:peter

# Solution
1. # Part 1 - Brute-force the secret key
- In Burp, load the JWT Editor extension from the BApp store.
- In the lab, log in to your own account and send the post-login GET /my-account request to Burp Repeater.
- In Burp Repeater, change the path to /admin and send the request. Observe that the admin panel is only accessible when logged in as the administrator user.
- Copy the JWT and brute-force the secret. You can do this using hashcat as follows:
```
hashcat -a 0 -m 16500 <YOUR-JWT> /path/to/jwt.secrets.list
```
- If you're using hashcat, this outputs the JWT, followed by the secret. If everything worked correctly, this should reveal that the weak secret is secret1.

# Part 2 - Generate a forged signing key
- Using Burp Decoder, Base64 encode the secret that you brute-forced in the previous section.
- In Burp, go to the JWT Editor Keys tab and click New Symmetric Key. 
- In the dialog, click Generate to generate a new key in JWK format. 
- Note that you don't need to select a key size as this will automatically be updated later.
- Replace the generated value for the k property with the Base64-encoded secret.
- Click OK to save the key.

# Part 3 - Modify and sign the JWT
- Go back to the GET /admin request in Burp Repeater and switch to the extension-generated JSON Web Token message editor tab.
- In the payload, change the value of the sub claim to administrator
- At the bottom of the tab, click Sign, then select the key that you generated in the previous section.
- Make sure that the Don't modify header option is selected, then click OK. The modified token is now signed with the correct signature.
- Send the request and observe that you have successfully accessed the admin panel.
- In the response, find the URL for deleting carlos (/admin/delete?username=carlos). Send the request to this endpoint to solve the lab.

# Note
- Instead of this Part Two and part 3 we can use the JSON web TOKens Extention and recalculate with the secret key that was found and change the username part to administrator
- We can also use the jwt_tool instead of hashcat
```
jwt_tool "jwt code" -C -d jwtsecretlist 
```
- After getting the secret, run the following code
jwt_tool "jwt_code" -T -S hs256 -p "THE_SECRET"
- Copy the resulting jwt and paste it in.
- If the server uses an extremely weak secret, it may even be possible to brute-force this character-by-character rather than using a wordlist.


# JWT header parameter injections
- According to the JWS specification, only the alg header parameter is mandatory. 
- In practice, however, JWT headers (also known as JOSE headers) often contain several other parameters. 
- The following ones are of particular interest to attackers.
- jwk (JSON Web Key) - Provides an embedded JSON object representing the key.
- jku (JSON Web Key Set URL) - Provides a URL from which servers can fetch a set of keys containing the correct key.
- kid (Key ID) - Provides an ID that servers can use to identify the correct key in cases where there are multiple keys to choose from. 
- Depending on the format of the key, this may have a matching kid parameter.
- As you can see, these user-controllable parameters each tell the recipient server which key to use when verifying the signature. 
- In this section, you'll learn how to exploit these to inject modified JWTs signed using your own arbitrary key rather than the server's secret.

# Injecting self-signed JWTs via the jwk parameter
- The JSON Web Signature (JWS) specification describes an optional jwk header parameter, which servers can use to embed their public key directly within the token itself in JWK format.

## JWK
- A JWK (JSON Web Key) is a standardized format for representing keys as a JSON object.
- You can see an example of this in the following JWT header:
```json
{
    "kid": "ed2Nf8sb-sD6ng0-scs5390g-fFD8sfxG",
    "typ": "JWT",
    "alg": "RS256",
    "jwk": {
        "kty": "RSA",
        "e": "AQAB",
        "kid": "ed2Nf8sb-sD6ng0-scs5390g-fFD8sfxG",
        "n": "yy1wpYmffgXBxhAUJzHHocCuJolwDqql75ZWuCQ_cb33K2vh9m"
    }
}
```
- Ideally, servers should only use a limited whitelist of public keys to verify JWT signatures. 
- However, misconfigured servers sometimes use any key that's embedded in the jwk parameter.
- You can exploit this behavior by signing a modified JWT using your own RSA private key, then embedding the matching public key in the jwk header.
- Although you can manually add or modify the jwk parameter in Burp, the JWT Editor extension provides a useful feature to help you test for this vulnerability:
    - With the extension loaded, in Burp's main tab bar, go to the JWT Editor Keys tab.
    - Generate a new RSA key.
    - Send a request containing a JWT to Burp Repeater.
    - In the message editor, switch to the extension-generated JSON Web Token tab and modify the token's payload however you like.
    - Click Attack, then select Embedded JWK. When prompted, select your newly generated RSA key.
    - Send the request to test how the server responds.
- You can also perform this attack manually by adding the jwk header yourself. 
- However, you may also need to update the JWT's kid header parameter to match the kid of the embedded key. 
- The extension's built-in attack takes care of this step for you.

# Lab: JWT authentication bypass via jwk header injection
- This lab uses a JWT-based mechanism for handling sessions. 
- The server supports the jwk parameter in the JWT header. 
- This is sometimes used to embed the correct verification key directly in the token. 
- However, it fails to check whether the provided key came from a trusted source.
- To solve the lab, modify and sign a JWT that gives you access to the admin panel at /admin, then delete the user carlos.
- You can log in to your own account using the following credentials: wiener:peter

# My Solution 
- Using Burp Log into your account 
- Go to Jwt Editor and create a new RSA key
- Send a Request containing a JWT to Burp Repeater.
- In the message editor, switch to the extension-generated JSON Web Token tab and modify the token's payload "wiener to administrator.
- Change the request to /admin and send the request
- If successful Delete user carlos to solve the lab

# Lab Solution
- In Burp, load the JWT Editor extension from the BApp store.
- In the lab, log in to your own account and send the post-login GET /my-account request to Burp Repeater.
- In Burp Repeater, change the path to /admin and send the request. Observe that the admin panel is only accessible when logged in as the administrator user.
- Go to the JWT Editor Keys tab in Burp's main tab bar.
- Click New RSA Key.
- In the dialog, click Generate to automatically generate a new key pair, then click OK to save the key. Note that you don't need to select a key size as this will automatically be updated later.
- Go back to the GET /admin request in Burp Repeater and switch to the extension-generated JSON Web Token tab.
- In the payload, change the value of the sub claim to administrator.
- At the bottom of the JSON Web Token tab, click Attack, then select Embedded JWK. When prompted, select your newly generated RSA key and click OK.
- In the header of the JWT, observe that a jwk parameter has been added containing your public key.
- Send the request. Observe that you have successfully accessed the admin panel.
- In the response, find the URL for deleting carlos (/admin/delete?username=carlos). Send the request to this endpoint to solve the lab.

# Note
- Instead of using the built-in attack in the JWT Editor extension, you can embed a JWK by adding a jwk parameter to the header of the JWT manually. 
- In this case, you need to also update the kid header of the token to match the kid of the embedded key.

# Using JWT_TOOL 
- Get the jwt and run this command
```
jwt_tool "eyJraWQiOiIwNDQ4ZWQ1Ni1jMzgwLTQ1MzgtODlkNi0wYWIxZTRkZmZiODUiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc1ODM4MDUwOSwic3ViIjoid2llbmVyIn0.C6q2ZEt4sQw9rsbHOxiBpJMLDyzpMv5PyrTsTiKlJKoKp1yacCJnqt501QRGIpnXhKNrlWnAeocjVqRM4KA35YeYz8hiA6cX5Jap_OBzFKh8ZRImzwK67wJzskdi7eBuS0MxRcGoOR0TCWvCtRgSR7gMDYOhVGzBxVoumiJ-0QFSlFufMcvAy1Ws4kYsvHcn1msz6AOaPitbc3DAf7Qb103GKIf1_yqVg6SUatrDLasnNsyDdjARTaKeMiDSiq9nO5qDfMrsy1dimYJrTpo7ywjjye25_x9VakPzp9fCkYzWC0RbpGb-L899LXSlg9q0fZLLR7zWK9KXlDAemd3orQ" -X i -T
```
- -X i options run the jwk inline attack and -T, tampers the the jwt
- Tamper the header to have "jwt_tool"
- Tamper the sub to become wiener
- Copy the resulting jwt to the cookie browser or burp repeater to delete carlos 

# Injecting self-signed JWTs via the jku parameter
- Instead of embedding public keys directly using the jwk header parameter, some servers let you use the jku (JWK Set URL) header parameter to reference a JWK Set containing the key. 
- When verifying the signature, the server fetches the relevant key from this URL.

# JWK Set
- A JWK Set is a JSON object containing an array of JWKs representing different keys. You can see an example of this below.

```json
{
    "keys": [
        {
            "kty": "RSA",
            "e": "AQAB",
            "kid": "75d0ef47-af89-47a9-9061-7c02a610d5ab",
            "n": "o-yy1wpYmffgXBxhAUJzHHocCuJolwDqql75ZWuCQ_cb33K2vh9mk6GPM9gNN4Y_qTVX67WhsN3JvaFYw-fhvsWQ"
        },
        {
            "kty": "RSA",
            "e": "AQAB",
            "kid": "d8fDFo-fS9-faS14a9-ASf99sa-7c1Ad5abA",
            "n": "fc3f-yy1wpYmffgXBxhAUJzHql79gNNQ_cb33HocCuJolwDqmk6GPM4Y_qTVX67WhsN3JvaFYw-dfg6DH-asAScw"
        }
    ]
}
```
- JWK Sets like this are sometimes exposed publicly via a standard endpoint, such as /.well-known/jwks.json.
- More secure websites will only fetch keys from trusted domains, but you can sometimes take advantage of URL parsing discrepancies to bypass this kind of filtering. 
- We covered some examples of these in our topic on SSRF.

# Lab: JWT authentication bypass via jku header injection
- This lab uses a JWT-based mechanism for handling sessions. The server supports the jku parameter in the JWT header. 
- However, it fails to check whether the provided URL belongs to a trusted domain before fetching the key.
- To solve the lab, forge a JWT that gives you access to the admin panel at /admin, then delete the user carlos.
- You can log in to your own account using the following credentials: wiener:peter

# My Solution
- Login to your account with burp on
- Navigate to burp JWT editor and create a new RSA key
- Copy the generated key and paste it to the body of the exploit server
```json
{
    "keys": [
        {
            "p": "9eXvK0K6iIj-RrxW9mnNOdx3lt4Jr_wsSjD-iEXrLPLkWpYoCjfc3Hd6Bkd9ZM73vguEoPAnGqPBJRbbS3lbcMy7jxzxtKFFTUJgXhpD0BVwu1xaggF4-T3BuMo4IP5XxNJwudX2on7owx1k-xuxsyeDnzCzAIQBNXHijqieEG0",
            "kty": "RSA",
            "q": "7yRl-q6TQsL1qLiIFQVEc7-Yg1RulNAYJDtiwnL_TPz0wbYWG_5TiNSmFi3GabN-H-d3dv3_eK8ivXJiL5ZqHQVUz-CAYgtVBV3gyElOf7Wle26DIEUcC9nlv2f1LIUapKZxL9hOgWrozInaehwWxrJu3PZrtU5LHqEZxmq4xqs",
            "d": "TH7_rsGXJ6NewrjdjpKNUCBCWSWzHZTGCyLOPKqOLACleKjCT4ut5F_uzqaUqGMsEvNVr3O14--2Dhj6qUhmZPOGvlpogXn6nLIxmWGtW8zSQwnVRH01g6IrDLBf89BZ0lFygIBXeJCG52G9xF6uuG7tzZL4XHbT2IKdVkoGN4wFkEE4LCiq4evUyG3Oq4cmIRQ6WksvV8Zpx7ZObYmefH7Jgqcza_xmzdz3yc1uhM3mY9_nMDX2SLRuoxCwHurE73N7IpAB72ByPyxfmxSpZQBpUIdkX9E2ajTfH0-JDEsI68mqBazylIgzkhfDzxC2QWb_WLRp9vDIm60E00V1uQ",
            "e": "AQAB",
            "kid": "f8213812-8452-4c37-bae2-de45afd4c739",
            "qi": "r78iilz6DLpDbfjIYF1TPezKt6QidFeJ-ynT7Ly7Kyh1wdTODa8bs8EAKSIaZTTRLYGNuML7EIzRwMFH_Krj25_i9X10sLThN64wwzUbowk90ZChySwrR9vCqVwdy0yynq26mTHvUfuDfJkydhbdYATGznN-5eby110cVG3ZSGQ",
            "dp": "7lSOGz_xy6P70FN7dhnV797fijpq6UdhJgeWrD4YUtiYu7QN2tmKF6U1gCCKSMrRFEHVqqcZP5i3-1rL8bsOBaZpo6xKGOi2YsuS26JZV7VwLii1EIyc0_YnbROSk2fxabMNzxCym4ylzXcQCNIuyZXi3Mg2tqk7ArH_BIYprYE",
            "dq": "n0UeplaevVgbRMOh3l4juPNiIBWbkIEHkxn6LIdqgVv3pwwerYY1HGyEMUFLZBqnZZhDeHyyKS57dLE5s3f6NFnYoppi5umlNm3Px5ULMwNHs21m55cflsUIvvH92CjOFdrEh5kIsCkD4zXszGboxG0SaRe1pIsAfOXOxNdPOQE",
            "n": "5bSgk4b45P4jwMvRZzXrgSZ9mCVlsxNWe1XvmIG3bGFHmfphkinMRdYdkMuqdIVBIuOKIEXgrXokFAXfrRVtIw8dr7ZTBW-_5L_snhuAxh2_RigAcxLZgFqhpRacT8_tc5ZZSR70Su3ZFHPPCqrj_axkyYZW0P1dTT7JgLnBx-U9i0A3PI8_BEsAUKswX-CD3czWduUvqRxSiBwoq1Vhe10syH3jn-IM_-FCb6AfeHW9gJO2PzdXzbVMdfjdRPznkRwkjabgvufT9u6qEk_AW-YjSQnRg3dJtEKlKG_0eLcae4dMhNcteoljw6w819ctUQ2f3byBbeClD6lr0qFGzw"
        }  
    ]
}
```
- Change the link of the exploit server to  https://exploit-0a3f008c0355bf8a8027deb601ee00a4.exploit-server.net/jwks.json
- Send a request containing jwt to repeater
- Change the enpoint to /admin and move to jwt-editor
- Replace the KID with the one from the exploit server
- Sign the the request 
- And send the requst
- Delete carlos to solve the lab

# Lab Solution
1. # Part 1 - Upload a malicious JWK Set
- In Burp, load the JWT Editor extension from the BApp store.
- In the lab, log in to your own account and send the post-login GET /my-account request to Burp Repeater.
- In Burp Repeater, change the path to /admin and send the request. Observe that the admin panel is only accessible when logged in as the administrator user.
- Go to the JWT Editor Keys tab in Burp's main tab bar.
- Click New RSA Key.
- In the dialog, click Generate to automatically generate a new key pair, then click OK to save the key. Note that you don't need to select a key size as this will automatically be updated later.
- In the browser, go to the exploit server.
- Replace the contents of the Body section with an empty JWK Set as follows:
```json
{
    "keys": [

    ]
}
```
- Back on the JWT Editor Keys tab, right-click on the entry for the key that you just generated, then select Copy Public Key as JWK.
- Paste the JWK into the keys array on the exploit server, then store the exploit. The result should look something like this:
```json
{
    "keys": [
        {
            "kty": "RSA",
            "e": "AQAB",
            "kid": "893d8f0b-061f-42c2-a4aa-5056e12b8ae7",
            "n": "yy1wpYmffgXBxhAUJzHHocCuJolwDqql75ZWuCQ_cb33K2vh9mk6GPM9gNN4Y_qTVX67WhsN3JvaFYw"
        }
    ]
}
```
2. # Part 2 - Modify and sign the JWT
- Go back to the GET /admin request in Burp Repeater and switch to the extension-generated JSON Web Token message editor tab.
- In the header of the JWT, replace the current value of the kid parameter with the kid of the JWK that you uploaded to the exploit server.
- Add a new jku parameter to the header of the JWT. Set its value to the URL of your JWK Set on the exploit server.
- In the payload, change the value of the sub claim to administrator.
- At the bottom of the tab, click Sign, then select the RSA key that you generated in the previous section.
- Make sure that the Don't modify header option is selected, then click OK. The modified token is now signed with the correct signature.
- Send the request. Observe that you have successfully accessed the admin panel.
- In the response, find the URL for deleting carlos (/admin/delete?username=carlos). Send the request to this endpoint to solve the lab.

# Injecting self-signed JWTs via the kid parameter
- Servers may use several cryptographic keys for signing different kinds of data, not just JWTs. 
- For this reason, the header of a JWT may contain a kid (Key ID) parameter, which helps the server identify which key to use when verifying the signature.
- Verification keys are often stored as a JWK Set. In this case, the server may simply look for the JWK with the same kid as the token. 
- However, the JWS specification doesn't define a concrete structure for this ID - it's just an arbitrary string of the developer's choosing. 
- For example, they might use the kid parameter to point to a particular entry in a database, or even the name of a file.
- If this parameter is also vulnerable to directory traversal, an attacker could potentially force the server to use an arbitrary file from its filesystem as the verification key.
```json
{
    "kid": "../../path/to/file",
    "typ": "JWT",
    "alg": "HS256",
    "k": "asGsADas3421-dfh9DGN-AFDFDbasfd8-anfjkvc"
}
```
- This is especially dangerous if the server also supports JWTs signed using a symmetric algorithm. 
- In this case, an attacker could potentially point the kid parameter to a predictable, static file, then sign the JWT using a secret that matches the contents of this file.
- You could theoretically do this with any file, but one of the simplest methods is to use /dev/null, which is present on most Linux systems. 
- As this is an empty file, reading it returns an empty string. 
- Therefore, signing the token with a empty string will result in a valid signature.

# Note
- If you're using the JWT Editor extension, note that this doesn't let you sign tokens using an empty string. 
- However, due to a bug in the extension, you can get around this by using a Base64-encoded null byte.

# Lab: JWT authentication bypass via kid header path traversal
- This lab uses a JWT-based mechanism for handling sessions. 
- In order to verify the signature, the server uses the kid parameter in JWT header to fetch the relevant key from its filesystem.
- To solve the lab, forge a JWT that gives you access to the admin panel at /admin, then delete the user carlos.
- You can log in to your own account using the following credentials: wiener:peter

# Lab Solution
- # NOTE
- In this solution, we'll point the kid parameter to the standard file /dev/null. In practice, you can point the kid parameter to any file with predictable contents.
- # Generate a suitable signing key
- In Burp, load the JWT Editor extension from the BApp store.
- In the lab, log in to your own account and send the post-login GET /my-account request to Burp Repeater.
- In Burp Repeater, change the path to /admin and send the request. Observe that the admin panel is only accessible when logged in as the administrator user.
- Go to the JWT Editor Keys tab in Burp's main tab bar.
- Click New Symmetric Key.
- In the dialog, click Generate to generate a new key in JWK format. Note that you don't need to select a key size as this will automatically be updated later.
- Replace the generated value for the k property with a Base64-encoded null byte (AA==). 
- Note that this is just a workaround because the JWT Editor extension won't allow you to sign tokens using an empty string.
- Click OK to save the key.
- # Modify and sign the JWT
- Go back to the GET /admin request in Burp Repeater and switch to the extension-generated JSON Web Token message editor tab.
- In the header of the JWT, change the value of the kid parameter to a path traversal sequence pointing to the /dev/null file:
```
../../../dev/null
```
- In the JWT payload, change the value of the sub claim to administrator.
- At the bottom of the tab, click Sign, then select the symmetric key that you generated in the previous section.
- Make sure that the Don't modify header option is selected, then click OK. The modified token is now signed using a null byte as the secret key.
- Send the request and observe that you have successfully accessed the admin panel.
- In the response, find the URL for deleting carlos (/admin/delete?username=carlos). Send the request to this endpoint to solve the lab.

- Solution With JWT_TOOL
- Copy the JWT and run the following commands
```
jwt_tool "eyJraWQiOiIyNjUwNWI3MS04N2RmLTQ2MDAtOTUyNC1hZTY3YjExZWMyNTQiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc1ODQ1MTA0OSwic3ViIjoid2llbmVyIn0.YS2998KGOSwBg2K4Q6jFaCeoA7O8qy1HSd27kLOpszk" -T -S hs256
```
- -S is to sign the JWT with hs256 after tampering
- While Tampering change the kid to ../../../dev/null and the sub value to administrator
- Click on enter and take note of the new jwt, paste it in your burp suite or browser session
- Reload and delete carlos
- We can also use this command
```
jwt_tool "eyJraWQiOiIyNjUwNWI3MS04N2RmLTQ2MDAtOTUyNC1hZTY3YjExZWMyNTQiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJwb3J0c3dpZ2dlciIsImV4cCI6MTc1ODQ1MTA0OSwic3ViIjoid2llbmVyIn0.YS2998KGOSwBg2K4Q6jFaCeoA7O8qy1HSd27kLOpszk" -I -hc kid -hv '../../../dev/null' -pc sub -pv administrator -S hs256 -p ''
```
* If the server stores its verification keys in a database, the kid header parameter is also a potential vector for SQL injection attacks.*

# Other interesting JWT header parameters
- The following header parameters may also be interesting for attackers:
1. cty (Content Type) - 
- Sometimes used to declare a media type for the content in the JWT payload. 
- This is usually omitted from the header, but the underlying parsing library may support it anyway. 
- If you have found a way to bypass signature verification, you can try injecting a cty header to change the content type to text/xml or application/x-java-serialized-object, which can potentially enable new vectors for XXE and deserialization attacks.
2. x5c (X.509 Certificate Chain) - 
- Sometimes used to pass the X.509 public key certificate or certificate chain of the key used to digitally sign the JWT. 
- This header parameter can be used to inject self-signed certificates, similar to the jwk header injection attacks discussed above. 
- Due to the complexity of the X.509 format and its extensions, parsing these certificates can also introduce vulnerabilities. 
- Details of these attacks are beyond the scope of these materials, but for more details, check out CVE-2017-2800 and CVE-2018-2633.

# How to prevent JWT attacks
- You can protect your own websites against many of the attacks we've covered by taking the following high-level measures:
- Use an up-to-date library for handling JWTs and make sure your developers fully understand how it works, along with any security implications. 
- Modern libraries make it more difficult for you to inadvertently implement them insecurely, but this isn't foolproof due to the inherent flexibility of the related specifications.
- Make sure that you perform robust signature verification on any JWTs that you receive, and account for edge-cases such as JWTs signed using unexpected algorithms.
- Enforce a strict whitelist of permitted hosts for the jku header.
- Make sure that you're not vulnerable to path traversal or SQL injection via the kid header parameter.

# Additional best practice for JWT handling
- Although not strictly necessary to avoid introducing vulnerabilities, we recommend adhering to the following best practice when using JWTs in your applications:
- Always set an expiration date for any tokens that you issue.
- Avoid sending tokens in URL parameters where possible.
- Include the aud (audience) claim (or similar) to specify the intended recipient of the token. This prevents it from being used on different websites.
- Enable the issuing server to revoke tokens (on logout, for example).