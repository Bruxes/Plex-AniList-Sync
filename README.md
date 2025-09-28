# Plex-AniList-Sync

<img width="256" height="256" alt="Gemini_Generated_Image_74zd7474zd7474zd" src="https://github.com/user-attachments/assets/34ee7ac4-2e1b-46d2-b6e4-e9642993aafe" />


A modern and robust Python script to automatically update your AniList watch progress when you watch an anime episode in Plex, triggered by Tautulli.

This project is designed to be a simple, user-friendly solution. **You only need to edit the `config.ini` file to get started.**

## Project Files

-   **`anilist_sync.py`**: The main script that Tautulli will run.
-   **`config.ini`**: The central configuration file. **This is the only file you need to edit.**
-   **`get_token.py`**: A helper script that you run once to automatically generate your API token.
-   **`test_config.py`**: A test script to help you know if you did everything good or not.

## How It Works

1.  You finish watching an anime episode in Plex.
2.  Tautulli detects the "watched" event and triggers its script agent.
3.  Tautulli runs `anilist_sync.py`, passing the show's title, season, and episode number.
4.  The script reads your API token from `config.ini`, searches AniList for the correct anime, and updates your watch progress.

## Setup Instructions

Follow these steps carefully. The entire configuration is handled in the `config.ini` file.

### 1. Prerequisites

-   A working Plex Media Server and Tautulli instance.
-   Python 3 installed on the machine where Tautulli runs.
-   The `requests` library for Python. If you don't have it, install it:

    ```bash
    pip install requests

### 2. Generate Your AniList API Token (One-Time Setup)

This process uses the `get_token.py` script to automatically generate and save your token.

**Step 2.1: Get Your Client ID and Secret**
1.  Go to the AniList Apps settings page: **[https://anilist.co/settings/apps](https://anilist.co/settings/apps)**
2.  Click **Create New Client**.
3.  Fill in the details:
    -   **Name**: `Tautulli Sync` (or anything you like)
    -   **Redirect URL**: `https://anilist.co/api/v2/oauth/pin`
4.  Click **Save**. You will now see your new client. Click on it to see its **Client ID** and **Client Secret**.
5.  Open the `config.ini` file from this repository.
6.  Copy your **Client ID** and **Client Secret** and paste them into the corresponding fields in `config.ini`. Save the file.

**Step 2.2: Run the Token Generation Script**
1.  Now, run the `get_token.py` script from your terminal:

    ```bash
    python get_token.py

2.  The script will guide you. It will ask you to open a URL in your browser to authorize the app.
3.  After authorizing, AniList will give you a long code (PIN).
4.  **Copy the PIN** and **paste it back into the terminal** when the script asks for it.
5.  If successful, the script will automatically write the final `ApiToken` into your `config.ini` file.

### 3. Verify Your Setup (Recommended)

After completing the configuration, you can run the included test script to verify that everything is working correctly. This will check your `config.ini` file and attempt to connect to the AniList API with your token.

From your terminal, run the following command:

    python test_config.py

**If the test is successful**, you will see a success message with your AniList username:

    --- Running Configuration Test ---
    ✅ Found config.ini file.
    ✅ Found 'ApiToken' in config.ini.
    ▶️  Attempting to connect to AniList API...
    ✅ Successfully connected to AniList API.

    -----------------------------------------
    🎉 SUCCESS! Your configuration is correct!
       Connected to AniList as: YourUsername
    -----------------------------------------

If you see any errors, the script will provide hints on how to fix the issue (e.g., an invalid token or a missing configuration file).

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

Your setup is complete. The project is now fully configured and ready to go.

---
## License
This project is licensed under the MIT License.
