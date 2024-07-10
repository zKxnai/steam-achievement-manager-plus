import tkinter as tk
import subprocess
from tkinter import ttk
from PIL import ImageTk, Image
from concurrent.futures import ThreadPoolExecutor
from utils import ScrollableFrame, download_image, resize_image, resource_path
from database import get_owned_games, load_default_theme, get_achievement_stats, game_has_achievements, save_pinned_game, remove_pinned_game, get_pinned_games
from info import update_info_bar

# Define ThreadPoolExecutor with 10 threads
achievements_executor = ThreadPoolExecutor(max_workers=10)

# Global list to store pinned game appids
pinned_games = set()

def mainframe(achievements_tab, info_bar_label):
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

    # Create dropdown for sorting options
    global sort_var
    sort_var = tk.StringVar()
    sort_options = ["Alphabetical (A-Z)", "Alphabetical (Z-A)", "Most Achievements", "Least Achievements", "Completed (A-Z)", "Uncompleted (A-Z)"]
    sort_dropdown = ttk.Combobox(searchbar_frame, textvariable=sort_var, values=sort_options, state="readonly")
    sort_dropdown.set(sort_options[0])  # Set default value
    sort_dropdown.pack(side=tk.LEFT, padx=10, pady=10)
    sort_dropdown.bind("<<ComboboxSelected>>", lambda event: display_games(achievements_tab, info_bar_label, sort_var.get()))

    # Create widget for info
    info_frame = tk.Frame(main_frame)
    info_frame.pack(side="right")
    global info_label
    info_label = ttk.Label(info_frame, text="Loading games...")
    info_label.pack(side="right", padx=10)

