import os
import re
import csv
import requests
import concurrent.futures
from concurrent.futures import ThreadPoolExecutor

# Define ThreadPoolExecutor with 5 threads
achievementcount_executor = ThreadPoolExecutor(max_workers=5)

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

"""
# Get achievements
def get_achievement_count(appid, API_key, steam_id):
    url = f"https://api.steampowered.com/ISteamUserStats/GetPlayerAchievements/v0001/?appid={appid}&key={API_key}&steamid={steam_id}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if 'playerstats' in data:
            achievements = data['playerstats'].get('achievements', [])
            if achievements:
                unlocked_count = sum(1 for achievement in achievements if achievement.get('achieved', 0) == 1)
                total_count = len(achievements)
                return unlocked_count, total_count
            else:
                print(f"No achievements found for appid {appid}")
                return 0, 0  # Return 0 for both unlocked and total count when no achievements found
        else:
            print(f"No player stats found for appid {appid}")
            return None, None
    else:
        print(f"Failed to fetch player achievements for appid {appid}")
        return None, None

def get_achievement_counts_from_csv(csv_filename, API_key, steam_id):
    with open(csv_filename, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        achievement_counts = []
        for row in reader:
            appid = row["appid"]
            name = row["name"]
            unlocked_count, total_count = get_achievement_count(appid, API_key, steam_id)
            if unlocked_count is not None and total_count is not None:
                achievement_counts.append({"appid": appid, "name": name, "unlocked_count": unlocked_count, "total_count": total_count})
            else:
                print(f"Failed to fetch achievement counts for {name} (appid: {appid})")
        return achievement_counts

def get_achievement_counts_from_csv_background(csv_filename, API_key, steam_id):
    with open(csv_filename, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        achievement_counts = []
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(get_achievement_count, row["appid"], API_key, steam_id): row for row in reader}
            for future in concurrent.futures.as_completed(futures):
                row = futures[future]
                appid = row["appid"]
                name = row["name"]
                try:
                    unlocked_count, total_count = future.result()
                    if unlocked_count is not None and total_count is not None:
                        achievement_counts.append({"appid": appid, "name": name, "unlocked_count": unlocked_count, "total_count": total_count})
                    else:
                        print(f"Failed to fetch achievement counts for {name} (appid: {appid})")
                except Exception as e:
                    print(f"Error fetching achievement counts for {name} (appid: {appid}): {e}")
        return achievement_counts

achievement_counts = get_achievement_counts_from_csv_background("owned_games.csv", API_key, steam_id)
"""