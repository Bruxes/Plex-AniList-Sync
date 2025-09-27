# FILE: anilist_sync.py

import requests
import argparse
import json
import configparser
import re

# --- CONFIGURATION ---
# Load configuration from an external file for better security and management.
config = configparser.ConfigParser()
config.read('config.ini')

try:
    ANILIST_API_TOKEN = config['AniList']['ApiToken']
except KeyError:
    print("🚨 ERROR: 'ApiToken' not found in config.ini. Please check your configuration file.")
    exit()
# ---------------------

ANILIST_API_URL = 'https://graphql.anilist.co'
HEADERS = {
    'Authorization': 'Bearer ' + ANILIST_API_TOKEN,
    'Content-Type': 'application/json',
    'Accept': 'application/json',
}

def to_roman(n):
    """Converts an integer to a simple Roman numeral (for season numbers)."""
    if not 1 <= n <= 10: return str(n)
    val = [10, 9, 5, 4, 1]
    syb = ["X", "IX", "V", "IV", "I"]
    roman_num = ""
    i = 0
    while n > 0:
        for _ in range(n // val[i]):
            roman_num += syb[i]
            n -= val[i]
        i += 1
    return roman_num

def get_anilist_id_and_progress(show_title, season_number):
    """
    Searches for an anime on AniList using a robust season-aware search logic.
    """
    base_title = re.sub(r'(?i)\s*season\s*\d+', '', show_title).strip()
    search_patterns = []

    if season_number > 1:
        roman_season = to_roman(season_number)
        search_patterns.extend([
            f"{base_title} Season {season_number}",
            f"{base_title} {season_number}",
            f"{base_title} {roman_season}" if roman_season != str(season_number) else None,
            f"{base_title} 2nd Season" if season_number == 2 else f"{base_title} {season_number}rd Season"
        ])
    
    search_patterns.append(show_title)
    search_patterns = [p for p in search_patterns if p] # Remove None entries
    search_patterns = list(dict.fromkeys(search_patterns)) # Remove duplicates
    
    print(f"🔎 Searching AniList with the following patterns: {search_patterns}")

    for pattern in search_patterns:
        print(f"▶️  Trying: '{pattern}'")
        query = '''
        query ($search: String) { 
            Media (search: $search, type: ANIME) { 
                id, 
                title { romaji, english }, 
                mediaListEntry { progress } 
            } 
        }
        '''
        variables = {'search': pattern}
        
        try:
            response = requests.post(ANILIST_API_URL, json={'query': query, 'variables': variables}, headers=HEADERS)
            response.raise_for_status()
            data = response.json()
            
            if data.get('data') and data['data'].get('Media'):
                media = data['data']['Media']
                found_title = (media['title'].get('english') or media['title'].get('romaji') or "").lower()
                
                if pattern != base_title and season_number > 1:
                    roman_season = to_roman(season_number).lower()
                    if not (str(season_number) in found_title or 
                            roman_season in found_title or 
                            (season_number == 2 and "2nd" in found_title) or
                            (season_number == 3 and "3rd" in found_title)):
                        print(f"⚠️  Result '{found_title}' found, but it doesn't seem to be Season {season_number}. Skipping.")
                        continue

                media_id = media['id']
                media_list_entry = media.get('mediaListEntry')
                progress = media_list_entry.get('progress') or 0 if media_list_entry else 0
                
                print(f"✅ Found! '{media['title']['romaji']}' (ID: {media_id}) with {progress} episodes watched.")
                return media_id, progress
            
        except requests.exceptions.RequestException as e:
            print(f"🚨 Error connecting to the AniList API: {e}")
            return None, None

    print(f"❌ Could not find '{show_title}' (S{season_number}) with any pattern.")
    return None, None

def update_anilist_progress(media_id, episode_number):
    """
    Updates the progress for a given media ID on the user's AniList list.
    """
    query = '''
    mutation ($mediaId: Int, $progress: Int) {
      SaveMediaListEntry (mediaId: $mediaId, progress: $progress, status: CURRENT) {
        id
        progress
        status
      }
    }
    '''
    variables = {'mediaId': media_id, 'progress': episode_number}
    
    try:
        response = requests.post(ANILIST_API_URL, json={'query': query, 'variables': variables}, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        if data.get('data') and data['data'].get('SaveMediaListEntry'):
            updated_progress = data['data']['SaveMediaListEntry']['progress']
            print(f"🎉 Success! Progress updated to episode {updated_progress} on AniList.")
        else:
            print(f"💔 Failed to update progress on AniList: {data.get('errors')}")

    except requests.exceptions.RequestException as e:
        print(f"🚨 Error connecting to the AniList API during update: {e}")

def main():
    """
    Main function to parse arguments from Tautulli and run the sync process.
    """
    parser = argparse.ArgumentParser(description="Syncs Plex watch progress from Tautulli to AniList.")
    parser.add_argument('--title', required=True, help="The title of the series.")
    parser.add_argument('--episode', required=True, type=int, help="The episode number watched.")
    parser.add_argument('--season', required=True, type=int, help="The season number watched.")

    args = parser.parse_args()
    
    print(f"🎬 Tautulli reported watch of S{args.season:02d}E{args.episode:02d} for '{args.title}'.")
    
    media_id, current_progress = get_anilist_id_and_progress(args.title, args.season)
    
    if media_id:
        if args.episode > current_progress:
            print(f"⬆️  New episode watched ({args.episode}) is greater than recorded progress ({current_progress}). Updating...")
            update_anilist_progress(media_id, args.episode)
        else:
            print(f"👍 Progress on AniList is already up-to-date or ahead. No action needed.")

if __name__ == "__main__":
    main()