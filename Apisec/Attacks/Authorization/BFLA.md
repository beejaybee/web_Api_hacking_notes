#          BROKEN FUNCTION LEVEL AUTHORIZATION
 This is just like BOLA but it is mainly performing action and not getting information

 Where BOLA is all about accessing resources that do not belong to you, BFLA is all about performing unauthorized actions. BFLA vulnerabilities are common for requests that perform actions of other users

 These requests could be lateral actions or escalated actions. Lateral actions are requests that perform actions of users that are the same role or privilege level. Escalated actions are requests that perform actions that are of an escalated role like an administrator. 

 The main difference between hunting for BFLA is that you are looking for functional requests. This means that you will be testing for various HTTP methods, seeking out actions of other users that you should not be able to perform.

## For BFLA we will be hunting for very similar requests to BOLA.

    - Resource ID: a resource identifier will be the value used to specify a unique resource. 
    - Requests that perform authorized actions. In order to test if you can access another update, delete, or otherwise alter other the resources of other users.
    - Missing or flawed access controls. In order to exploit this weakness, the API provider must not have access controls in place. 