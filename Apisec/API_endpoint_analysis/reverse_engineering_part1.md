# Reverse Engineering an API using POSTMAN

1. open postman
2. create workspace
3. create collection
4. Go to collection and click and capture request
5. Enable proxy and give it port 5555
6. Set to save responses for requests
7. Configure incoming request
8. Then start proxy
9. And start working on the web app you need the api reqeust.
10. Dont forget to change your foxyproxy to postman
11. Then click on every possible link you can find
13. Stop the proxy and save all the useful links in their respective files


# Reverse Engineering an API using MITMPROXY & MITMPROXYSWAGGER

1. mitmproxy
2. once it's running create an port listening on 8080
3. Once the Proxy is set up, you can now start clicking on all the links in your target
4. Make sure you have the certificate set up before clicking on the links
5. Go to http://127.0.0.1:8081 to access your logs from your target
6. Filter out your target and click on save. save it to a test file
7. Then run **sudo mitmproxy2swagger -i /Downloads/flows -o spec.yml -p http://yourtargetbaseurl -f flow**
8. Edit the result to remove ignore from valuable links
9. vim spec.yml
10. run **sudo mitmproxy2swagger -i /Downloads/flows -o spec.yml -p http://yourtargetbaseurl -f flow --examples**
11. Go to  https://editor.swagger.io/ and import the spec.yml file into it
12. You would have the API format like that.
13. You can also import the spec.yml file into postman
14. The Api collection is then ready for use
15. You can also start directly brute forcing
