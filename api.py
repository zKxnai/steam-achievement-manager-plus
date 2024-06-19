import os
import re
import requests
import threading
from database import save_owned_games, load_api_key, save_achievements
from tkinter import messagebox
from concurrent.futures import ThreadPoolExecutor

# Get Steam user ID
def get_steam_id():
    steam_config_path = os.path.join(os.getenv("ProgramFiles(x86)"), "Steam", "config", "loginusers.vdf")
    if not os.path.isfile(steam_config_path):
        print("Steam user config not found.")
        return None
    try:
        with open(steam_config_path, 'r') as f:
            config_data = f.read()

        user_id_match = re.search(r'"users"\s+{\s+"(\d+)"\s+', config_data)
        if user_id_match:
            return user_id_match.group(1)
        else:
            print("User ID not found in Steam configuration file.")
            return None
    except Exception as e:
        print(f"Error reading Steam configuration file: {e}")
        return None

def get_api_key():
    api_key = load_api_key()
    if not api_key:
        # Show the warning message in a separate thread
        threading.Thread(target=show_warning_message).start()
    return api_key

def show_warning_message():
    messagebox.showwarning("Warning", "No API key found in the database. Please enter an API key.")

steam_id = get_steam_id()
API_key= get_api_key()

# Get owned games
def get_owned_games(API_key, steam_id):
    url_owned_games = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_key}&steamid={steam_id}&format=json&include_appinfo&include_appinfo=true&include_played_free_games=true"
    response = requests.get(url_owned_games)
    if response.status_code == 200:
        data = response.json()

        owned_games = data.get("response", {}).get("games", [])

        # Save owned games to the database
        games_to_save = []
        for game in owned_games:
            appid = game.get("appid", "")
            name = game.get("name", "")
            img_icon_url = f"http://steamcdn-a.akamaihd.net/steamcommunity/public/images/apps/{appid}/{game['img_icon_url']}.jpg"

            games_to_save.append({"appid": appid, "name": name, "img_icon_url": img_icon_url})

        save_owned_games(games_to_save)

        print("Owned games data saved to the database successfully.")

        # Fetch achievements for each game using ThreadPoolExecutor
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(fetch_and_save_achievements, API_key, steam_id, game['appid']) for game in owned_games]
            for future in futures:
                future.result()  # Wait for all futures to complete

    else:
        print("Failed to fetch data from Steam API.")

# Fetch latest news entry from game
def get_latest_news(appid):
    url = f"https://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={appid}&count=1&maxlength=500&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        news = response.json().get("appnews", {}).get("newsitems", [])
        if news:
            latest_news = news[0]
            return latest_news
    return None

# Fetch and save achievements
def fetch_and_save_achievements(API_key, steam_id, appid):
    url_achievements = f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appid}&key={API_key}&steamid={steam_id}"
    response = requests.get(url_achievements)
    if response.status_code == 200:
        data = response.json()

        achievements = data.get("playerstats", {}).get("achievements", [])

        # Save achievements to the database
        achievements_to_save = []
        for achievement in achievements:
            apiname = achievement.get("apiname", "")
            achieved = achievement.get("achieved", 0)

            achievements_to_save.append({"appid": appid, "apiname": apiname, "achieved": achieved})

        save_achievements(achievements_to_save)

        print(f"Achievements for appid {appid} saved to the database successfully.")
    else:
        print(f"Failed to fetch achievements for appid {appid}.")