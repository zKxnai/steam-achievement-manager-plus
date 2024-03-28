import csv
import tkinter as tk
import sv_ttk
import os
import re
import requests
import subprocess
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

# Define ThreadPoolExecutor with 10 threads
executor = ThreadPoolExecutor(max_workers=10)

# Main window
main = tk.Tk()
main.title("Steam Achievement Manager+ 0.3.1")
main.geometry("725x550")

# Change app icon
icon_image = tk.PhotoImage(file="Resources/SAM+ Logo.png")
main.iconphoto(True, icon_image)

# Change theme
sv_ttk.set_theme("dark")

# Create a custom style for the highlighted frame
main_style = ttk.Style()
main_style.configure("Highlighted.TFrame", background="lightblue")

class HighlightFrame(ttk.Frame):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.default_bg = self["style"]['background']  # Assuming the default background color is set through the style

    def highlight(self):
        self.configure(style="Highlighted.TFrame")

    def reset_highlight(self):
        self.configure(style="TFrame")

# Create "main"frame for buttons
container_frame = ttk.Frame(main)
container_frame.pack(side="top", fill="both")

# Create frame for darkmode switch
darkmode_frame = ttk.Frame(container_frame)
darkmode_frame.pack(side="left")

darkmode_switch = ttk.Checkbutton(darkmode_frame, text="Lightmode", style="Switch.TCheckbutton", command=sv_ttk.toggle_theme)
darkmode_switch.pack(side="left", padx=10, pady=10)

#Placeholder function
def clear_placeholder(event=None):
    if search_var.get() == placeholder:
        searchbar.delete(0, tk.END)

def restore_placeholder(event=None):
    if search_var.get() == "":
        searchbar.insert(0, placeholder)

# Create frame for search bar
searchbar_frame = ttk.Frame(container_frame)
searchbar_frame.pack(side="left")
search_var = tk.StringVar()
placeholder = "Enter AppID or Name..."

searchbar = ttk.Entry(searchbar_frame, textvariable=search_var, width=40)
searchbar.insert(0, placeholder)
searchbar.bind("<FocusIn>", clear_placeholder)
searchbar.bind("<FocusOut>", restore_placeholder)
searchbar.pack(side=tk.LEFT)

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

def on_image_loaded(result, name, appid, row, col, frame, img_list):
    img = result
    if img:
        img = resize_image(img, (50, 50))
        img_tk = ImageTk.PhotoImage(img)
        img_list.append(img_tk)
        icon_label = tk.Label(frame, image=img_tk)
        icon_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")
        name_label = tk.Label(frame, text=name)
        name_label.grid(row=row, column=1, padx=10, pady=5, sticky="w")
        
        # Add buttons
        play_button_img = tk.PhotoImage(file="Resources/play_g.png")
        play_button = ttk.Button(frame, text="Play", image=play_button_img, compound="left", command=lambda appid=appid: open_hidden(appid))
        play_button.image = play_button_img
        play_button.grid(row=row, column=2, padx=10, pady=5, sticky="e")
        
        pause_button_img = tk.PhotoImage(file="Resources/pause_g.png")
        pause_button = ttk.Button(frame, text="Pause", image=pause_button_img, compound="left", command=lambda name=name: close_hidden(name))
        pause_button.image = pause_button_img
        pause_button.grid(row=row, column=3, padx=10, pady=5, sticky="e")
        
        achievement_button_img = tk.PhotoImage(file="Resources/trophy_g.png")
        achievement_button = ttk.Button(frame, text="Achievements", image=achievement_button_img, compound="left", command=lambda appid=appid: open_visible(appid))
        achievement_button.image = achievement_button_img
        achievement_button.grid(row=row, column=4, padx=10, pady=5, sticky="e")
    else:
        print(f"Skipping game '{name}' due to missing or invalid image.")

# Create widget for info
info_frame = tk.Frame(container_frame)
info_frame.pack(side="right")
info_label = ttk.Label(info_frame, text="Loading game icons...")
info_label.pack(side="right", padx=10)

def update_info_label(total_games):
    info_label.config(text=f"Total games: {total_games}")


def display_games():
    # Load games from CSV
    games = load_games_from_csv("owned_games.csv")
    sorted_games = sorted(games, key=lambda x: x["name"].lower())

    # Function to highlight the matching entry
    def highlight_entry(index):
        # Remove previous highlights
        for widget in scrollable_frame.winfo_children():
            if isinstance(widget, HighlightFrame):
                widget.reset_highlight()

        # Highlight the matching entry
        widget = scrollable_frame.winfo_children()[index]
        if isinstance(widget, HighlightFrame):
            widget.highlight()

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
        appid = game["appid"]
        img_url = game["img_icon_url"]

        # Download images asynchronously
        img_future = executor.submit(download_image, img_url)
        img_future.add_done_callback(
            lambda f, name=name, appid=appid, row=i, frame=scrollable_frame, img_list=img_list, total=len(sorted_games):
            on_image_loaded(f.result(), name, appid, row, 0, frame, img_list) or (update_info_label(total) if len(img_list) == total else None)
        )

    # Define a function to scroll to the entry matching the search term
    def scroll_to_entry(event=None):
        search_term = search_var.get().lower()

        # Find the index of the first entry that matches the search term
        for i, game in enumerate(sorted_games):
            if search_term in game["name"].lower() or search_term == str(game["appid"]):
                canvas.yview_moveto(i / len(sorted_games))
                highlight_entry(i)
                break

    # Bind the function to the search bar
    searchbar.bind("<Return>", scroll_to_entry)

    main.mainloop()

# Function to open the executable in a hidden window
def open_hidden(appid):
    subprocess.Popen(f"start /MIN cmd /c start /MIN /B Resources\\SAM.Game.exe {appid}", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

# Function to open the executable in a visible window
def open_visible(appid):
    subprocess.Popen(f"start /MIN cmd /c Resources\\SAM.Game.exe {appid}", shell=True)

# Function to close the hidden window opened by open_hidden
def close_hidden(name):
    subprocess.Popen(f"start /MIN cmd /c taskkill /F /FI \"WindowTitle eq Steam Achievement Manager 7.0 | {name}\"", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

# Display games
display_games()