def on_image_loaded(result, name, appid, row, col, frame, img_list, achievements_tab, info_bar_label):
    global pinned_games
    img = result

    # Load the pin icon once to use it for all game entries
    pin_icon_img = Image.open(resource_path("Resources/Icons/pin_g.png")).resize((14, 14), Image.LANCZOS)
    pin_icon = ImageTk.PhotoImage(pin_icon_img)

    if img:
        img = resize_image(img, (50, 50))
        img_tk = ImageTk.PhotoImage(img)
        img_list.append(img_tk)

        # Check if the frame still exists before creating the widgets
        if not frame.winfo_exists():
            return
        
        icon_label = tk.Label(frame, image=img_tk)
        icon_label.image = img_tk  # Keep a reference to the image
        icon_label.grid(row=row, column=0, padx=10, pady=5, sticky="w")

        # Create a frame to hold the name and additional information
        achievements_info_frame = tk.Frame(frame)
        achievements_info_frame.grid(row=row, column=1, padx=10, pady=5, sticky="w")

        # Create a sub-frame for the name and pin icon
        name_pin_frame = tk.Frame(achievements_info_frame)
        name_pin_frame.grid(row=0, column=0, sticky="w")

        display_name = name + " (Pinned)" if appid in pinned_games else name

        name_label = tk.Label(name_pin_frame, text=display_name)
        name_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Add the pin icon next to the game name
        pin_label = tk.Label(name_pin_frame, image=pin_icon, cursor="hand2")
        pin_label.image = pin_icon  # Keep a reference to the image
        pin_label.grid(row=0, column=1, sticky="w")

        # Make the pin icon clickable
        pin_label.bind("<Button-1>", lambda event, appid=appid: pin_game(appid, achievements_tab, info_bar_label))

        # Check if achievements exist for the game
        if game_has_achievements(appid):
            # Fetch and display achievements information
            unlocked_achievements, total_achievements = get_achievement_stats(appid)

            # If game has 100%, change text color to green
            if unlocked_achievements == total_achievements:
                # Add progress bar below the name
                achievement_progress = (unlocked_achievements / total_achievements) * 100 if total_achievements else 0
                progress = ttk.Progressbar(achievements_info_frame, length=100, mode='determinate')
                progress.grid(row=1, column=0, sticky="w")
                progress['value'] = achievement_progress

                achievement_progress_label = ttk.Label(achievements_info_frame, text=f"{achievement_progress:.2f}%", foreground="Green")
                achievement_progress_label.configure(font=("Helvetica", 9, "normal"))
                achievement_progress_label.grid(row=1, column=0, sticky="w", padx=(105, 0)) # Adjust padx as needed

                achievements_count = ttk.Label(achievements_info_frame, text=f"{unlocked_achievements}/{total_achievements}", foreground="Green")
                achievements_count.configure(font=("Helvetica", 9, "normal"))
                achievements_count.grid(row=1, column=0, sticky="w", padx=(170, 0)) # Adjust padx as needed

            else:
                # Add progress bar below the name
                achievement_progress = (unlocked_achievements / total_achievements) * 100 if total_achievements else 0
                progress = ttk.Progressbar(achievements_info_frame, length=100, mode='determinate')
                progress.grid(row=1, column=0, sticky="w")
                progress['value'] = achievement_progress

                achievement_progress_label = ttk.Label(achievements_info_frame, text=f"{achievement_progress:.2f}%")
                achievement_progress_label.configure(font=("Helvetica", 9, "normal"))
                achievement_progress_label.grid(row=1, column=0, sticky="w", padx=(105, 0)) # Adjust padx as needed

                achievements_count = ttk.Label(achievements_info_frame, text=f"{unlocked_achievements}/{total_achievements}")
                achievements_count.configure(font=("Helvetica", 9, "normal"))
                achievements_count.grid(row=1, column=0, sticky="w", padx=(170, 0)) # Adjust padx as needed

        else:
            # Display message when no achievements available
            no_achievements_label = ttk.Label(achievements_info_frame, text="No achievements available")
            no_achievements_label.configure(font=("Helvetica", 9, "normal"))
            no_achievements_label.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Configure columns to distribute evenly
        achievements_info_frame.grid_columnconfigure(0, weight=1)  # Adjust weight as needed
        achievements_info_frame.grid_columnconfigure(1, weight=1)  # Adjust weight as needed
        achievements_info_frame.grid_columnconfigure(2, weight=1)  # Adjust weight as needed
        
        # Add buttons
        play_button_img = tk.PhotoImage(file=resource_path("Resources/Icons/play_g.png"))
        play_button = ttk.Button(frame, text="Play", image=play_button_img, compound="left", command=lambda appid=appid: open_hidden(appid), width=10)
        play_button.image = play_button_img
        play_button.grid(row=row, column=2, padx=10, pady=5, sticky="e")
        
        pause_button_img = tk.PhotoImage(file=resource_path("Resources/Icons/pause_g.png"))
        pause_button = ttk.Button(frame, text="Pause", image=pause_button_img, compound="left", command=lambda name=name: close_hidden(name), width=10)
        pause_button.image = pause_button_img
        pause_button.grid(row=row, column=3, padx=10, pady=5, sticky="e")
        
        achievement_button_img = tk.PhotoImage(file=resource_path("Resources/Icons/achievements_g.png"))
        achievement_button = ttk.Button(frame, text="Achievements", image=achievement_button_img, compound="left", command=lambda appid=appid: open_achievements_window(appid))
        achievement_button.image = achievement_button_img
        achievement_button.grid(row=row, column=4, padx=10, pady=5, sticky="e")

        # Update button states when clicked
        play_button.config(command=lambda appid=appid, button=play_button: play_button_clicked(appid, button))
        pause_button.config(command=lambda name=name, button=play_button: pause_button_clicked(name, button))

    else:
        print(f"Skipping game '{name}' due to missing or invalid image.")

def pin_game(appid, achievements_tab, info_bar_label):
    global pinned_games

    # Retrieve all owned games from the database
    games = get_owned_games()

    if appid in pinned_games:
        remove_pinned_game(appid)
        pinned_games.remove(appid)
        display_games(achievements_tab, info_bar_label, sort_var.get()) # Refresh the game display to update labels
        game_name = next((game["name"] for game in games if game["appid"] == appid), str(appid))
        info_bar_label.config(text=f"{game_name} successfully unpinned.")
    else:
        save_pinned_game(appid)
        pinned_games.add(appid)
        display_games(achievements_tab, info_bar_label, sort_var.get()) # Refresh the game display to update labels
        game_name = next((game["name"] for game in games if game["appid"] == appid), str(appid))
        info_bar_label.config(text=f"{game_name} successfully pinned.")
  
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
    global played_games_count, game_process
    played_games_count += 1
    played_games_label.config(text=f"Played Games: {played_games_count}")
    exe_path = resource_path("Resources/API/Darkmode/bin/SAM.Game.exe")
    cmdline = f'"{exe_path}" {appid}'

    startupinfo = subprocess.STARTUPINFO()
    startupinfo.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startupinfo.wShowWindow = subprocess.SW_HIDE

    game_process = subprocess.Popen(cmdline, startupinfo=startupinfo)

