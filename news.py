import tkinter as tk
import datetime
from tkinter import ttk
from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
from api import get_latest_news, load_games_from_csv

# Define ThreadPoolExecutor with 10 threads
news_executor = ThreadPoolExecutor(max_workers=10)

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

        # Bind the mouse wheel to the canvas for scrolling
        self.bind_mouse_wheel(self.canvas)

    def bind_mouse_wheel(self, widget):
        widget.bind_all("<MouseWheel>", self._on_mousewheel)  # For Windows and MacOS

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1, "units")

def display_news(news_tab):
    # Create a scrollable frame for news entries
    scrollable_frame = ScrollableFrame(news_tab)
    scrollable_frame.pack(fill="both", expand=True)
    
    # Load news for each game
    games = load_games_from_csv("owned_games.csv")
    for game in games:
        appid = game["appid"]
        game_title = game["name"]
        # Load news asynchronously
        news_future = news_executor.submit(get_news_for_game, appid, game_title, scrollable_frame.scrollable_frame)
        news_future.add_done_callback(lambda x: print("News loaded for", game_title))

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
    
    # Add news text
    text_label = ttk.Label(news_frame, text=news_text, wraplength=750, justify="left")
    text_label.pack(anchor="w", padx=5, pady=5)