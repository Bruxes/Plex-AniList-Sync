# Tautulli-AniList-Sync

A modern and robust Python script to automatically update your AniList watch progress when you watch an anime episode in Plex, triggered by Tautulli.

This script is designed to be a simple, single-file solution that correctly handles seasonal anime (e.g., "Jujutsu Kaisen Season 2") without manual intervention.

## Project Files

-   **`anilist_sync.py`**: The main script that Tautulli will run.
-   **`config.ini`**: The configuration file where you will safely store your AniList API token.
-   **`obtener_token.py`**: A one-time-use helper script to generate your personal AniList API token.

## How It Works

1.  You finish watching an anime episode in Plex.
2.  Tautulli detects the "watched" event and triggers its script agent.
3.  Tautulli runs `anilist_sync.py`, passing the show's title, season, and episode number as arguments.
4.  The script reads your API token from `config.ini`, then searches AniList for the correct anime and season.
5.  If the watched episode is newer than the progress on AniList, it updates your list.

## Setup Instructions

Follow these steps carefully to get everything running.

### 1. Prerequisites

-   A working Plex Media Server and Tautulli instance.
-   Python 3 installed on the machine where Tautulli runs.
-   The `requests` library for Python. If you don't have it, install it:

    pip install requests

### 2. AniList API Setup & Token Generation

This is a **one-time process** to authorize the script to access your AniList account.

**Step 2.1: Create an AniList API Client**
1.  Go to the AniList Apps settings page: **[https://anilist.co/settings/apps](https://anilist.co/settings/apps)**
2.  Click **Create New Client**.
3.  Fill in the details:
    -   **Name**: `Tautulli Sync` (or anything you like)
    -   **Redirect URL**: `https://anilist.co/api/v2/oauth/pin`
4.  Click **Save**. You will now see your new client in a list. Click on it to see its details.
5.  Keep this page open. You will need the **Client ID** and **Client Secret** for the next step.

**Step 2.2: Generate the Final Access Token**
1.  Download the `obtener_token.py` script from this repository.
2.  Open `obtener_token.py` in a text editor.
3.  Paste your **Client ID** and **Client Secret** into the corresponding variables at the top of the file.
4.  Now, on the AniList page from the previous step, get your authorization code (PIN) by visiting the authorization URL: `https://anilist.co/api/v2/oauth/authorize?client_id=YOUR_CLIENT_ID&response_type=code` (replace `YOUR_CLIENT_ID` with your actual Client ID).
5.  Authorize the app. You will be redirected to a page displaying a long authorization code (PIN). **Copy this entire code.**
6.  Paste the PIN you just copied into the `AUTHORIZATION_CODE` variable in `obtener_token.py`.
7.  Save the `obtener_token.py` file and run it from your terminal:

    ```bash
    python obtener_token.py

8.  If successful, the script will print a very long **Access Token**. **Copy this token!** This is the final key you need.

### 3. Script Configuration

1.  Open the `config.ini` file.
2.  You will see this content:

    [AniList]
    ApiToken = YOUR_ANILIST_TOKEN_GOES_HERE

3.  Replace `YOUR_ANILIST_TOKEN_GOES_HERE` with the final **Access Token** you just generated.
4.  Save the `config.ini` file. **Keep this file private and never share it.**

### 4. Tautulli Configuration

1.  In Tautulli, go to **Settings > Notification Agents > Add a new notification agent**.
2.  Select **Script**.
3.  **Configuration Tab:**
    -   **Script Folder**: Select the folder where you saved `anilist_sync.py`.
    -   **Script File**: Choose `anilist_sync.py` from the dropdown.
4.  **Triggers Tab:**
    -   Check the box for **Watched**.
5.  **Arguments Tab:**
    -   Go to the **Watched** section.
    -   In the text box, enter the following arguments:

    ```bash
    --title "{show_name}" --episode "{episode_num}" --season "{season_num}"

6.  Save the notification agent.

## That's it!

Your setup is complete. The next time you finish watching an anime episode, your AniList profile will be updated automatically.

---
## License
This project is licensed under the MIT License.
