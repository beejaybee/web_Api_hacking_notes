# 2023 OWASP API SECURITY TOP 10

## 1. Broken object level authorization
    - Also Known as BOLA
    - Most Common and damaging API vulnerability
    - Manipulation of Objects/data belonging to other users
### Example
    Attacker authenticate as user A and the retrieves user B's data
### Prevention
    Define data Access policies and implement associated controls
    Enforce data access controls at application logic layer
    Implement Automated testing to find BOLA flaws

## 2. Broken Authenication
### Description
    - Weak or poor authentication creates
        1. Missing security controls
        2. Poorly implemented Controls
### Risk Exposure
    - Account takeover
    - Data theft, unauthorize transaction
### Examples
    - Weak password requirements
    - Credential stuffing: brute force ID/password
    - No captcha/rate limiting/ lockout
    - Auth Infos in URLs (token, password)
    - Non validation of token expiration
    - Insecure Password storage
### Prevention
    - Define Authentication policies and best practice: follow best practices
    - Implement continous testting


## 3. Broken Object Property Level Authorization
### Description
    - Exploits of endpoints by reaading  and/or modifying values of objects
    - Ability to update object elements ("Mass assignment)
    - Revealing unneccessary sensitive data (Excessive data exposure)
### Risk Exposure
    - Revealin protected user
### Example
    - User is able to set "account-type: premium"
    - User search endpoints and returns excessive, unnecessary details
### Prevention 
    - Ensure you can only access legitimate, permitted field
    - Return Only minimum amount of data for the use case

## 4. unrestricted resource consumption
### Description
    - Abuse of API due to high  volumes of API calls, large requests etc.
    - Formerly Lack of resource and rate limiting
### Risk Exposure
    - Denial of service
    - Performance impact
    - Mass data harvesting
### Examples
    - Missing/inadequates rate controls
    - Execution
    - Max allocable memory
    - Max numbers of files, upload size
    - Excessive operations in single request
    - Excessive records returned in single request
### Prevention 
    - Implementation
    - Test effectiveness


## 5. Broken Function Level Authorization
### Description
    - Abuse of API functionality to improperly  modify objects (create, update, delete)
    - Often involves replacing passive methods GET with (PUT, DELETE)
### Risk Exposure
    - May be used to escalate privilege
    - Can be exploited to modify account details
### Examples
    - Modify Parameters -> role = admin
    - Delete an invoice
    - Set account Balance
### Prevention
    - Identify functions that expose sensitive capability  and develop controls to limit access
    - Implement continous release testing to ensure proper behaviour 

## 6. Unrestricted access to sensitive business flows
### Description
    - Abuse of a legimate business workflow through excessive, automated use
    - Rate limiting, captchas not always effective against fraudulent traffic 
    - Rapid IP rotation makes detection  difficult
    - Typically a result of Application logic flaw
### Example
    - Mass, Automated ticket purchasing
    - High volume referal bonuses
### Prevention
    - Identify critical business workflows
    - Implement fraudulent traffic detection and control
    - Setup and automate testing of control  mechanism


## 7. Server-side-request-forgery
### Description
    - Exploiting URL inputs to make  a request to a 3rd party server
### Risk Exposure
    - SSRF creates a channel for malicious requests, data access or other fraudulent activity
    - potential for data leaks
### Example
    - Local File Injection (LFI)
### Prevention
    - Validate and sanitize all user supplied information, including URL parameters


## 8. Security misconfiguration
### Description
    - Broad category, encompasses lack of hardening to unnecessary services
    - Use of bots to scan, detect and exploit misconfigurations 
### Risk Exposure
    - Misconfiguration can expose sensitive user data
    - Potential for full server compromise
### Example
    - Lack of security hardening
    - Improper configured permissions
    - Missing Security patched
    - Unnecessary features available
    - Missing TLS
    - CORS policy missing/improperly set
### Prevention
    - Implement Hardening procedure
    - ROutinely review configurations
    - Implement automated, continous security testing

## 9. Improper Inventory Management
### Description
    - Unauthorised API access via old, unused API versions, or through  trusted 3rd parties 
### Risk Exposure
    - Data/account theft via unretired APIs
    - Exposure of Sensitive Data via improperly secured 3rd parties API
### Example
    - Old versions of API
    - Unpatched endpoints
    - Endpoints with weaker security
    - Outdated documentation
    - unncessary expposed endpoints
    - API access via 3rd parties
### Prevention
    - Deploy/manage all APIs in Gateway
    - Define rules for versioning  and retirement
    - Periodically audit 3rd party access


## 10. Unsafe consumption of APIs
### Description
    - Consuming 3rd parties API can be really dangerous if consuming in unsafe way
### Risk Exposure
    
### Example
    
### Prevention


