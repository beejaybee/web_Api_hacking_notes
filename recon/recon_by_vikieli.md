The First Step to attacking any website is conducting recconaissance or simply put put gathering information on the target.

1. Manually Walking through the target

    - It will help first to manually browse through the target when starting out to know more about the target.

    - Try to uncover every feature in the application that the users can access, by browsing through every page and clicking every link

    - Access functionality that you don't normally use.

    - Sign up for the account at every privilege level

    - Then you can start a more in-depth recon process: finding out the technology and structure of an application.

2. Google Dorking
    - site: example: **site:google.com** Tells google that you want a result for a certain website
    - inurl: example: **inurl:"/api/v1" site:google.com** This is a powerful way to search for vulnerable pages on your targets
    - intitle: example: **intitle:"index of" site:google.com** Find specific strings in page title, example: you can use the this query to find file listing pages on websites
    - link: example: **link:"https://en.wikipedia.org/wiki/ReDoS"** Searches for web pages that contains a specific URLs
    - filetype: example: **filetype:log site:example.com** Searches for a specific file extension
    - wildcard("\*"): example: **site:*.example.com** You can use wildcard within searches to mean any characters or series of characters.
    - quotes: example: **"how to hack"** Adding quotes around your search terms forces an exact match
    - or(|): example **""how to hack" site:(google.com | reddit.com), Used for searching from one search or the other
    - minus: example **site:google.com -www** Used for excluding certain search terms 

    Uses cases:
    - look for all of a company's subdomain by doing **site:*.google.com**
    - You can also look for special endpoints that can lead to vulnerabilities **site:example.com inurl:app/kibana** finds a vulnerable kibana app.
    - Google can find company resources hosted by a third party online, such as Amazon S3 buckets **site:s3.amazonaws.com COMPANY_NAME** 
    - Look for special extensions that could indicate a sensitive file. In addition to .log, which often indicates log files, search for .php, cfm, asp, .jsp, and .pl
    - Finally, you can also combine search terms for a more accurate search.


    In addition to constructing your own queries, check out the Google Hacking Database (https://www.exploit-db.com/google-hacking-database/), a website that hackers and security practitioners use to share Google search queries for finding security-related information.


3. SCOPE DISCOVERY
    - A program’s scope on its policy page specifies which subdomains, products, and applications you’re allowed to attack

    - Carefully verify which of the company’s assets are in scope to avoid overstepping boundaries during the recon and hacking process.

    - For example, if example.com’s policy specifies that dev.example.com and test.example.com are out of scope, you shouldn’t perform any recon or attacks on those subdomains.

4. WHOIS and REVERSE WHOIS
    - whois example.com "This get commands get all the information of the person who registered the website
    - Use a public reverse WHOIS tool like ViewDNS.info (https://viewdns.info/reversewhois/) to conduct this search.
    - WHOIS and reverse WHOIS will give you a good set of top-level domains to work with.

5. IP Addresses
    - Another way of discovering your target’s top-level domains is to locate IP addresses
    - Find the IP address of a domain you know by running the nslookup command
        - nslookup target.com
    - Once you’ve found the IP address of the known domain, perform a reverse IP lookup
    - whois ip_address
    - Also run the whois command on an IP address, and then see if the target has a dedicated IP range by checking the NetRange field
    - An IP range is a block of IP addresses that all belong to the same organization.
    - If the organization has a dedicated IP range, any IP you find in that range belongs to that organization
    - whois -h whois.cymru.com ip_address
    

6. Certificate Parsing
    - Another way of finding hosts is to take advantage of the Secure Sockets Layer (SSL) certificates used to encrypt web traffic
    - An SSL certificate’s Subject Alternative Name field lets certificate owners specify additional hostnames that use the same certificate, so you can find those hostnames by parsing this field. Use online databases like crt.sh, Censys, and Cert Spotter to find certificates for a domain
    - https://crt.sh/?q=target.com&output=json

7. Subdomain Enumeration
    - After finding as many domains on the target as possible, locate as many subdomains on those domains as you can.
    - The best way to enumerate subdomains is to use automation
    - You can build a tool that combines the results of multiple tools to achieve the best results
    - To use many subdomain enumeration tools, you need to feed the program a wordlist of terms likely to appear in subdomains
    - You can find some good wordlists made by other hackers online
    - Daniel Miessler’s SecLists at https://github.com/danielmiessler/SecLists/ is a pretty extensive one
    - You can also use a wordlist generation tool like Commonspeak2 (https://github.com/assetnote/commonspeak2/) to generate wordlists based on the most current internet data.
    - Finally, you can combine several wordlists found online or that you generated yourself for the most comprehensive results.
    - Here’s a simple command to remove duplicate items from a set of two wordlists: **sort -u wordlist1.txt wordlist2.txt**
    - Gobuster is a tool for brute-forcing to discover subdomains, directories, and files on target web servers
    - Its DNS mode is used for subdomain bruteforcing In this mode, you can use the flag -d to specify the domain you want to brute-force and -w to specify the wordlist you want to use: **gobuster dns -d target_domain -w wordlist**
    - Once you’ve found a good number of subdomains, you can discover more by identifying patterns.
    - For example, if you find two subdomains of example.com named 1.example.com and 3.example.com, you can guess that 2.example.com is probably also a valid subdomain.
    - A good tool for automating this process is Altdns (https://github.com/infosec-au-altdns/), which discovers subdomains with names that are permutations of other subdomain names.
    - **altdns -i subdomains.txt -o data_output -w words.txt -r -s results_output.txt**
    - In addition, you can find more subdomains based on your knowledge about the company’s technology stack. For example, if you’ve already learned that example.com uses Jenkins, you can check if jenkins.example.com is a valid subdomain.
    - Also look for subdomains of subdomains. After you’ve found, say, dev.example.com, you might find subdomains like 1.dev.example.com
    - You can find subdomains of subdomains by running enumeration tools recursively: add the results of your first run to your Known Domains list and run the tool again.
    
8. Service Enumeration
    - Next, enumerate the services hosted on the machines you’ve found.
    - A good way to find them is by port-scanning the machine with either active or passive scanning.
    - You can use tools like Nmap or Masscan for active scanning
    - For example, this simple Nmap command reveals the open ports on browserstack
    - **nmap browserstack.com**
    - In the other hand, in passive scanning, you use third-party resources to learn about a machine’s ports without interacting with the server
    - Passive scanning is stealthier and helps attackers avoid detection
    - Alternatives to Shodan include Censys and Project Sonar
    - With these databases, you might also find your target’s IP addresses, certificates, and software versions.
9. Directory Brute-Forcing
    - The next thing you can do to discover more of the site’s attack surface is brute-force the directories of the web servers you’ve found
    -Finding directories on servers is valuable, because through them, you might discover hidden admin panels, configuration files, password files, outdated functionalities,database copies, and source code files.
    - Directory brute-forcing can sometimes allow you to directly take over a server!
    - Even if you can’t find any immediate exploits, directory information often tells you about the structure and technology of an application.
    - For example, a pathname that includes phpmyadmin usually means that the application is built with PHP
    - You can use Dirsearch or Gobuster for directory brute-forcing
    - These tools use wordlists to construct URLs, and then request these URLs from a web server
    - If the server responds with a status code in the 200 range, the directory or file exists
    - To run dirsearch make sure you activate the venv environment
    - Example code to run **python3 dirsearch.py -u https://browserstack.com**
    - **python3 dirsearch.py -u https://browserstack.com -e php"**
    - Gobuster’s Dir mode is used to find additional content on a specific domain or subdomain
    - In this mode, you can use the -u flag to specify the domain or subdomain you want to brute-force and -w to specify the wordlist you want to use: **gobuster dir -u target_url -w wordlist**
    - Manually visiting all the pages you’ve found through brute-forcing can be time-consuming. 
    - Instead, use a screenshot tool like EyeWitness (https://github.com/FortyNorthSecurity/EyeWitness/) or Snapper (https://github.com/dxa4481/Snapper/) to automatically verify that a page is hosted on each location.
    - EyeWitness accepts a list of URLs and takes screenshots of each page
    - In a photo gallery app, you can quickly skim these to find the interesting-looking ones.
    - Keep an eye out for hidden services, such as developer or admin panels, directory listing pages, analytics pages, and pages that look outdated and ill-maintained.
    - These are all common places for vulnerabilities to manifest
    
10. Spidering the website
    - Another way of discovering directories and paths is through web spidering, or web crawling, a process used to identify all pages on a site
    - A web spider tool starts with a page to visit.
    - It then identifies all the URLs embedded on the page and visits them.
    - By recursively visiting all URLs found on all pages of a site, the web spider can uncover many hidden endpoints in an application.
    - OWASP Zed Attack Proxy (ZAP) has a built-in web spider you can use
    - Access its spider tool by opening ZAP and choosing Tools > Spider
    - You should see a window for specifying the starting URL
    - You should also see a site tree appear on the left side of your ZAP window
    - This shows you the files and directories found on the target server in an organized format.

11. Third-party Hosting
    - Take a look at the company’s third-party hosting footprint. For example, look for the organization’s S3 buckets.         
    - S3, which stands for Simple Storage Service, is Amazon’s online storage product.
    - Organizations can pay to store resources in buckets to serve in their web applications, or they can use S3 buckets as a backup or storage location.
    - If an organization uses Amazon S3, its S3 buckets can contain hidden endpoints, logs, credentials, user information, source code, and other information that might be useful to you
    - Most buckets use the URL format BUCKET.s3.amazonaws.com or s3.amazonaws.com/BUCKET, so the following search terms are likely to find results: **site:s3.amazonaws.com COMPANY_NAME**, **site:amazonaws.com COMPANY_NAME**
    - If the company uses custom URLs for its S3 buckets, try more flexible search terms instead. Companies often still place keywords like aws and s3 in their custom bucket URLs, so try these searches:
    - amazonaws s3 COMPANY_NAME
    - amazonaws bucket COMPANY_NAME
    - amazonaws COMPANY_NAME
    - s3 COMPANY_NAME
    - Another way of finding buckets is to search a company’s public GitHub repositories for S3 URLs.
    - Try searching these repositories for the term s3.
    - rayhatWarfare (https://buckets.grayhatwarfare.com/) is an online search engine you can use to find publicly exposed S3 buckets
    - It allows you to search for a bucket by using a keyword. Supply keywords related to your target, such as the application, project, or organization name, to find relevant buckets.
    - Finally, you can try to brute-force buckets by using keywords
    - Lazys3 (https://github.com/nahamsec/lazys3/) is a tool that helps you do this.
    - It relies on a wordlist to guess buckets that are permutations of common bucket names
    - Once you’ve found a couple of buckets that belong to the target organization, use the AWS command line tool to see if you can access one.
    - Install the tool by using the following command: **pip install awscli**
    - Then configure it to work with AWS by following Amazon’s documentation at https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html
    - Now you should be able to access buckets directly from your terminal via the aws s3 command.
    - Try listing the contents of the bucket you found: **aws s3 ls s3://BUCKET_NAME/**
    - If this works, see if you can read the contents of any interesting files by copying files to your local machine: **aws s3 cp s3://BUCKET_NAME/FILE_NAME/path/to/local/directory**
    - Gather any useful information leaked via the bucket and use it for future exploitation!
    - If the organization reveals information such as active API keys or personal information, you should report this right away.
    - Exposed S3 buckets alone are often considered a vulnerability.
    - You can also try to upload new files to the bucket or delete files from it.
    - For example, this command will copy your local file named TEST_FILE into the target’s S3 bucket: **aws s3 cp TEST_FILE s3://BUCKET_NAME/**
    - And this command will remove the TEST_FILE that you just uploaded:**aws s3 rm s3://BUCKET_NAME/TEST_FILE**
    - These commands are a harmless way to prove that you have write access to a bucket without actually tampering with the target company’s files.
    - Always upload and remove your own test files. Don’t risk deleting important company resources during your testing unless you’re willing to entertain a costly lawsuit
    
12. Github Recon
    - Search an organization’s GitHub repositories for sensitive data that has been accidentally committed, or information that could lead to the discovery of a vulnerability.
    - Start by finding the GitHub usernames relevant to your target.
    - You should be able to locate these by searching the organization’s name or product names via GitHub’s search bar, or by checking the GitHub accounts of known employees
    - When you’ve found usernames to audit, visit their pages. Find repositories related to the projects you’re testing and record them, along with the usernames of the organization’s top contributors, which can help you find more relevant repositories.
    - Then dive into the code. For each repository, pay special attention to the Issues and Commits sections.
    - These sections are full of potential info leaks: they could point attackers to unresolved bugs, problematic code, and the most recent code fixes and security patches.
    - Recent code changes that haven’t stood the test of time are more likely to contain bugs.
    - Look at any protection mechanisms implemented to see if you can bypass them.
    - You can also search the Code section for potentially vulnerable code snippets.
    - You can also search the Code section for potentially vulnerable code snippets. 
    - Once you’ve found a file of interest, check the Blame and History sections at the top-right corner of the file’s page to see how it was developed.
    - Search the organization’s repositories for terms like key, secret, and password to locate hardcoded user credentials that you can use to access internal systems
    - After you’ve found leaked credentials, you can use KeyHacks (https://github.com/streaak/keyhacks/) to check if the credentials are valid and learn how to use them to access the target’s services.
    - You should also search for sensitive functionalities in the project.
    - See 
    - if any of the source code deals with important functions such as authentication, password reset, state-changing actions, or private info reads.
    - Pay attention to code that deals with user input, such as HTTP request parameters, HTTP headers, HTTP request paths, database entries, file reads, and file uploads, because they provide potential entry points for attackers to exploit the application’s vulnerabilities.
    - Look for any configuration files, as they allow you to gather more information about your infrastructure.
    - Also, search for old endpoints and S3 bucket URLs that you can attack. Record these files for further review in the future.
    - Outdated dependencies and the unchecked use of dangerous functions are also a huge source of bugs.
    - Pay attention to dependencies and imports being used and go through the versions list to see if they’re outdated. Record any outdated dependencies.
    - You can use this information later to look for publicly disclosed vulnerabilities that would work on your target.
    - Tools like Gitrob and TruffleHog can automate the GitHub recon process.
    - Gitrob (https://github.com/michenriksen/gitrob/) locates potentially sensitive files pushed to public repositories on GitHub.
    - TruffleHog (https://github.com/trufflesecurity/truffleHog/) specializes in finding secrets in repositories by conducting regex searches and scanning for high-entropy strings
    
13. Other Sneaky OSINT Techniques
    - First, check the company’s job posts for engineering positions. Engineering job listings often reveal the technologies the company uses. For example, take a look at an ad like this one:
    - Full Stack Engineer
        - Minimum Qualifications:
        - Proficiency in Python and C/C++
        - Linux experience
        - Experience with Flask, Django, and Node.js
        - Experience with Amazon Web Services, especially EC2, ECS, S3, and RDS
    - From reading this, you know the company uses Flask, Django, and Node.js to build its web applications. 
    - The engineers also probably use Python, C, and C++ on the backend with a Linux machine. Finally, they use AWS to outsource their operations and file storage.
    -If you can’t find relevant job posts, search for employees’ profiles on LinkedIn, and read employees’ personal blogs or their engineering questions on forums like Stack Overflow and Quora.
    - The expertise of a company’s top employees often reflects the technology used in development.
    - Another source of information is the employees’ Google calendars. 
    - People’s work calendars often contain meeting notes, slides, and sometimes even login credentials
    - If an employee shares their calendars with the public by accident, you could gain access to these.
    - The organization or its employees’ social media pages might also leak valuable information.
    - If the company has an engineering mailing list, sign up for it to gain insight into the company’s technology and development process.
    - Also check the company’s SlideShare or Pastebin accounts. 
    - Sometimes, when organizations present at conferences or have internal meetings, they upload slides to SlideShare for reference. 
    - You might be able to find information about the technology stack and security challenges faced by the company
    - Pastebin (https://pastebin.com/) is a website for pasting and storing text online for a short time.- People use it to share text across machines or with others. 
    - Engineers sometimes use it to share source code or server logs with their colleagues for viewing or collaboration, so it could be a great source of information.
    - You might also find uploaded credentials and development comments. 
    - Go to Pastebin, search for the target’s organization name, and see what happens! 
    - You can also use automated tools like PasteHunter (https://github.com/kevthehermit/PasteHunter/) to scan for publicly pasted data.
    - Lastly, consult archive websites like the Wayback Machine (https://archive.org/web/).
    - Using the Wayback Machine, you can find old endpoints, directory listings, forgotten subdomains, URLs, and files that are outdated but still in use
    - Tomnomnom’s tool Waybackurls (https://github.com/tomnomnom/waybackurls/) can automatically extract endpoints and URLs from the Wayback Machine.

14. Tech Stack Fingerprinting
    - Fingerprinting techniques can help you understand the target application even better.
    - Fingerprinting is identifying the software brands and versions that a machine or an application uses. 
    - This information allows you to perform targeted attacks on the application, because you can search for any known misconfigurations and publicly disclosed vulnerabilities related to a particular version.
    - For example, if you know the server is using an old version of Apache that could be impacted by a disclosed vulnerability, you can immediately attempt to attack the server using it
    - The security community classifies known vulnerabilities as Common Vulnerabilities and Exposures (CVEs) and gives each CVE a number for reference. 
    - Search for them on the CVE database (https://cve.mitre.org/cve/search_cve_list.html).
    - The simplest way of fingerprinting an application is to engage with the application directly
    - First, run Nmap on a machine with the -sV flag on to enable version detection on the port scan. 
    - Here, you can see that Nmap attempted to fingerprint some software running on the target host for us: **nmap scanme.nmap.org -sV**
    - Next, in Burp, send an HTTP request to the server to check the HTTP headers used to gain insight into the tech stack
    - A server might leak many pieces of information useful for fingerprinting its technology
    - The HTML source code of web pages can also provide clues. 
    - Many web frameworks or other technologies will embed a signature in source code. 
    - Right-click a page, select View Source Code, and press CTRL-F to search for phrases like powered by, built with, and running. For instance, you might find Powered by: WordPress 3.3.2 written in the source
    - Check technology-specific file extensions, filenames, folders, and directories. 
    - For example, a file named phpmyadmin at the root directory, like https://example.com/phpmyadmin, means the application runs PHP. 
    - A directory named jinja2 that contains templates means the site probably uses Django and Jinja2. 
    - You can find more information about a specific technology’s filesystem signatures by visiting its individual documentation.
    - Several applications can automate this process. 
    - Wappalyzer (https://www.wappalyzer.com/) is a browser extension that identifies content management systems, frameworks, and programming languages used on a site. 
    - BuiltWith (https://builtwith.com/) is a website that shows you which web technologies a site is built with. 
    - StackShare (https://stackshare.io/) is an online platform that allows developers to share the tech they use. You can use it to find out if the organization’s developers have posted their tech stack.
    - Retire.js is a tool that detects outdated JavaScript libraries and Node.js packages. 
    - You can use it to check for outdated technologies on a site.


# ADVICE FROM VICKIE LI

*But when you’re starting out, I recommend that you do recon manually with individual tools or write your own automated recon scripts to learn about the process.*

