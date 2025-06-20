1. Find Scope domains
# Find Seeds/Root Domains
https://cdp*.browserstack.com
35.202.184.41
35.202.19.5
35.226.127.204
104.154.145.167
https://docs.percy.io/docs/enterprise-firewalls

https://turn*.browserstack.com
https://repeater*.browserstack.com
api-cloud.browserstack.com

https://www.browserstack.com/docs/automate/api-reference/selenium/introduction
https://www.browserstack.com/docs/app-automate/api-reference/introduction
https://www.browserstack.com/app-live/rest-api

https://*rproxy*.browserstack.com
geo-uploader.browserstack.com
https://geo-uploader*.browserstack.com
https://upload*.browserstack.com

api.browserstack.com
https://github.com/browserstack/api

https://hub*.browserstack.com
automate.browserstack.com

live.browserstack.com
https://www.browserstack.com/docs/live

app-live.browserstack.com
https://www.browserstack.com/docs/app-live

app-automate.browserstack.com
https://www.browserstack.com/docs/app-automate/appium
https://www.browserstack.com/docs/app-automate/espresso/getting-started
https://www.browserstack.com/docs/app-automate/xcuitest/getting-started
https://www.browserstack.com/docs/app-automate/earlgrey/getting-started

*.browserstack.com
## out of scope
Alpha/Beta Products
Alpha/Beta Functionalities in existing in scope products
Products Integration with 3rd Party Apps. Eg (Jira, Slack integration)
BrowserStack Acquisitions
Third Party applications - This includes any BrowserStack subdomain pointed to applications that belong to third party services.

*.percy.io
browserstack.com

2. Found Acquisition (Not Applicable)

3. Enumerate ASNs 
    - https://bgp.he.net/
        - AS136662
        - 103.95.100.0/24
        - 102.165.49.0/24
    - metabigor
        - echo browserstack | metabigor net --org -v
            - 136662 - 103.95.100.0/24 - BSTACK-AS Browserstack Software Pvt Ltd - IN
    - nslookup
        - nslookup browserstack.com            
            -   Server:         10.0.2.3
                Address:        10.0.2.3#53

                Non-authoritative answer:
                Name:   browserstack.com
                Address: 44.219.129.14
                Name:   browserstack.com
                Address: 44.194.131.149
                Name:   browserstack.com
                Address: 54.225.178.104
                Name:   browserstack.com
                Address: 52.86.22.150
        - nslookup percy.io                         
            -   Server:         10.0.2.3
                Address:        10.0.2.3#53

                Non-authoritative answer:
                Name:   percy.io
                Address: 104.22.7.36
                Name:   percy.io
                Address: 172.67.20.231
                Name:   percy.io
                Address: 104.22.6.36

Now we can do:
    - amass intel -asn 136662 
    - nothing came back from the asn

4. whoxy.com did not return anything meaninful for browserstack

5. Builtwith
    - ruby_on_rails
    - Amazon_s3
    - cloudflare
    - stripe
    - sentry
    - jquery_3.5.1
    - core_js
    - React
    - wpengine
    - nginx
    - percy -- github hosting
6. Finding subdomains
    - Linked and javascript discovery
        - Gospider
            - gospider -s https://browserstack.com
    - Subdomain scraping
    - Subdomain bruteforce