def open_achievements_window(appid):
    # Define the set of dark mode themes
    dark_mode_themes = {
        "Dark",
        "Forest Dark",
        "Azure Dark"
    }
    current_theme = load_default_theme()
    # Check if the current theme is a dark mode theme
    if current_theme in dark_mode_themes:
        subprocess.Popen([resource_path("Resources/API/Darkmode/bin/SAM.Game.exe"), str(appid)])
    else:
        subprocess.Popen([resource_path("Resources/API/Lightmode/bin/SAM.Game.exe"), str(appid)])
    
# Function to close the hidden window opened by open_hidden
def close_hidden(name):
    global played_games_count, game_process
    played_games_count -= 1
    played_games_label.config(text=f"Played Games: {played_games_count}")

    if game_process:
        try:
            game_process.terminate()  # Terminate the game process
            game_process = None  # Reset game_process variable

        except Exception as e:
            print(f"Error terminating game process: {e}")

def update_info_label(total_games):
    info_label.config(text=f"Total games: {total_games}")

# Initialize the scrollable_frame as None initially
scrollable_frame = None

def display_games(achievements_tab, info_bar_label, sort_option="Alphabetical (A-Z)"):
    global scrollable_frame  # Ensure we are referencing the global variable
    global pinned_games

    # Load pinned games
    pinned_games = get_pinned_games()

    # Load games from CSV
    games = get_owned_games()

    # Initialize sorted_games with an empty list
    sorted_games = []

    # Apply sorting based on the selected option
    if sort_option == "Alphabetical (A-Z)":
        sorted_games = sorted(games, key=lambda x: x["name"].lower())
        update_info_bar(info_bar_label, "Games sorted Alphabetically (A-Z).")
    elif sort_option == "Alphabetical (Z-A)":
        sorted_games = sorted(games, key=lambda x: x["name"].lower(), reverse=True)
        update_info_bar(info_bar_label, "Games sorted Alphabetically (Z-A).")
    elif sort_option == "Most Achievements":
        sorted_games = sorted(games, key=lambda x: get_achievement_stats(x["appid"])[1], reverse=True)
        update_info_bar(info_bar_label, "Games sorted by Most Achievements.")
    elif sort_option == "Least Achievements":
        games = [g for g in games if game_has_achievements(g["appid"]) and get_achievement_stats(g["appid"])[1] > 0]
        sorted_games = sorted(games, key=lambda x: get_achievement_stats(x["appid"])[1])
        update_info_bar(info_bar_label, "Games sorted by Least Achievements.")
    elif sort_option == "Completed (A-Z)":
        games = [g for g in games if game_has_achievements(g["appid"]) and get_achievement_stats(g["appid"])[0] == get_achievement_stats(g["appid"])[1]]
        sorted_games = sorted(games, key=lambda x: x["name"].lower())
        update_info_bar(info_bar_label, "Games sorted by Completion (A-Z).")
    elif sort_option == "Uncompleted (A-Z)":
        games = [g for g in games if game_has_achievements(g["appid"]) and get_achievement_stats(g["appid"])[0] < get_achievement_stats(g["appid"])[1]]
        sorted_games = sorted(games, key=lambda x: x["name"].lower())
        update_info_bar(info_bar_label, "Games sorted by Uncompletion (A-Z).")

    # Prioritize pinned games
    sorted_games = [game for game in sorted_games if game["appid"] in pinned_games] + \
                   [game for game in sorted_games if game["appid"] not in pinned_games]

    # Create scrollable frame if it doesn't exist
    if not scrollable_frame:
        scrollable_frame = ScrollableFrame(achievements_tab)
        scrollable_frame.pack(fill="both", expand=True)

    # Clear existing widgets in the scrollable frame
    for widget in scrollable_frame.scrollable_frame.winfo_children():
        widget.destroy()

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
            on_image_loaded(f.result(), name, appid, row, 0, frame, img_list, achievements_tab, info_bar_label) or (update_info_label(total) if len(img_list) == total else None)
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