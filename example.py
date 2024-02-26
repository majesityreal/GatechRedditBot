import requests
import requests.auth
client_auth = requests.auth.HTTPBasicAuth('btLKK3hRHmvn7Ou1nI_Gpw', '9WHJ2P1KMEe3DEskP-8ZNK4acq1kbg')
post_data = {"grant_type": "password", "username": "ramblinwreckedEE", "password": "P0k3m0n!g0"}
headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=post_data, headers=headers)
print(response.json())