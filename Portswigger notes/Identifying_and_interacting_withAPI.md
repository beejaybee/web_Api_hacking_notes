
# Interacting with API endpoints

Once you've identified API endpoints, interact with them using Burp Repeater and Burp Intruder. This enables you to observe the API's behavior and discover additional attack surface. For example, you could investigate how the API responds to changing the HTTP method and media type.

As you interact with the API endpoints, review error messages and other responses closely. Sometimes these include information that you can use to construct a valid HTTP request.

# Identifying supported HTTP methods

The HTTP method specifies the action to be performed on a resource. For example:

    GET - Retrieves data from a resource.
    PATCH - Applies partial changes to a resource.
    OPTIONS - Retrieves information on the types of request methods that can be used on a resource.

An API endpoint may support different HTTP methods. It's therefore important to test all potential methods when you're investigating API endpoints. This may enable you to identify additional endpoint functionality, opening up more attack surface.

For example, the endpoint /api/tasks may support the following methods:

    GET /api/tasks - Retrieves a list of tasks.
    POST /api/tasks - Creates a new task.
    DELETE /api/tasks/1 - Deletes a task.

 You can use the built-in HTTP verbs list in Burp Intruder to automatically cycle through a range of methods.
Note

When testing different HTTP methods, target low-priority objects. This helps make sure that you avoid unintended consequences, for example altering critical items or creating excessive records.


# Identifying supported content types

API endpoints often expect data in a specific format. They may therefore behave differently depending on the content type of the data provided in a request. Changing the content type may enable you to:

    Trigger errors that disclose useful information.
    Bypass flawed defenses.
    Take advantage of differences in processing logic. For example, an API may be secure when handling JSON data but susceptible to injection attacks when dealing with XML.

To change the content type, modify the Content-Type header, then reformat the request body accordingly. You can use the Content type converter BApp to automatically convert data submitted within requests between XML and JSON.

# LAB

## Finding and exploiting an unused API endpoint

To solve the lab, exploit a hidden API endpoint to buy a Lightweight l33t Leather Jacket. You can log in to your own account using the following credentials: wiener:peter. 

## To solve this lab:

- You need to Browse through the app and look for apis
- Send API endpoints to burp repeater
- Find any API endpoint that has to do with the Lightweight 133t Leather Jacket
- If GET method, send the request and study the response
- Change the request method to OPTIONS to see allowed method
- Study the response and forge your request with the HTTP methods
- Send the forge requests and notice the response errors
- Used the new errors to forge the new request
- change price to 0, to buy the jacket   

# Using Intruder to find hidden endpoints

Once you have identified some initial API endpoints, you can use Intruder to uncover hidden endpoints. For example, consider a scenario where you have identified the following API endpoint for updating user information:

PUT /api/user/update

To identify hidden endpoints, you could use Burp Intruder to find other resources with the same structure. For example, you could add a payload to the /update position of the path with a list of other common functions, such as delete and add.

When looking for hidden endpoints, use wordlists based on common API naming conventions and industry terms. Make sure you also include terms that are relevant to the application, based on your initial recon.


