import csv
import tkinter as tk
import sv_ttk
import os
import re
import requests
import subprocess
import datetime
import appearance
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

# Define ThreadPoolExecutor with 10 threads
achievements_executor = ThreadPoolExecutor(max_workers=10)
news_executor = ThreadPoolExecutor(max_workers=5)

# Main window
main = tk.Tk()
main.title("Steam Achievement Manager+ 0.5.7")
main.geometry("725x550")

# Create a Notebook (tabbed layout)
notebook = ttk.Notebook(main)
notebook.pack(fill="both", expand=True)

# Create frames for each tab
achievements_tab = ttk.Frame(notebook)
#news_tab = ttk.Frame(notebook)
observed_games_tab = ttk.Frame(notebook)
appearance_tab = ttk.Frame(notebook)

# Add tabs to the notebook
notebook.add(achievements_tab, text='Achievements')
#notebook.add(news_tab, text='News')
notebook.add(observed_games_tab, text='Observed Games')
notebook.add(appearance_tab, text='Appearance')

# Change app icon
icon_image = tk.PhotoImage(file="Resources/SAM+ Logo.png")
main.iconphoto(True, icon_image)

# Change theme
sv_ttk.set_theme("dark")

# Pass to appearance
appearance.lightmode_switch(appearance_tab)

# Define a custom style for the green color
main_style = ttk.Style()
main_style.configure("Green.TButton", foreground="green")

# Create "main"frame for buttons
container_frame = ttk.Frame(achievements_tab)
container_frame.pack(side="top", fill="both")

#Create game count frame
played_games_frame = ttk.Frame(achievements_tab)
played_games_frame.pack(padx=10, pady=10)

#Create game count
played_games_count = 0
played_games_label = ttk.Label(played_games_frame, text=f"Played Games: {played_games_count}")
played_games_label.pack(side="bottom")

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
searchbar.pack(side=tk.LEFT, padx=10, pady=10)

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

def on_mousewheel(event, achievements_canvas):
    achievements_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

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

        # Update button states when clicked
        play_button.config(command=lambda appid=appid, button=play_button: play_button_clicked(appid, button))
        pause_button.config(command=lambda name=name, button=play_button: pause_button_clicked(name, button))
    else:
        print(f"Skipping game '{name}' due to missing or invalid image.")

def play_button_clicked(appid, button):
    # Change the button text to "Playing..." and color to green
    button.config(text="Playing...", style="Green.TButton")
    open_hidden(appid)

def pause_button_clicked(name, button):
    # Change the button text back to "Play" and revert to the default style
    button.config(text="Play", style="TButton")
    close_hidden(name)

# Create widget for info
info_frame = tk.Frame(container_frame)
info_frame.pack(side="right")
info_label = ttk.Label(info_frame, text="Loading game icons...")
info_label.pack(side="right", padx=10)

def update_info_label(total_games):
    info_label.config(text=f"Total games: {total_games}")

