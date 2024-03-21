import csv
import tkinter as tk
import sv_ttk
import os
import re
import requests
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO

# Main window
main = tk.Tk()
main.title("Steam Achievement Manager+ 0.1")
main.geometry("800x550")

# Change app icon
icon_image = tk.PhotoImage(file="Resources/SAM+ Logo.png")
main.iconphoto(True, icon_image)

# Change theme
sv_ttk.set_theme("dark")

# Create frame for darkmode switch
darkmode_frame = ttk.Frame(main)
darkmode_frame.pack(side="bottom")

# Darkmode Switch
darkmode_switch = ttk.Checkbutton(darkmode_frame, text="Lightmode", style="Switch.TCheckbutton", command=sv_ttk.toggle_theme)
darkmode_switch.pack(side="bottom")

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
    
steam_id = get_steam_id()
API_key= "9326C492E1DF557C1EC8E9DC717E3C3D"

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

        for game in owned_games:
            appid = game.get("appid", "")
            name = game.get("name", "")
            #img_icon_url = f"http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{game.get('img_icon_url', '')}.jpg"
            img_icon_url = f"https://cdn.cloudflare.steamstatic.com/steam/apps/{appid}/header.jpg"

            writer.writerow({"appid": appid, "name": name, "img_icon_url": img_icon_url})

    print("Owned games data exported to 'owned_games.csv' successfully.")
else:
    print("Failed to fetch data.")

# Display games in frame
def load_games_from_csv(csv_file):
    games = []
    with open(csv_file, "r", newline="", encoding="utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            games.append(row)
    return games

def resize_image(image, size):
    return image.resize(size)

def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            print(f"Failed to download image from {url}: {response.status_code}")
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")

def on_mousewheel(event, canvas):
    canvas.yview_scroll(int(-1*(event.delta/120)), "units")

def display_games():
    # Load games from CSV
    games = load_games_from_csv("owned_games.csv")

    # Create scrollable frame
    canvas = tk.Canvas(main)
    scrollbar = ttk.Scrollbar(main, orient="vertical", command=canvas.yview)
    scrollable_frame = ttk.Frame(canvas)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Enable mouse scroll
    canvas.bind("<MouseWheel>", lambda event: on_mousewheel(event, canvas))

    # Create game widgets
    cols = 3
    for i, game in enumerate(games):
        row = i // cols
        col = i % cols

        name = game["name"]
        img_url = game["img_icon_url"]  # No need to append base URL

        # Download and resize game icon
        img = download_image(img_url)
        if img:
            img = resize_image(img, (230, 107))
            img = ImageTk.PhotoImage(img)

            # Create label with game icon
            icon_label = tk.Label(scrollable_frame, image=img)
            icon_label.image = img
            icon_label.grid(row=row*2, column=col, padx=10, pady=8)

            # Create label with game name
            name_label = tk.Label(scrollable_frame, text=name)
            name_label.grid(row=row*2 + 1, column=col, padx=10, pady=5)
        else:
            print(f"Skipping game '{name}' (ID: {game['appid']}) due to missing or invalid image.")

    main.mainloop()

# Display games
display_games()