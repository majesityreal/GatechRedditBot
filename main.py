import requests

# note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
auth = requests.auth.HTTPBasicAuth('fuHSQXgJfhJZDtn-0I8DBw', 'e84VuhD2YyCCLiFySE-7siDkhV52UA')

# here we pass our login method (password), username, and password
data = {'grant_type': 'password',
        'username': 'HelluvaWreckFromTech',
        'password': '!Yourmom123'}
        # ramblinwreckedEE
        # P0k3m0n!g0

# setup our header info, which gives reddit a brief description of our app
headers = {'User-Agent': 'MyBot/0.0.1'}

# send our request for an OAuth token
res = requests.post('https://www.reddit.com/api/v1/access_token',
                    auth=auth, data=data, headers=headers)

# Print the status code and response body for debugging
print("Status Code:", res.status_code)
print("Response Body:", res.json())

# convert response to JSON and pull access_token value
TOKEN = res.json()['access_token']

# add authorization to our headers dictionary
headers = {**headers, **{'Authorization': f"bearer {TOKEN}"}}

# while the token is valid (~2 hours) we just add headers=headers to our requests
requests.get('https://oauth.reddit.com/api/v1/me', headers=headers)

# res = requests.get("https://oauth.reddit.com/r/python/hot",
#                    headers=headers)

# print(res.json())  # let's see what we get