# Definition

Passive recon is looking for APIs without working with the target application directly

The goal is to find and save public information about the target API

This uses OSINT - getting informations from the public 

# Tools for passive Recon

- Google Dorking
    - If the website have a public API, search for **target_name api**
    - **intitle:"api" site:"target_name.com"**
    - **inurl:"/api/v1"site:"target_name.com"**
    - **intitle:"json" site:target_name.com**
    
- Git Dorking
    - **target_name api**
    - **target_name api key** then check issues
    - If you know how your target use to call API key, search for it on github
    - You can also search for common headers: like, **Authorization: Bearer** You can also specify your target name
    - **"filename: swagger.json"** 
    - **path:\*\*'/swagger.json**

- Shodan shadan.io
    - Generic search _ target name

- API Directory
- Wayback machine
- shodan

sudo docker run -it -v "$PWD:/pwd" trufflesecurity/trufflehog:latest github --org=target-name
