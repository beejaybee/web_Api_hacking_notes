# SUBDOMAIN enumeration

## Link Discovery
# TOOLS TO USE
# Gospider gospider -h
    - gospider -s https://site.com
# Hakwraler hakwraler -h
    - echo site.com | hakwraler
    - cat site_lists.txt | hakwraler
    - check https://github.com/hakluke/hakrawler for more 

# SUBDOMAIN FINDER
 ## subscraper
    - subscraper -d site.com
    - thehavester
        - theHarvester -d browserstack.com -b all -l 100 -t 
    - dns_parallel_prober

## SUBDOMAIN SCRAPING
#    Tools
    - Google dorks
        - Start with site:target.com and minus everything youve seen to find more until you did not find anything again
        - site:browserstack.com -www.browserstack.com
    - Amass
        - amass enum -d browserstack.com
        - amass enum -active -d browserstack.com
        - amass enum -passive -d browserstack.com
    - subfinder
        - subfinder -d browserstack.com
    - github-subdomains requires githuh token
        - github-subdomains -d browserstack.com
    - shosubgo requires shodan token | and only for members
        - shosubgo -d browserstack.com -s shodantoken

## SUBOMAIN BRUTEFORCE
#   Tools
        - Amass
            - amass enum -brute -d browserstack.com
            - amass enum -brute -d browserstack.com -rf ~/resolver.txt -w google_dorking/wordlist > amass_resolver
## SUBDOMAIN PERMUTATION
#   TOOLS
        - altdns

## PORT ANALYSIS (MASSCAN) takes in IP addresses only
    - masscan -p1-65535 -iL $InPutfile --max-rate 1800 -oG $outputFile
    - I have put this command inside mass.sh file, which allows us to massscan domain
    - I have also done something like this
        - dnmasscan browserstack.com.txt dns.log -p80,443 -oG masscan.log 

## NMAP
    nmap -sSV -p- -iL targets.txt -oA output_syn --min-parallelism 64 --min-hostgroup 96\ -T4 --version-all --reason --open

## SERVICE SCANNING (BRUTESPRAY)
# TOOLS
    - brutespray
## PROBE WITH HTTPROBE and httpx
    - cat subdomain.txt | httprobe 
    - cat subs.txt | httpx -silent -status-code -title -tech-detect
## SCREENSHOTING 
#   TOOLS
    - AQUATONE
        - 

# SUBDOMAIN TAKEOVER

RECON & APPLICATION ANALYSIS

1. Find Scope domains
2. Find Acquisition (If applicable)
3. Enumerate ASNs
4. Reverse whois
5. SUBDOMAIN ENUMERATION
6. PORT ANALYSIS
7. Others
