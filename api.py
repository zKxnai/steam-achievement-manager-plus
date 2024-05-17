import os
import re
import csv
import requests

# Display games in frame
def load_games_from_csv(csv_file):
    games = []
    with open(csv_file, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            games.append(row)
    return games

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

# Function to get API key from environment variable
def get_api_key():
    api_key = os.environ.get('STEAM_API_KEY')
    if not api_key:
        raise ValueError("API key not found. Set the STEAM_API_KEY environment variable.")
    return api_key

steam_id = get_steam_id()
API_key= get_api_key()

# Get owned games
url_owned_games = f"http://api.steampowered.com/IPlayerService/GetOwnedGames/v0001/?key={API_key}&steamid={steam_id}&format=json&include_appinfo&include_appinfo=true&include_played_free_games=true"
response = requests.get(url_owned_games)
if response.status_code == 200:
    data = response.json()

    owned_games = data.get("response", {}).get("games", [])

    with open("owned_games.csv", "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["appid", "name", "img_icon_url"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Sort games alphabetically by name
        sorted_owned_games = sorted(owned_games, key=lambda x: x["name"].lower())

        for game in sorted_owned_games:
            appid = game.get("appid", "")
            name = game.get("name", "")
            #img_icon_url = f"http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{game['img_icon_url']}.jpg"
            img_icon_url = f"http://steamcdn-a.akamaihd.net/steamcommunity/public/images/apps/{appid}/{game['img_icon_url']}.jpg"

            writer.writerow({"appid": appid, "name": name, "img_icon_url": img_icon_url})

    print("Owned games data exported to 'owned_games.csv' successfully.")

else:
    print("Failed to fetch data.")

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

"""
# Get achievements
url = f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appid}&key={API_key}&steamid={steam_id}"
"""