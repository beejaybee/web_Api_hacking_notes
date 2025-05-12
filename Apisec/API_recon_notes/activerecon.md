# NMAP
Nmap is a powerful tool for scanning ports, searching for vulnerabilities, enumerating services, and discovering live hosts.

## $ nmap -sC -sV [target address or network range] -oA nameofoutput

## nmap -sC -sV 127.0.0.1

## nmap -p- 127.0.0.1 | $ nmap -p- [target address] -oA allportscan

## nmap sV 127.0.0.1 -p 8025

Once you discover a web server, you can perform HTTP enumeration using a Nmap NSE script (use -p to specify which ports you'd like to test).

## $ nmap -sV --script=http-enum <target> -p 80,443,8000,8080


# AMASS

## amass enum -list || This will get you what api key youve installed for amass to use
## amass enum -active -d target-name.com | grep api
## $ amass intel -addr [target IP addresses]
## $ amass intel -d [target domain] –whois
## amass enum -active -d target-name.com | grep api
## $ amass intel -d [target domain] –whois ||| for passive scan 
## $ amass enum -passive -d [target domain]
## $ amass enum -active -d [target domain]

## $ amass enum -active -brute -w /usr/share/wordlists/API_superlist -d [target domain] -dir [directory name]  

# Gobuster
## gobuster dir -u [target domain] -w /usr/share/dirbuster/wordlists/directory-list-2.3-medium.txt -b 404
## $ gobuster dir -u ://targetaddress/ -w /usr/share/wordlists/api_list/common_apis_160 -x 200,202,301 -b 302


# kiterunner

##  kr scan HTTP://127.0.0.1 -w ~/api/wordlists/data/kiterunner/routes-large.kite
##  kr brute <target> -w ~/api/wordlists/data/automated/nameofwordlist.txt when there is txt file

If you have many targets, you can save a list of line-separated targets as a text file and use that file as the target. You can use any of the following line-separated URI formats as input:

Test.com

Test2.com:443

http://test3.com

http://test4.com

http://test5.com:8888/api

One of the coolest Kiterunner features is the ability to replay requests. Thus, not only will you have an interesting result to investigate, you will also be able to dissect exactly why that request is interesting. In order to replay a request, copy the entire line of content into Kiterunner, paste it using the kb replay option, and include the wordlist you used:

# $ kr kb replay "GET     414 [    183,    7,   8]

://192.168.50.35:8888/api/privatisations/count 0cf6841b1e7ac8badc6e237ab300a90ca873d571" -w

~/api/wordlists/data/kiterunner/routes-large.kite

Running this will replay the request and provide you with the HTTP response. You can then review the contents to see if there is anything worthy of investigation. I normally review interesting results and then pivot to testing them using Postman and Burp Suite.

# DevTools

You can use the filter tool to search for any term you would like, such as "API", "v1", or "graphql". This is a quick way to find API endpoints in use. You can also leave the Devtools Network tab open while you perform actions on the web page
