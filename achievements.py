import tkinter as tk
import datetime
import csv
import requests
import subprocess
from tkinter import ttk
from io import BytesIO
from PIL import Image, ImageTk
from concurrent.futures import ThreadPoolExecutor
from api import load_games_from_csv

# Define ThreadPoolExecutor with 10 threads
achievements_executor = ThreadPoolExecutor(max_workers=10)

class ScrollableFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Bind mouse wheel events when the mouse enters and leaves the canvas
        self.canvas.bind("<Enter>", self._bind_mouse_wheel)
        self.canvas.bind("<Leave>", self._unbind_mouse_wheel)

    def _bind_mouse_wheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)  # For Windows and MacOS
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)    # For Linux
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)    # For Linux

    def _unbind_mouse_wheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1, "units")

def mainframe(achievements_tab):
    # Create main frame for achievements content
    global main_frame
    main_frame = ttk.Frame(achievements_tab)
    main_frame.pack(side="top", fill="both")

    # Create game count frame
    played_games_frame = ttk.Frame(achievements_tab)
    played_games_frame.pack(padx=10, pady=10)

    # Create game count
    global played_games_count
    played_games_count = 0
    global played_games_label
    played_games_label = ttk.Label(played_games_frame, text=f"Played Games: {played_games_count}")
    played_games_label.pack(side="bottom")

    # Create frame for search bar
    searchbar_frame = ttk.Frame(main_frame)
    searchbar_frame.pack(side="left")
    global search_var
    search_var = tk.StringVar()
    placeholder = "Enter AppID or Name..."

    # Placeholder function
    def clear_placeholder(event=None):
        if search_var.get() == placeholder:
            searchbar.delete(0, tk.END)

    def restore_placeholder(event=None):
        if search_var.get() == "":
            searchbar.insert(0, placeholder)

    global searchbar
    searchbar = ttk.Entry(searchbar_frame, textvariable=search_var, width=40)
    searchbar.insert(0, placeholder)
    searchbar.bind("<FocusIn>", clear_placeholder)
    searchbar.bind("<FocusOut>", restore_placeholder)
    searchbar.pack(side=tk.LEFT, padx=10, pady=10)

    # Create widget for info
    info_frame = tk.Frame(main_frame)
    info_frame.pack(side="right")
    global info_label
    info_label = ttk.Label(info_frame, text="Loading game icons...")
    info_label.pack(side="right", padx=10)

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

def on_image_loaded(result, name, appid, row, col, frame, img_list):
    img = result
    if img:
        img = resize_image(img, (50, 50))
        img_tk = ImageTk.PhotoImage(img)
        img_list.append(img_tk)
        icon_label = tk.Label(frame, image=img_tk)
        icon_label.image = img_tk  # Keep a reference to the image
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

def update_info_label(total_games):
    info_label.config(text=f"Total games: {total_games}")

def display_games(achievements_tab):
    # Load games from CSV
    games = load_games_from_csv("owned_games.csv")
    sorted_games = sorted(games, key=lambda x: x["name"].lower())

    # Create scrollable frame
    scrollable_frame = ScrollableFrame(achievements_tab)
    scrollable_frame.pack(fill="both", expand=True)

    # Create game widgets
    img_list = []  # List to store image objects
    for i, game in enumerate(sorted_games):
        name = game["name"]
        appid = game["appid"]
        img_url = game["img_icon_url"]

        # Download images asynchronously
        img_future = achievements_executor.submit(download_image, img_url)
        img_future.add_done_callback(
            lambda f, name=name, appid=appid, row=i, frame=scrollable_frame.scrollable_frame, img_list=img_list, total=len(sorted_games):
            on_image_loaded(f.result(), name, appid, row, 0, frame, img_list) or (update_info_label(total) if len(img_list) == total else None)
        )

    # Define a function to scroll to the entry matching the search term
    def scroll_to_entry(event=None):
        search_term = search_var.get().lower()

        # Find the index of the first entry that matches the search term
        for i, game in enumerate(sorted_games):
            if search_term in game["name"].lower() or search_term == str(game["appid"]):
                scrollable_frame.canvas.yview_moveto(i / len(sorted_games))
                break

    # Bind the function to the search bar
    searchbar.bind("<Return>", scroll_to_entry)