# Function to open the executable in a hidden window
def open_hidden(appid):
    global played_games_count
    played_games_count += 1
    played_games_label.config(text=f"Played Games: {played_games_count}")
    subprocess.Popen(f"start /MIN cmd /c start /MIN /B Resources\\SAM.Game.exe {appid}", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

# Function to open the executable in a visible window
def open_visible(appid):
    subprocess.Popen(f"start /MIN cmd /c Resources\\SAM.Game.exe {appid}", shell=True)

# Function to close the hidden window opened by open_hidden
def close_hidden(name):
    global played_games_count
    played_games_count -= 1
    played_games_label.config(text=f"Played Games: {played_games_count}")
    subprocess.Popen(f"start /MIN cmd /c taskkill /F /FI \"WindowTitle eq Steam Achievement Manager 7.0 | {name}\"", shell=True, creationflags=subprocess.CREATE_NO_WINDOW)

# Temporarily deprecated
"""
# Function to fetch news for each game
def fetch_game_news(appid):
    url = f"http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={appid}&count=1&maxlength=500&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        news = data.get("appnews", {}).get("newsitems", [])
        
        # Convert Unix timestamp to human-readable format for each news item
        for item in news:
            item_date = datetime.datetime.fromtimestamp(item.get("date", 0), tz=datetime.timezone.utc)
            item["date"] = item_date.strftime("%Y-%m-%d %H:%M:%S")  # Format the date
            
        return news
    else:
        print(f"Failed to fetch news for appid {appid}")

def fetch_news_async(appid):
    return news_executor.submit(fetch_game_news, appid)

# Create frame for lightmode switch and search bar in the news tab
news_search_frame = ttk.Frame(news_tab)
news_search_frame.pack(side="top", fill="x")

# Create search bar in the news tab
news_searchbar_frame = ttk.Frame(news_search_frame)
news_searchbar_frame.pack(side="left")
news_search_var = tk.StringVar()
news_placeholder = "Search News..."

#Placeholder function
def clear_news_placeholder(event=None):
    if news_search_var.get() == news_placeholder:
        news_searchbar.delete(0, tk.END)

def restore_news_placeholder(event=None):
    if news_search_var.get() == "":
        news_searchbar.insert(0, news_placeholder)

news_searchbar = ttk.Entry(news_searchbar_frame, textvariable=news_search_var, width=40)
news_searchbar.insert(0, news_placeholder)
news_searchbar.bind("<FocusIn>", clear_news_placeholder)
news_searchbar.bind("<FocusOut>", restore_news_placeholder)
news_searchbar.pack(side=tk.LEFT, padx=10, pady=10)

# Create a frame to hold all the news entries
all_news_frame = ttk.Frame(news_tab)
all_news_frame.pack(padx=10, pady=10, fill="both", expand=True)

# Create a canvas to add a scrollbar to the news frame
news_canvas = tk.Canvas(all_news_frame)
news_canvas.pack(side="left", fill="both", expand=True)

# Add a scrollbar to the canvas
news_scrollbar = ttk.Scrollbar(all_news_frame, orient="vertical", command=news_canvas.yview)
news_scrollbar.pack(side="right", fill="y")
news_canvas.configure(yscrollcommand=news_scrollbar.set)

# Create a frame to contain the news items
inner_frame = ttk.Frame(news_canvas)
news_canvas.create_window((0, 0), window=inner_frame, anchor="nw")

# Function to display news in the news tab
def display_news_async(news_tab, games):
    for game in games:
        appid = game["appid"]
        future_news = fetch_news_async(appid)
        future_news.add_done_callback(
            lambda f, game=game: display_news_callback(f.result(), news_tab, game)
        )

def display_news_callback(news, news_tab, game):
    appid = game["appid"]
    if news:
        game_frame = ttk.Frame(inner_frame)
        game_frame.pack(side="top", anchor="w", padx=10, pady=10, fill="x")

        # Display game name
        game_name_label = ttk.Label(game_frame, text=game["name"], font=("Arial", 12, "bold"))
        game_name_label.pack(anchor="w", padx=10, pady=(0, 5))

        # Create a subframe for news items
        news_frame = ttk.Frame(game_frame)
        news_frame.pack(anchor="w", padx=10)

        # Display news items in a list
        for item in news:
            news_title_label = ttk.Label(news_frame, text=item["title"], font=("Arial", 10, "bold"), wraplength=600, justify="left")
            news_title_label.pack(anchor="w", padx=10, pady=5)
            news_date_label = ttk.Label(news_frame, text=item["date"])
            news_date_label.pack(anchor="w", padx=10, pady=2)
            news_content_label = ttk.Label(news_frame, text=item["contents"], wraplength=600, justify="left")
            news_content_label.pack(anchor="w", padx=10, pady=5)
            empty_line_label = ttk.Label(news_frame, text="")
            empty_line_label.pack(anchor="w", padx=10, pady=5)
        
        # Update the scroll region of the canvas
        inner_frame.update_idletasks()
        news_canvas.config(scrollregion=news_canvas.bbox("all"))

    else:
        print(f"No news found for appid {appid}")

# Display news
games = load_games_from_csv("owned_games.csv")
display_news_async(news_tab, games)

def scroll_to_news_entry(event=None):
    search_term = news_search_var.get().lower()

    # Iterate over the news items to find a match for the search term
    for game_frame in inner_frame.winfo_children():
        game_name_label = game_frame.winfo_children()[0]  # First child is the game name label
        game_name = game_name_label.cget("text").lower()

        # Check if the search term matches the game name
        if search_term in game_name:
            # Get the position of the game frame relative to the canvas height
            relative_y = game_frame.winfo_y() / news_canvas.winfo_height()
            # Scroll to the position of the game frame
            news_canvas.yview_moveto(relative_y)
            break

# Bind the function to the search bar
news_searchbar.bind("<Return>", scroll_to_news_entry)
"""

def display_games():
    # Load games from CSV
    games = load_games_from_csv("owned_games.csv")
    sorted_games = sorted(games, key=lambda x: x["name"].lower())

    # Create scrollable frame
    achievements_canvas = tk.Canvas(achievements_tab)
    scrollable_frame = ttk.Frame(achievements_canvas)
    scrollbar = ttk.Scrollbar(achievements_canvas, orient="vertical", command=achievements_canvas.yview)

    scrollable_frame.bind(
        "<Configure>",
        lambda e: achievements_canvas.configure(
            scrollregion=achievements_canvas.bbox("all")
        )
    )

    achievements_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    achievements_canvas.configure(yscrollcommand=scrollbar.set)

    # Configure list layout
    achievements_canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Enable mouse scroll
    achievements_canvas.bind_all("<MouseWheel>", lambda event: on_mousewheel(event, achievements_canvas))

    # Create game widgets
    img_list = []  # List to store image objects
    for i, game in enumerate(sorted_games):
        name = game["name"]
        appid = game["appid"]
        img_url = game["img_icon_url"]

        # Download images asynchronously
        img_future = achievements_executor.submit(download_image, img_url)
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
                achievements_canvas.yview_moveto(i / len(sorted_games))
                break

    # Bind the function to the search bar
    searchbar.bind("<Return>", scroll_to_entry)

    main.mainloop()

# Display games
display_games()
