# Algorithm confusion attacks
- Algorithm confusion attacks (also known as key confusion attacks) occur when an attacker is able to force the server to verify the signature of a JSON web token (JWT) using a different algorithm than is intended by the website's developers. 
- If this case isn't handled properly, this may enable attackers to forge valid JWTs containing arbitrary values without needing to know the server's secret signing key.

# Symmetric vs asymmetric algorithms
- JWTs can be signed using a range of different algorithms. 
- Some of these, such as HS256 (HMAC + SHA-256) use a "symmetric" key. 
- This means that the server uses a single key to both sign and verify the token. 
- Clearly, this needs to be kept secret, just like a password.
- Other algorithms, such as RS256 (RSA + SHA-256) use an "asymmetric" key pair. 
- This consists of a private key, which the server uses to sign the token, and a mathematically related public key that can be used to verify the signature.

# How do algorithm confusion vulnerabilities arise?
- Algorithm confusion vulnerabilities typically arise due to flawed implementation of JWT libraries. 
- Although the actual verification process differs depending on the algorithm used, many libraries provide a single, algorithm-agnostic method for verifying signatures. 
- These methods rely on the alg parameter in the token's header to determine the type of verification they should perform.
- The following pseudo-code shows a simplified example of what the declaration for this generic verify() method might look like in a JWT library:

```javascript
function verify(token, secretOrPublicKey){
    algorithm = token.getAlgHeader();
    if(algorithm == "RS256"){
        // Use the provided key as an RSA public key
    } else if (algorithm == "HS256"){
        // Use the provided key as an HMAC secret key
    }
}
```
- Problems arise when website developers who subsequently use this method assume that it will exclusively handle JWTs signed using an asymmetric algorithm like RS256. 
- Due to this flawed assumption, they may always pass a fixed public key to the method as follows:
```javascript
publicKey = <public-key-of-server>;
token = request.getCookie("session");
verify(token, publicKey);
```
- In this case, if the server receives a token signed using a symmetric algorithm like HS256, the library's generic verify() method will treat the public key as an HMAC secret. 
- This means that an attacker could sign the token using HS256 and the public key, and the server will use the same public key to verify the signature.

# Note
- The public key you use to sign the token must be absolutely identical to the public key stored on the server. 
- This includes using the same format (such as X.509 PEM) and preserving any non-printing characters like newlines. 
- In practice, you may need to experiment with different formatting in order for this attack to work.

# Performing an algorithm confusion attack
- An algorithm confusion attack generally involves the following high-level steps:
1. Obtain the server's public key
2. Convert the public key to a suitable format
3. Create a malicious JWT with a modified payload and the alg header set to HS256.
4. Sign the token with HS256, using the public key as the secret.
- In this section, we'll walk through this process in more detail, demonstrating how you can perform this kind of attack using Burp Suite.

# Step 1 - Obtain the server's public key
- Servers sometimes expose their public keys as JSON Web Key (JWK) objects via a standard endpoint mapped to /jwks.json or /.well-known/jwks.json, for example. 
- These may be stored in an array of JWKs called keys. This is known as a JWK Set.
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
- Even if the key isn't exposed publicly, you may be able to extract it from a pair of existing JWTs.

# Step 2 - Convert the public key to a suitable format
- Although the server may expose their public key in JWK format, when verifying the signature of a token, it will use its own copy of the key from its local filesystem or database. This may be stored in a different format.
- In order for the attack to work, the version of the key that you use to sign the JWT must be identical to the server's local copy. 
- In addition to being in the same format, every single byte must match, including any non-printing characters.
- For the purpose of this example, let's assume that we need the key in X.509 PEM format. 
- You can convert a JWK to a PEM using the JWT Editor extension in Burp as follows:
1. With the extension loaded, in Burp's main tab bar, go to the JWT Editor Keys tab.
2. Click New RSA Key. In the dialog, paste the JWK that you obtained earlier.
3. Select the PEM radio button and copy the resulting PEM key.
4. Go to the Decoder tab and Base64-encode the PEM.
5. Go back to the JWT Editor Keys tab and click New Symmetric Key.
6. In the dialog, click Generate to generate a new key in JWK format.
7. Replace the generated value for the k parameter with a Base64-encoded PEM key that you just copied.
8. Save the key

# Step 3 - Modify your JWT
- Once you have the public key in a suitable format, you can modify the JWT however you like. 
- Just make sure that the alg header is set to HS256.

# Step 4 - Sign the JWT using the public key
- Sign the token using the HS256 algorithm with the RSA public key as the secret.

# Lab: JWT authentication bypass via algorithm confusion
- This lab uses a JWT-based mechanism for handling sessions. 
- It uses a robust RSA key pair to sign and verify tokens. However, due to implementation flaws, this mechanism is vulnerable to algorithm confusion attacks.
- To solve the lab, first obtain the server's public key. This is exposed via a standard endpoint. Use this key to sign a modified session token that gives you access to the admin panel at /admin, then delete the user carlos.
- You can log in to your own account using the following credentials: wiener:peter

