import tkinter as tk
import datetime
import csv
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor
from api import get_latest_news
from achievements import load_games_from_csv

# Define ThreadPoolExecutor with 5 threads
news_executor = ThreadPoolExecutor(max_workers=5)

def display_news(news_tab):
    # Load news for each game
    games = load_games_from_csv("owned_games.csv")
    for game in games:
        appid = game["appid"]
        game_title = game["name"]
        # Load news asynchronously
        news_future = news_executor.submit(get_news_for_game, appid, game_title, news_tab)
        news_future.add_done_callback(lambda x: print("News loaded for", game_title))

def get_news_for_game(appid, game_title, news_tab):
    news_data = get_latest_news(appid)
    if news_data:
        news_text = news_data.get("contents", "")
        news_date = datetime.datetime.fromtimestamp(news_data.get("date", 0), tz=datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
        # Display news entry
        news_tab.after(0, display_news_entry, news_tab, game_title, news_text, news_date)

def display_news_entry(news_tab, game_title, news_text, news_date):
    # Create a frame for the news entry
    news_frame = ttk.Frame(news_tab)
    news_frame.pack(fill="x", padx=10, pady=10)
    
    # Add game title
    title_label = ttk.Label(news_frame, text=game_title, font=("Helvetica", 12, "bold"))
    title_label.pack(anchor="w", padx=5, pady=5)
    
    # Add news date
    date_label = ttk.Label(news_frame, text=news_date, font=("Helvetica", 10, "italic"))
    date_label.pack(anchor="w", padx=5, pady=5)
    
    # Add news text
    text_label = tk.Text(news_frame, wrap="word", width=80, height=10)
    text_label.insert("1.0", news_text)
    text_label.config(state="disabled")
    text_label.pack(anchor="w", padx=5, pady=5)
