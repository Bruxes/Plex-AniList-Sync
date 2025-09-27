# filename: get_token.py

import requests
import configparser
import os
import sys

# --- CONFIGURATION ---
# This script now reads and writes to config.ini
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')

if not os.path.exists(config_path):
    print(f"🚨 Error: config.ini not found. Please make sure the file exists in the same directory.")
    sys.exit(1)

config.read(config_path)

try:
    CLIENT_ID = config['AniList']['ClientId']
    CLIENT_SECRET = config['AniList']['ClientSecret']
except KeyError:
    print("🚨 Error: Could not read 'ClientId' or 'ClientSecret' from config.ini.")
    sys.exit(1)

if 'YOUR_CLIENT' in CLIENT_ID or 'YOUR_CLIENT' in CLIENT_SECRET:
    print("🚨 Error: Please fill in your ClientId and ClientSecret in the config.ini file first.")
    sys.exit(1)
# ---------------------

# Step 1: Guide user to get the authorization code
auth_url = f"https://anilist.co/api/v2/oauth/authorize?client_id={CLIENT_ID}&response_type=code"
print("--- AniList Token Generation ---")
print("\nStep 1: Please open the following URL in your browser to authorize the application:")
print(f"\n{auth_url}\n")
print("After authorizing, you will be redirected to a page with a long code (PIN).")

# Step 2: Ask user to paste the code
AUTHORIZATION_CODE = input("Step 2: Please paste the entire authorization code here and press Enter:\n> ")

if not AUTHORIZATION_CODE.strip():
    print("🚨 Error: Authorization code cannot be empty.")
    sys.exit(1)

# Step 3: Exchange the code for the final token
url = 'https://anilist.co/api/v2/oauth/token'
payload = {
    'grant_type': 'authorization_code',
    'client_id': CLIENT_ID,
    'client_secret': CLIENT_SECRET,
    'redirect_uri': 'https://anilist.co/api/v2/oauth/pin',
    'code': AUTHORIZATION_CODE.strip(),
}

print("\nStep 3: Requesting the final access token from AniList...")
response = requests.post(url, json=payload)

if response.status_code == 200:
    access_token = response.json().get('access_token')
    
    # Step 4: Write the token back to config.ini
    config.set('AniList', 'ApiToken', access_token)
    with open(config_path, 'w') as configfile:
        config.write(configfile)
        
    print("\n🎉 SUCCESS! 🎉")
    print("Your final access token has been automatically saved to config.ini.")
    print("You can now close this window. Your setup is complete.")
else:
    print("\n🚨 ERROR! 🚨")
    print(f"Status Code: {response.status_code}")
    print(f"Response from AniList: {response.text}")
    print("\nPlease try the process again, making sure to generate a new authorization code.")