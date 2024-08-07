import tkinter as tk
import datetime
from tkinter import ttk
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from api import get_latest_news
from utils import ScrollableFrame, clean_news_text
from database import get_owned_games

# Define ThreadPoolExecutor with 10 threads
news_executor = ThreadPoolExecutor(max_workers=10)

def display_news(news_tab):
    # Create a frame for the search bar
    searchbar_frame = ttk.Frame(news_tab)
    searchbar_frame.pack(side="top", fill="x")

    # Create search bar
    search_var = tk.StringVar()
    placeholder = "Enter AppID or Name..."
    
    def clear_placeholder(event=None):
        if search_var.get() == placeholder:
            searchbar.delete(0, tk.END)

    def restore_placeholder(event=None):
        if search_var.get() == "":
            searchbar.insert(0, placeholder)
    
    searchbar = ttk.Entry(searchbar_frame, textvariable=search_var, width=40)
    searchbar.insert(0, placeholder)
    searchbar.bind("<FocusIn>", clear_placeholder)
    searchbar.bind("<FocusOut>", restore_placeholder)
    searchbar.pack(side=tk.LEFT, padx=10, pady=10)

    # Create a scrollable frame
    scrollable_frame = ScrollableFrame(news_tab)
    scrollable_frame.pack(fill="both", expand=True)
    
    # Load news for each game
    games = get_owned_games()
    # Sort the games alphabetically by name
    games = sorted(games, key=lambda x: x["name"].lower())
    game_frames = []

    for game in games:
        appid = game["appid"]
        game_title = game["name"]
        # Create a frame for each game to reference later
        game_frame = ttk.Frame(scrollable_frame.scrollable_frame)
        game_frame.pack(fill="x", padx=10, pady=5)
        game_frames.append((game_frame, appid, game_title))
        # Load news asynchronously
        news_executor.submit(get_news_for_game, appid, game_title, game_frame)
        
    for frame, appid, game_title in game_frames:
        frame.pack(fill="x", padx=10, pady=5)

    # Define a function to scroll to the entry matching the search term
    def scroll_to_entry(event=None):
        search_term = search_var.get().lower()

        # Find the index of the first entry that matches the search term
        for i, (frame, appid, title) in enumerate(game_frames):
            if search_term in title.lower() or search_term == str(appid):
                scrollable_frame.canvas.yview_moveto(i / len(game_frames))
                break

    # Bind the function to the search bar
    searchbar.bind("<Return>", scroll_to_entry)

def get_news_for_game(appid, game_title, parent_frame):
        news_data = get_latest_news(appid)
        if news_data:
            news_text = news_data.get("contents", "")
            news_date = datetime.datetime.fromtimestamp(news_data.get("date", 0), tz=datetime.timezone.utc).strftime("%d.%m.%Y %H:%M")
            # Display news entry
            parent_frame.after(0, display_news_entry, parent_frame, game_title, news_text, news_date)

def display_news_entry(parent_frame, game_title, news_text, news_date):
    # Create a frame for the news entry
    news_frame = ttk.Frame(parent_frame)
    news_frame.pack(fill="x", padx=10, pady=10)
    
    # Add game title
    title_label = ttk.Label(news_frame, text=game_title, font=("Helvetica", 12, "bold"))
    title_label.pack(anchor="w", padx=5, pady=5)
    
    # Add news date
    date_label = ttk.Label(news_frame, text=news_date, font=("Helvetica", 10))
    date_label.pack(anchor="w", padx=5, pady=5)

    # Parse HTML content and extract only text
    soup = BeautifulSoup(news_text, "html.parser")
    news_text = soup.get_text()

    cleaned_text = clean_news_text(news_text)

    # Add news text
    text_label = ttk.Label(news_frame, text=cleaned_text, wraplength=750, justify="left")
    text_label.pack(anchor="w", padx=5, pady=5)