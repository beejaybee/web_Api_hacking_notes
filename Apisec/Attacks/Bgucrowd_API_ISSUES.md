# Common things to test for in APIS

# 1. Authorization and Authintication

# Enumerating potential restricted endpoints
# Modifying Session Tokens
# Reusing Older session Tokens
# Attempt to bypass restriction on resource with IDOR
# Modifying the resource with additional parameters like $admin=True, 
# Modifying Referer headers that the application may expect

# 2. Input Validation

Input Validation is a very important thing to consider when hunting for bugs

It is crucial that input is anything that the server takes in, from the user, 3rd party apps and other internal mechanisms

Common places to test for input validation in an API:
# Within the request header
# Parameters within the URL
# Parameters within the request
# file uploads (PUT/DELETE request)
# Different Request

Depending on the Architecture of the application, specific parts of the requests may be processed in an unsafe way

These Include:
# Improper parameterization of requests within the application logic
# Lack of input sanitization / escaping unsafe characters
# Improper handling of parameters
# Insufficient controls for data types passed

Things You can fuzz for
# Remote Code execution
# Cross site scripting
# Local/Remote file Inclution
# SQL/NoSQL Injection
# Request SPlitting
# Deserialization
# XXE
# File Upload vulnerability
# SSRF

Tools You can Use 
# BURP
# Enumeration tools - wfuzz, Gobuster, DIRB
