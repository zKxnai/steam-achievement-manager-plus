import tkinter as tk
import datetime
import csv
from tkinter import ttk
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from api import get_latest_news
from api import load_games_from_csv

# Define ThreadPoolExecutor with 5 threads
news_executor = ThreadPoolExecutor(max_workers=10)

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
        news_date = datetime.datetime.fromtimestamp(news_data.get("date", 0), tz=datetime.timezone.utc).strftime("%d.%m.%Y %H:%M")
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
    date_label = ttk.Label(news_frame, text=news_date, font=("Helvetica", 10))
    date_label.pack(anchor="w", padx=5, pady=5)

    # Parse HTML content and extract only text
    soup = BeautifulSoup(news_text, "html.parser")
    news_text = soup.get_text()
    
    # Add news text
    text_label = ttk.Label(news_frame, text=news_text, wraplength=750)
    text_label.pack(anchor="w", padx=5, pady=5)