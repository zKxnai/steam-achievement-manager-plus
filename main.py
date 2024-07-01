import customtkinter as ctk
from tkinter import ttk
from PIL import Image, ImageTk
from achievements import mainframe, display_games
from appearance import set_default_theme, theme_switch
from news import display_news
from utils import app_version, resource_path
from key import apikey_frame
from api import get_owned_games, API_key, steam_id
from concurrent.futures import ThreadPoolExecutor
from info import create_info_bar

# Define ThreadPoolExecutor with 10 threads
achievements_stats_executor = ThreadPoolExecutor(max_workers=10)
  
# Absolute icon paths
icon_path = resource_path("Resources/Icons/SAM+ Logo.ico")
home_icon_path = resource_path("Resources/Icons/home_g.png")
achievements_icon_path = resource_path("Resources/Icons/achievements_g.png")
news_icon_path = resource_path("Resources/Icons/news_g.png")
appearance_icon_path = resource_path("Resources/Icons/settings_g.png")
steam_api_icon_path = resource_path("Resources/Icons/keyword_g.png")

# Main window
main = ctk.CTk()
main.title(f"Steam Achievement Manager+ {app_version}")
main.iconbitmap(icon_path)
main.geometry("850x600")

# Create a Notebook (tabbed layout)
notebook = ttk.Notebook(main)
notebook.pack(fill="both", expand=True)

# Loads icons for tabs
home_icon = ImageTk.PhotoImage(Image.open(home_icon_path).resize((16,16)))
achievements_icon = ImageTk.PhotoImage(Image.open(achievements_icon_path).resize((16,16)))
news_icon = ImageTk.PhotoImage(Image.open(news_icon_path).resize((16,16)))
appearance_icon = ImageTk.PhotoImage(Image.open(appearance_icon_path).resize((16,16)))
steam_api_icon = ImageTk.PhotoImage(Image.open(steam_api_icon_path).resize((16,16)))

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

# Get owned games
achievements_stats_executor.submit(get_owned_games, API_key, steam_id)

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

# Pass to achievements
mainframe(achievements_tab)
display_games(achievements_tab, sort_option="Alphabetical (A-Z)")

# Pass to news
display_news(news_tab)

# Pass to appearance
theme_switch(appearance_tab, main, info_bar_label)

# Pass to key
apikey_frame(api_key_tab)

main.mainloop()