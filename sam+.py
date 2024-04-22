import csv
import tkinter as tk
import sv_ttk
import requests
import subprocess
import appearance
import api
import news
from tkinter import ttk
from PIL import Image, ImageTk
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor

# Define ThreadPoolExecutor with 10 threads
achievements_executor = ThreadPoolExecutor(max_workers=10)

# Main window
main = tk.Tk()
main.title("Steam Achievement Manager+ 0.5.10")
main.geometry("725x550")

# Create a Notebook (tabbed layout)
notebook = ttk.Notebook(main)
notebook.pack(fill="both", expand=True)

# Create frames for each tab
achievements_tab = ttk.Frame(notebook)
news_tab = ttk.Frame(notebook)
observed_games_tab = ttk.Frame(notebook)
appearance_tab = ttk.Frame(notebook)

# Add tabs to the notebook
notebook.add(achievements_tab, text='Achievements')
notebook.add(news_tab, text='News')
notebook.add(observed_games_tab, text='Observed Games')
notebook.add(appearance_tab, text='Appearance')

# Change app icon
icon_image = tk.PhotoImage(file="Resources/SAM+ Logo.png")
main.iconphoto(True, icon_image)

# Create "main"frame for buttons
container_frame = ttk.Frame(achievements_tab)
container_frame.pack(side="top", fill="both")

# Change theme
sv_ttk.set_theme("dark")

# Pass to appearance
appearance.lightmode_switch(appearance_tab)

# Pass to news
news.newsinfolabel(news_tab)

# Define a custom style for the green color
main_style = ttk.Style()
main_style.configure("Green.TButton", foreground="green")

############################################################

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
