Testing for Improper Assets Management is all about discovering unsupported and non-production versions of an API.

Often times an API provider will update services and the newer version of the API will be available over a new path like the following:

api.target.com/v3
/api/v2/accounts
/api/v3/accounts
/v2/accounts
API versioning could also be maintained as a header:

Accept: version=2.0
Accept api-version=3
In addition versioning could also be set within a query parameter or request body.

/api/accounts?ver=2
POST /api/accounts

{
"ver":1.0,
"user":"hapihacker"
}

Finding versions that are not included in API documentation will be at best a vulnerability for insufficient technical documentation (CWE-1059) and at worst a gateway to more severe findings and the compromise of the provider. 

You can discover mass assignment vulnerabilities by finding interesting parameters in API documentation and then adding those parameters to requests. Look for parameters involved in user account properties, critical functions, and administrative actions. Intercepting API requests and responses could also reveal parameters worthy of testing. Additionally, you can guess parameters or fuzz them in API requests that accept user input. I recommend seeking out registration processes that allow you to create and/or edit account variables. 

# Test for Improper Asset Management

1. Understand the baseline versioning information of the API you are testing. Make sure to check out the path, parameters, and headers for any versioning information.

2. To get better results from the Postman Collection Runner, we’ll configure a test using the Collection Editor. Select the crAPI collection options, choose Edit, and select the Tests tab. Add a test that will detect when a status code 200 is returned so that anything that does not result in a 200 Success response may stick out as anomalous. You can use the following test:

```pm.test("Status code is 200", function () { pm.response.to.have.status(200); })```

3. Run an unauthenticated baseline scan of the crAPI collection with the Collection Runner. Make sure that "Save Responses" is checked as seen below

4. Review the results from your unauthenticated baseline scan to have an idea of how the API provider responds to requests using supported production versioning.

5. Next, use "Find and Replace" to turn the collection's current versions into a variable. Type the current version into "Find", update "Where" to the targeted collection, and update "Replace With" to a variable.

6. If that doesn't work, then you have to do it manually

7. Open Postman and navigate to the environmental variables (use the eye icon located at the top right of Postman as a shortcut). Note, we are using environmental variables so that this test can be accessed and reused for other API collections. Add a variable named "ver" to your Postman environment and set the initial value to "v1". Now you can update to test for various versioning-related paths such as v1, v2, v3, mobile, internal, test, and uat. As you come across different API versions expand this list of variables.

8. Now that the environmental variable is set to v1 use the collection runner again and investigate the results. You can drill down into any of the requests by clicking on them.

9. COntinue this process until you find anomalies in the result

10. Run different vulnerability checks on any valid version you find

11. Run the Test for authenticated baseline too and check for anomalies in the result.

**wfuzz -d '{"email":"hapihacker@email.com", "otp":"FUZZ","password":"NewPassword1"}' -H 'Content-Type: application/json' -z file,/usr/share/wordlists/SecLists-master/Fuzzing/4-digits-0000-9999.txt -u http://crapi.apisec.ai/identity/api/auth/v2/check-otp --hc 500**