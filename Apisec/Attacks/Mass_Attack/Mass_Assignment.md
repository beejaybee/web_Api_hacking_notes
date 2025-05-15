Mass Assignment vulnerabilities are present when an attacker is able to overwrite object properties that they should not be able to.

One of the ways that you can discover mass assignment vulnerabilities by finding interesting parameters in API documentation and then adding those parameters to requests. Look for parameters involved in user account properties, critical functions, and administrative actions.

Additionally, make sure to use the API as it was designed so that you can study the parameters that are used by the API provider. Doing this will help you understand the names and spelling conventions of the parameters that your target uses. If you find parameters used in some requests, you may be able to leverage those in your mass assignment attacks in other requests. 

You can also test for mass assignment blind by fuzzing parameter values within requests. Mass assignment attacks like this will be necessary when your target API does not have documentation available.

 Account registration is normally one of the first components of an API that accept user input. Once registration has been tested then you will need to target other requests that accept user input.

 The challenge with mass assignment attacks is that there is very little consistency in the parameters used between API providers. 
 
 That being said, if the API provider has some method for, say, designating accounts as administrators, they may also have some convention for creating or updating variables to make a user an administrator. Fuzzing can speed up your search for mass assignment vulnerabilities, but unless you understand your target’s variables, this technique can be a shot in the dark. Let's target crAPI for mass assignment vulnerabilities.

 The simplest form of this attack is to upgrade an account to an administrator role by adding a variable that the API provider likely uses to identify admins. 

 If you have access to admin documentation then there is a good chance that the parameters will be included in the registration requests. You can then use the discovered parameters to see if the API has any security controls preventing you from escalating a user account to an admin account.

 If you do not have admin docus, then you can do a simple test by including other key-values to the JSON POST body, such as:
"isadmin": true,
"isadmin":"true",
"admin": 1,
"admin": true, 
Any of these may cause the API to respond in a unique way indicating success or failure.

Once you attempt to a mass assignment attack on your target, you will need to analyze how the API responds

Make sure you have Param Miner installed as an extension to Burp Suite CE

Mass assignment attacks go beyond making attempts to become an administrator. You could also use mass assignment to gain unauthorized access to other organizations, for instance. If your user objects include an organizational group that allows access to company secrets or other sensitive information, you can attempt to gain access to that group. 

If you can assign yourself to other organizations, you will likely be able to gain unauthorized access to the other group’s resources. To perform such an attack, you’ll need to know the names or IDs used to identify the companies in requests. If the "org" value was a number, you could brute-force its value, like when testing for BOLA, to see how the API responds.

Do not limit your search for mass assignment vulnerabilities to the account registration process. Other API functions are capable of being vulnerable. Test other endpoints used for updating accounts, updating group information, user profiles, company profiles, and any other requests where you may be able to assign yourself additional access.

