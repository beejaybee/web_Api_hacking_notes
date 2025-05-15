#     BROKEN OBJECT LEVEL AUTHORIZATION

## When hunting for BOLA there are three ingredients needed for successful exploitation.

** Resource ID: a resource identifier will be the value used to specify a unique resource. This  could be as simple as a number, but will often be more complicated.
Resource ID could be:
    - Can be number
    - Can be group name
    - Can be company name
    - Can be a combo
    - Can be unguessable or unbrutable string

** Requests that access resources. In order to test if you can access another user's resource, you will need to know the requests that are necessary to obtain resources that your account should not be authorized to access.
** Missing or flawed access controls. In order to exploit this weakness, the API provider must not have access controls in place. This may seem obvious, but just because resource IDs are predictable, does not mean there is an authorization vulnerability present.

**The third item on the list is something that must be tested, while the first two are things that we can seek out in API documentation and within a collection of requests. Once you have the combination of these three ingredients then you should be able to exploit BOLA and gain unauthorized access to resources.** 

# Check Image.png to see how to test

# AUTHORIZATION TESTING STRATEGIES

When searching for authorization vulnerabilities the most effective way to find authorization weaknesses is to create two accounts and perform A-B testing. The A-B testing process consists of:

    1. Create a UserA account.
    2. Use the API and discover requests that involve resource IDs as UserA.
    3. Document requests that include resource IDs and should require authorization.
    4. Create a UserB account.
    5. Obtaining a valid UserB token and attempt to access UserA's resources.

You could also do this by using UserB's resources with a UserA token.
