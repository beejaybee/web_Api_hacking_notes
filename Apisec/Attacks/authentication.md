# First thing to do
## Check the request and response for the following
    - Check password requirements or token requirements first
    - Once length password/token requirements is confirmed, send the request
    - Send good request and check for the:
        - Response Status
        - Content Lenght header
        - Check what is in the header
    - Once You understood everything in good request, send the bad request too and check for the above checklists
    - Then send request to intruder or turbo intruder in burpsuite if you don't have burp pro


## Using wfuzz
wfuzz -d '{"email":"a@email.com","password":"FUZZ"}' -H 'Content-Type: application/json' -z file,/usr/share/wordlists/rockyou.txt -u http://127.0.0.1:8888/identity/api/auth/login --hc 405
