import requests
import requests.auth
client_auth = requests.auth.HTTPBasicAuth('btLKK3hRHmvn7Ou1nI_Gpw', '9WHJ2P1KMEe3DEskP-8ZNK4acq1kbg')
data = {'grant_type': 'password', 'username': 'HelluvaWreckFromTech', 'password': '!Yourmom123'}
headers = {"User-Agent": "ChangeMeClient/0.1 by YourUsername"}
response = requests.post("https://www.reddit.com/api/v1/access_token", auth=client_auth, data=data, headers=headers)
print(response.json())