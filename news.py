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

        # Bind mouse wheel events when the mouse enters and leaves the canvas
        self.canvas.bind("<Enter>", self._bind_mouse_wheel)
        self.canvas.bind("<Leave>", self._unbind_mouse_wheel)

    def _bind_mouse_wheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse_wheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1, "units")


def display_news(news_tab):
    # Create a frame for the search bar
    searchbar_frame = ttk.Frame(news_tab)
    searchbar_frame.pack(side="top", fill="x", padx=10, pady=10)

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

    # Create a scrollable frame for news entries
    scrollable_frame = ScrollableFrame(news_tab)
    scrollable_frame.pack(fill="both", expand=True)
    
    # Load news for each game
    games = load_games_from_csv("owned_games.csv")
    game_frames = []
    for game in games:
        appid = game["appid"]
        game_title = game["name"]
        # Create a frame for each game to reference later
        game_frame = ttk.Frame(scrollable_frame.scrollable_frame)
        game_frames.append((game_frame, appid, game_title))
        # Load news asynchronously
        news_future = news_executor.submit(get_news_for_game, appid, game_title, game_frame)
        news_future.add_done_callback(lambda x, game_title=game_title: print("News loaded for", game_title , "\n"))
    
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
    
    # Add news text
    text_label = ttk.Label(news_frame, text=news_text, wraplength=750, justify="left")
    text_label.pack(anchor="w", padx=5, pady=5)