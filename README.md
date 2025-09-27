# Tautulli-AniList-Sync

A simple, robust Python script to automatically update AniList progress from your Tautulli watch history.

This script is triggered by a Tautulli notification agent whenever you watch an episode on Plex. It then intelligently searches for the corresponding anime on AniList, including handling different seasons, and updates your episode progress.

## Features

- **Automatic Updates:** Syncs your watch progress without any manual intervention.
- **Smart Season Detection:** Correctly identifies and syncs multi-season anime (e.g., "Jujutsu Kaisen Season 2", "Attack on Titan The Final Season").
- **Robust Matching:** Tries multiple naming patterns, including Roman numerals, to find the correct AniList entry.
- **Safe Progress Updates:** Only updates progress if the watched episode is newer than the one tracked on AniList.
- **No External Dependencies:** Only requires Python and the `requests` library.

## Setup Guide

Follow these steps to get the script up and running.

### 1. Prerequisites

- You must have **Python 3** installed.
- You must have the **`requests`** library. If not, install it by running:

    pip install requests

### 2. Get AniList API Token

1.  Go to the AniList Apps settings page: **[https://anilist.co/settings/apps](https://anilist.co/settings/apps)**
2.  Click **Create New Client**.
3.  Enter a name (e.g., "Tautulli Sync") and set the **Redirect URL** to `https://anilist.co/api/v2/oauth/pin`.
4.  After creating the client, you will get a **Client ID** and **Client Secret**. Use these to generate a long-lived **Access Token** by following the PIN-based authorization flow.
    * *(Note: This is a one-time process to get the token you need for the script).*

### 3. Configure the Script

1.  Download the `anilist_sync.py` script from this repository.
2.  Open the file in a text editor.
3.  Find the following line at the top of the script:

    ANILIST_API_TOKEN = "PASTE_YOUR_ANILIST_TOKEN_HERE"

4.  Replace `"PASTE_YOUR_ANILIST_TOKEN_HERE"` with the Access Token you generated in the previous step. Save the file.

### 4. Configure Tautulli

1.  In Tautulli, go to **Settings > Notification Agents > Add a new notification agent**.
2.  Select **Script**.
3.  **Configuration Tab:**
    * **Script Folder:** Select the folder where you saved `anilist_sync.py`.
    * **Script File:** Choose `anilist_sync.py` from the dropdown.
4.  **Triggers Tab:**
    * Check the box for **Watched**.
5.  **Arguments Tab:**
    * Go to the **Watched** section.
    * In the text box, enter the following arguments:

    --title "{show_name}" --episode "{episode_num}" --season "{season_num}"

6.  Save the notification agent.

## That's it!

Your setup is complete. The next time you finish watching an anime episode on Plex, Tautulli will trigger the script, and your AniList profile will be updated automatically.

---
## License
This project is licensed under the MIT License.
