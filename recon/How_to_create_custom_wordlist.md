# Talk By tomnomnom

Wordlist exist to save time and resources

# Where can wordlist be used
- subdomain enumeration
- Path Guessing
- Authentication Gussing
- API method guessing
- Parameter guessing
- Header Guessing


# Write out the worlds yourself

# Tools to use 
## gau GET ALL URLS
    - gau site.com
## webpaste by tomnomnom
    - Webpaste allow you to copy google dorks 
    - webpaste -o site.txt

After getting all the link, you need to get the worldlists 
# tools to use
    - unfurl
        - This tool will get the paths, domain, or any other part of the links
    - How to use
        - cat inurl_api | unfurl -u paths > new_path
    - Then use sed to separate all the words like this
        - sed 's#/#\n#g' new_path | sort -u  
# Other Tools
    - CURL
        - curl https://www.browserstack.com > browserstack.html
    - then use the following to get the worldlist
        - cat browserstack.html | tok | tr '[:upper:]' '[:lower:]' | sort -u > browserwordlist
    - gau & fff
        - gau browserstack.com | head -n 1000 | fff -S 200 -S 404 --output browserstack_new
    - html-tool
        - find out -type f -name '*.body' | html-tool attribs src | grep '\.js$' 
 
# Wordlist complete