# Solution
- # Part 1
- In Burp, load the JWT Editor extension from the BApp store.
- In the lab, log in to your own account and send the post-login GET /my-account request to Burp Repeater.
- In Burp Repeater, change the path to /admin and send the request. Observe that the admin panel is only accessible when logged in as the administrator user.
- In the browser, go to the standard endpoint /jwks.json and observe that the server exposes a JWK Set containing a single public key.
- Copy the JWK object from inside the keys array. Make sure that you don't accidentally copy any characters from the surrounding array.
- # Part 2 - Generate a malicious signing key
- In Burp, go to the JWT Editor Keys tab in Burp's main tab bar.
- Click New RSA Key.
- In the dialog, make sure that the JWK option is selected, then paste the JWK that you just copied. Click OK to save the key.
- Right-click on the entry for the key that you just created, then select Copy Public Key as PEM.
- Use the Decoder tab to Base64 encode this PEM key, then copy the resulting string.
- Go back to the JWT Editor Keys tab in Burp's main tab bar.
- Click New Symmetric Key. In the dialog, click Generate to generate a new key in JWK format. Note that you don't need to select a key size as this will automatically be updated later.
- Replace the generated value for the k property with a Base64-encoded PEM that you just created.
- Save the key.
- # Part 3 - Modify and sign the token
- Go back to the GET /admin request in Burp Repeater and switch to the extension-generated JSON Web Token tab.
- In the header of the JWT, change the value of the alg parameter to HS256.
- In the payload, change the value of the sub claim to administrator.
- At the bottom of the tab, click Sign, then select the symmetric key that you generated in the previous section.
- Make sure that the Don't modify header option is selected, then click OK. The modified token is now signed using the server's public key as the secret key.
- Send the request and observe that you have successfully accessed the admin panel.
- In the response, find the URL for deleting carlos (/admin/delete?username=carlos). Send the request to this endpoint to solve the lab.

# Deriving public keys from existing tokens
- In cases where the public key isn't readily available, you may still be able to test for algorithm confusion by deriving the key from a pair of existing JWTs. 
- This process is relatively simple using tools such as jwt_forgery.py. You can find this, along with several other useful scripts, on the rsa_sign2n GitHub repository.
- We have also created a simplified version of this tool, which you can run as a single command:
```bash
docker run --rm -it portswigger/sig2n <token1> <token2>
```
- Note
- You need the Docker CLI to run either version of the tool. The first time you run this command, it will automatically pull the image from Docker Hub, which may take a few minutes.
- This uses the JWTs that you provide to calculate one or more potential values of n. 
- Don't worry too much about what this means - all you need to know is that only one of these matches the value of n used by the server's key. 
- For each potential value, our script outputs:
- A Base64-encoded PEM key in both X.509 and PKCS1 format.
- A forged JWT signed using each of these keys.
- To identify the correct key, use Burp Repeater to send a request containing each of the forged JWTs. 
- Only one of these will be accepted by the server. 
- You can then use the matching key to construct an algorithm confusion attack.

# Solution
1. # Part 1 - Obtain two JWTs generated by the server
- In Burp, load the JWT Editor extension from the BApp store.
- In the lab, log in to your own account and send the post-login GET /my-account request to Burp Repeater.
- In Burp Repeater, change the path to /admin and send the request. Observe that the admin panel is only accessible when logged in as the administrator user.
- Copy your JWT session cookie and save it somewhere for later.
- Log out and log in again.
- Copy the new JWT session cookie and save this as well. You now have two valid JWTs generated by the server.

2. # Part 2 - Brute-force the server's public key
- In a terminal, run the following command, passing in the two JWTs as arguments.
```
docker run --rm -it portswigger/sig2n <token1> <token2>
```
- Note that the first time you run this, it may take several minutes while the image is pulled from Docker Hub.
- Notice that the output contains one or more calculated values of n. Each of these is mathematically possible, but only one of them matches the value used by the server. 
- In each case, the output also provides the following:
- A Base64-encoded public key in both X.509 and PKCS1 format.
- A tampered JWT signed with each of these keys.
- Copy the tampered JWT from the first X.509 entry (you may only have one).
- Go back to your request in Burp Repeater and change the path back to /my-account.
- Replace the session cookie with this new JWT and then send the request.
- If you receive a 200 response and successfully access your account page, then this is the correct X.509 key.
- If you receive a 302 response that redirects you to /login and strips your session cookie, then this was the wrong X.509 key. In this case, repeat this step using the tampered JWT for each X.509 key that was output by the script.

3. # Part 3 - Generate a malicious signing key
- From your terminal window, copy the Base64-encoded X.509 key that you identified as being correct in the previous section. Note that you need to select the key, not the tampered JWT that you used in the previous section.
- In Burp, go to the JWT Editor Keys tab and click New Symmetric Key.
- In the dialog, click Generate to generate a new key in JWK format.
- Replace the generated value for the k property with a Base64-encoded key that you just copied. Note that this should be the actual key, not the tampered JWT that you used in the previous section.
- Save the key.

4. # Part 4 - Modify and sign the token
- Go back to your request in Burp Repeater and change the path to /admin.
- Switch to the extension-generated JSON Web Token tab.
- In the header of the JWT, make sure that the alg parameter is set to HS256.
- In the JWT payload, change the value of the sub claim to administrator.
- At the bottom of the tab, click Sign, then select the symmetric key that you generated in the previous section.
- Make sure that the Don't modify header option is selected, then click OK. The modified token is now signed using the server's public key as the secret key.
- Send the request and observe that you have successfully accessed the admin panel.
- In the response, find the URL for deleting carlos (/admin/delete?username=carlos). Send the request to this endpoint to solve the lab.