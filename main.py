import customtkinter as ctk
import threading
import time
import requests
import webbrowser
from tkinter import ttk
from PIL import Image, ImageTk
from achievements import mainframe, display_games
from appearance import set_default_theme, theme_switch
from news import display_news
from utils import app_version, resource_path, ToolTip
from key import apikey_frame
from api import get_owned_games, API_key, steam_id
from info import create_info_bar
from progress_window import ProgressWindow
  
# Absolute icon paths
icon_path = resource_path("Resources/Icons/SAM+ Logo.ico")
home_icon_path = resource_path("Resources/Icons/home_g.png")
achievements_icon_path = resource_path("Resources/Icons/achievements_g.png")
news_icon_path = resource_path("Resources/Icons/news_g.png")
appearance_icon_path = resource_path("Resources/Icons/settings_g.png")
steam_api_icon_path = resource_path("Resources/Icons/keyword_g.png")
github_icon_path = resource_path("Resources/Icons/github-mark_g.png")

# Main window
main = ctk.CTk()
main.title(f"Steam Achievement Manager+ {app_version}")
main.iconbitmap(icon_path)

# Place window in the center of the screen
window_height = 650
window_width = 875
screen_height = main.winfo_screenheight()
screen_width = main.winfo_screenwidth()
x = (screen_width - window_width) // 2
y = (screen_height - window_height) // 2

main.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Create a Notebook (tabbed layout)
notebook = ttk.Notebook(main)
notebook.pack(fill="both", expand=True)

# Loads icons for tabs
home_icon = ImageTk.PhotoImage(Image.open(home_icon_path).resize((16,16)))
achievements_icon = ImageTk.PhotoImage(Image.open(achievements_icon_path).resize((16,16)))
news_icon = ImageTk.PhotoImage(Image.open(news_icon_path).resize((16,16)))
appearance_icon = ImageTk.PhotoImage(Image.open(appearance_icon_path).resize((16,16)))
steam_api_icon = ImageTk.PhotoImage(Image.open(steam_api_icon_path).resize((16,16)))
github_icon = ImageTk.PhotoImage(Image.open(github_icon_path).resize((20,20)))

# Create frames for each tab
home = ttk.Frame(notebook)
achievements_tab = ttk.Frame(notebook)
news_tab = ttk.Frame(notebook)
appearance_tab = ttk.Frame(notebook)
api_key_tab = ttk.Frame(notebook)

# Add tabs to the notebook
notebook.add(home, text="Home", image=home_icon, compound="left")
notebook.add(achievements_tab, text='Achievements', image=achievements_icon, compound="left")
notebook.add(news_tab, text='News', image=news_icon, compound="left")
notebook.add(appearance_tab, text='Appearance', image=appearance_icon, compound="left")
notebook.add(api_key_tab, text='Steam API Key', image=steam_api_icon, compound="left")

# Configure the appearance_tab's row and columns
appearance_tab.columnconfigure(0, weight=1)

# Change theme
set_default_theme()

# Create the info bar and get its label
info_frame, info_bar_label = create_info_bar(main)

# Show progress window
progress_window = ProgressWindow(main)

def fetch_data():
    progress_window.update_progress("Setting up API key...")
    time.sleep(1)
    # Pass to key
    apikey_frame(api_key_tab)
    
    progress_window.update_progress("Fetching news...")
    # Pass to news
    display_news(news_tab)
    time.sleep(2)

    progress_window.update_progress("Fetching owned games...")
    # Get owned games
    get_owned_games(API_key, steam_id)

    progress_window.update_progress("Displaying games...")
    # Pass to achievements
    mainframe(achievements_tab, info_bar_label)
    display_games(achievements_tab, info_bar_label, sort_option="Alphabetical (A-Z)")
    time.sleep(2)

    progress_window.update_progress("Setting up appearance...")
    time.sleep(1)
    # Pass to appearance
    theme_switch(appearance_tab, main, info_bar_label)
    
    # Close progress window
    progress_window.close()

    # After loading, show the main window
    main.deiconify()

    check_for_update(info_bar_label)


def get_latest_github_version():
    url = f"https://api.github.com/repos/zKxnai/steam-achievement-manager-plus/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        release_info = response.json()
        return release_info["tag_name"]
    return None

def is_update_available(app_version, latest_version):
    current_version_parts = list(map(int, app_version.split('.')))
    latest_version_parts = list(map(int, latest_version.split('.')))
    
    return latest_version_parts > current_version_parts

def check_for_update(info_bar_label):
    latest_version = get_latest_github_version()
    if latest_version:
        if is_update_available(app_version, latest_version):
            info_bar_label.config(text=f"Version {latest_version} is available! Please update.", foreground="yellow")
        else:
            info_bar_label.config(text="You are using the latest version.", foreground="green")
    else:
        info_bar_label.config(text="Could not check for updates. Please try again later.", foreground="red")

def open_repo():
    url = "https://github.com/zKxnai/steam-achievement-manager-plus/releases"
    webbrowser.open_new_tab(url)

def add_tooltip(widget, text):
    tooltip = ToolTip(widget, text)
    widget.bind("<Enter>", lambda e: tooltip.show_tip())
    widget.bind("<Leave>", lambda e: tooltip.hide_tip())

# Creating landing page
landing_page_frame = ttk.Frame(home)
landing_page_frame.grid(row=0, column=0, sticky="w", padx=10, pady=10)

landing_page_label = ttk.Label(landing_page_frame, text="Welcome to SAM+!")
landing_page_label.configure(font=("Helvetica", 15, "bold underline"))
landing_page_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

custom_pady = 8
custom_padx = 10

landing_page_text = ttk.Label(landing_page_frame, text="Choose one of the tabs above to continue.")
landing_page_text.grid(row=1, column=0, sticky="w", padx=custom_padx, pady=custom_pady)

landing_page_text_achievements = ttk.Label(landing_page_frame, text="- Achievements: Enables you to farm playtime or edit your achievements for your desired game.")
landing_page_text_achievements.grid(row=2, column=0, sticky="w", padx=custom_padx, pady=custom_pady)

landing_page_text_news = ttk.Label(landing_page_frame, text="- News: Shows you the latest news released for every owned game.")
landing_page_text_news.grid(row=3, column=0, sticky="w", padx=custom_padx, pady=custom_pady)

landing_page_text_appearance = ttk.Label(landing_page_frame, text="- Appearance: Change the appearance of SAM+.")
landing_page_text_appearance.grid(row=4, column=0, sticky="w", padx=custom_padx, pady=custom_pady)

landing_page_text_key = ttk.Label(landing_page_frame, text="- Steam API Key: Insert or change the used Steam API Key.")
landing_page_text_key.grid(row=5, column=0, sticky="w", padx=custom_padx, pady=custom_pady)

# Create github icon to forward to repo
github_icon_label = ttk.Label(landing_page_frame, image=github_icon, cursor="hand2")
github_icon_label.grid(row=6, column=0, sticky="sw", padx=custom_padx, pady=custom_pady)
github_icon_label.bind("<Button-1>", lambda event: open_repo())
add_tooltip(github_icon_label, "Visit my GitHub repository")

# Hide the main window initially
main.withdraw()

# Start the background thread and main loop
thread = threading.Thread(target=fetch_data)
thread.start()

main.mainloop()

# Wait for the thread to complete before exiting the script
thread.join()