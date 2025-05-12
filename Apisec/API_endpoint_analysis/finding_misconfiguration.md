Once you've found an API and used it as intended, you can use it to form your baseline vulnerability scan.

To find security misconfiguration, use tools like nikto or zapproxy

# NIKTO
run
    - nikto -h http://yourtarget

this is a general test, You can do this for different subdomains and api you find

# Scanning API with OWASP ZAP
## Automatic run
    - You can import the spec.yml file into zap proxy and add the host target
    - Then click on active scan
## Manual Approach
    - Set the your target into zap proxy and click on launch firefox
    - Once on firefox, browse through all the possible buttons and forms you can come accross on the website, make sure you have gone through all the links and request.
    - Then go back to zap and you will notice you request are saved in zap
    - right click on your host context and click attack, wait till it completes the attack
    - Examine the alarts one after the other
    - Work through the results and determine which one is an actual finding



