# RECON command used

- subfinder -d target.com -silent > subs.txt
- httpx -l subs.txt -mc 403,401,200 -tech-direct -title > live.txt
- gau --subs target.com | grep -iE 'admin|internal|dashboard' > gau_admin.text
- After finding 403 
- curl -X POST https://admin/dashboard -H "X-Original-Method: GET"
- OR
- curl -X HEAD https://admin/settings -H "X-Original-Method: GET"
- curl -H "X-Forwarded-For: 127.0.0.1" https://admin/profile



