# filename: test_config.py

import requests
import configparser
import os
import sys

# --- Configuration Loading ---
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.ini')

print("--- Running Configuration Test ---")

# 1. Check if config.ini exists
if not os.path.exists(config_path):
    print(f"❌ FAILURE: config.ini not found. Please make sure the file exists.")
    sys.exit(1)
print("✅ Found config.ini file.")
config.read(config_path)

# 2. Check for the ApiToken
try:
    ANILIST_API_TOKEN = config['AniList']['ApiToken']
    if 'YOUR_ANILIST_TOKEN' in ANILIST_API_TOKEN or len(ANILIST_API_TOKEN) < 100:
        print("❌ FAILURE: 'ApiToken' in config.ini looks like a placeholder or is too short.")
        print("   Please run 'get_token.py' to generate a valid token first.")
        sys.exit(1)
except KeyError:
    print("❌ FAILURE: Could not find 'ApiToken' in config.ini.")
    sys.exit(1)
print("✅ Found 'ApiToken' in config.ini.")

# 3. Test connection to AniList API
print("▶️  Attempting to connect to AniList API...")

ANILIST_API_URL = 'https://graphql.anilist.co'
HEADERS = {
    'Authorization': 'Bearer ' + ANILIST_API_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

# A simple query to get the authenticated user's name
query = '''
query {
  Viewer {
    id
    name
  }
}
'''

try:
    response = requests.post(ANILIST_API_URL, json={'query': query}, headers=HEADERS)
    response.raise_for_status() # Raises an error for bad status codes (4xx or 5xx)
    data = response.json()

    if 'errors' in data:
        error_message = data['errors'][0].get('message', 'Unknown error.')
        print(f"❌ FAILURE: AniList returned an error. This likely means your ApiToken is invalid or expired.")
        print(f"   API Message: {error_message}")
        sys.exit(1)
    
    viewer_name = data['data']['Viewer']['name']
    print(f"✅ Successfully connected to AniList API.")
    
    print("\n-----------------------------------------")
    print(f"🎉 SUCCESS! Your configuration is correct!")
    print(f"   Connected to AniList as: {viewer_name}")
    print("-----------------------------------------")

except requests.exceptions.HTTPError as e:
    if e.response.status_code == 401:
        print(f"❌ FAILURE: Connection failed with a 401 Unauthorized error.")
        print("   This means your ApiToken is incorrect, expired, or revoked.")
    else:
        print(f"❌ FAILURE: An HTTP error occurred: {e}")
except requests.exceptions.RequestException as e:
    print(f"❌ FAILURE: A network error occurred. Could not connect to AniList.")
    print(f"   Error: {e}")