import base64
import requests
from urllib.parse import urlencode

# Your Spotify app's client ID and client secret
client_id = '**'
client_secret = '**'

# The redirect URI you set in your Spotify app settings
redirect_uri = 'http://localhost/callback/'

# The base64 encoded string of your client ID and client secret
client_creds = f"{client_id}:{client_secret}"
client_creds_b64 = base64.b64encode(client_creds.encode())

# The URL the user will be redirected to for login
auth_url = 'https://accounts.spotify.com/authorize'
auth_data = {
    'client_id': client_id,
    'response_type': 'code',
    'redirect_uri': redirect_uri,
    'scope': 'user-read-private'  # Change this to the scopes you need
}
auth_params = urlencode(auth_data)

print(f"Please go to the following URL to authorize the app: {auth_url}?{auth_params}")

# After the user logs in, they will be redirected to the redirect URI with a code in the query string
auth_code = input("Enter the code from the query string: ")

# Use the code to get an access token and refresh token
token_url = 'https://accounts.spotify.com/api/token'
token_data = {
    'grant_type': 'authorization_code',
    'code': auth_code,
    'redirect_uri': redirect_uri
}
token_headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Authorization': f"Basic {client_creds_b64.decode()}"
}

response = requests.post(token_url, data=token_data, headers=token_headers)
response_data = response.json()

print(f"Access token: {response_data['access_token']}")
print(f"Refresh token: {response_data['refresh_token']}")