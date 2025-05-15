# Finding hidden parameters

When you're doing API recon, you may find undocumented parameters that the API supports. You can attempt to use these to change the application's behavior. Burp includes numerous tools that can help you identify hidden parameters:

    Burp Intruder enables you to automatically discover hidden parameters, using a wordlist of common parameter names to replace existing parameters or add new parameters. Make sure you also include names that are relevant to the application, based on your initial recon.

    The Param miner BApp enables you to automatically guess up to 65,536 param names per request. Param miner automatically guesses names that are relevant to the application, based on information taken from the scope.

    The Content discovery tool enables you to discover content that isn't linked from visible content that you can browse to, including parameters.

# Mass assignment vulnerabilities

Mass assignment (also known as auto-binding) can inadvertently create hidden parameters. It occurs when software frameworks automatically bind request parameters to fields on an internal object. Mass assignment may therefore result in the application supporting parameters that were never intended to be processed by the developer.


# Identifying hidden parameters

Since mass assignment creates parameters from object fields, you can often identify these hidden parameters by manually examining objects returned by the API.

For example, consider a PATCH /api/users/ request, which enables users to update their username and email, and includes the following JSON:
{
    "username": "wiener",
    "email": "wiener@example.com",
}

**A concurrent GET /api/users/123 request returns the following JSON:**
{
    "id": 123,
    "name": "John Doe",
    "email": "john@example.com",
    "isAdmin": "false"
}

This may indicate that the hidden id and isAdmin parameters are bound to the internal user object, alongside the updated username and email parameters.

# LAB
To solve the lab, find and exploit a mass assignment vulnerability to buy a Lightweight l33t Leather Jacket. You can log in to your own account using the following credentials: wiener:peter. 

## To solve this lab
- Browse Through the APP
- Check for API endpoints 
- Look for POST request
- Check for API documentation
- Forge request based on the endpoint in the documentation
- You can also check the GET method and check for parameters not present in the POST request.
- Add it to the POST Request


