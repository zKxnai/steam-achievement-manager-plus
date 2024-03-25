import csv
import tkinter as tk
import sv_ttk
import os
import re
import requests
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

# Define ThreadPoolExecutor with 10 threads
executor = ThreadPoolExecutor(max_workers=10)

# Main window
main = tk.Tk()
main.title("Steam Achievement Manager+ 0.2")
main.geometry("800x550")

# Change app icon
icon_image = tk.PhotoImage(file="Resources/SAM+ Logo.png")
main.iconphoto(True, icon_image)

# Change theme
sv_ttk.set_theme("dark")

# Create "main"frame for buttons
container_frame = ttk.Frame(main)
container_frame.pack(side="top", fill="both")

# Create frame for darkmode switch
darkmode_frame = ttk.Frame(container_frame, width=50, height=50, relief="raised")
darkmode_frame.pack(side="left")

darkmode_switch = ttk.Checkbutton(darkmode_frame, text="Lightmode", style="Switch.TCheckbutton", command=sv_ttk.toggle_theme)
darkmode_switch.pack(side="left", padx=10, pady=10)

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
            img_icon_url = f"http://media.steampowered.com/steamcommunity/public/images/apps/{appid}/{game['img_icon_url']}.jpg"

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

def on_image_loaded(result, name, row, col, frame, img_list):
    img = result
    if img:
        #img = resize_image(img, (212, 100))
        img = resize_image(img, (50, 50))
        img_tk = ImageTk.PhotoImage(img)
        img_list.append(img_tk)
        icon_label = tk.Label(frame, image=img_tk)
        icon_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        name_label = tk.Label(frame, text=name)
        name_label.grid(row=row, column=1, padx=10, pady=5, sticky="w")
        
        # Add buttons
        play_button_img = tk.PhotoImage(file="Resources/play.png")
        play_button = ttk.Button(frame, text="Play", image=play_button_img)
        play_button.grid(row=row, column=2, padx=10, pady=5, sticky="e")
        
        pause_button_img = tk.PhotoImage(file="Resources/pause.png")
        pause_button = ttk.Button(frame, text="Pause", image=pause_button_img)
        pause_button.grid(row=row, column=3, padx=10, pady=5, sticky="e")
        
        achievement_button_img = tk.PhotoImage(file="Resources/trophy.png")
        achievement_button = ttk.Button(frame, text="Achievements", image=achievement_button_img)
        achievement_button.grid(row=row, column=4, padx=10, pady=5, sticky="e")
    else:
        print(f"Skipping game '{name}' due to missing or invalid image.")

def display_games():
    # Load games from CSV
    games = load_games_from_csv("owned_games.csv")
    sorted_games = sorted(games, key=lambda x: x["name"].lower())

    # Create scrollable frame
    canvas = tk.Canvas(main)
    scrollable_frame = ttk.Frame(canvas)
    scrollbar = ttk.Scrollbar(canvas, orient="vertical", command=canvas.yview)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(
            scrollregion=canvas.bbox("all")
        )
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Configure grid layout
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Enable mouse scroll
    canvas.bind_all("<MouseWheel>", lambda event: on_mousewheel(event, canvas))

    # Create game widgets
    img_list = []  # List to store image objects
    for i, game in enumerate(sorted_games):
        name = game["name"]
        img_url = game["img_icon_url"]

        # Download images asynchronously
        img_future = executor.submit(download_image, img_url)
        img_future.add_done_callback(
            lambda f, name=name, row=i, frame=scrollable_frame, img_list=img_list:
            on_image_loaded(f.result(), name, row, 0, frame, img_list)
        )

    main.mainloop()

# Display games
display_games()
