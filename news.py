import tkinter as tk
import samplus
import requests
import datetime
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor

# Define ThreadPoolExecutor with 5 threads
news_executor = ThreadPoolExecutor(max_workers=5)

# Function to fetch news for each game
def fetch_game_news(appid):
    url = f"http://api.steampowered.com/ISteamNews/GetNewsForApp/v0002/?appid={appid}&count=1&maxlength=500&format=json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        news = data.get("appnews", {}).get("newsitems", [])
        
        # Convert Unix timestamp to human-readable format for each news item
        for item in news:
            item_date = datetime.datetime.fromtimestamp(item.get("date", 0), tz=datetime.timezone.utc)
            item["date"] = item_date.strftime("%Y-%m-%d %H:%M:%S")  # Format the date
            
        return news
    else:
        print(f"Failed to fetch news for appid {appid}")

def fetch_news_async(appid):
    return news_executor.submit(fetch_game_news, appid)

def news_search_frame(news_tab):
    # Create frame for lightmode switch and search bar in the news tab
    news_search_frame = ttk.Frame(news_tab)
    news_search_frame.pack(side="top", fill="x")

    # Create search bar in the news tab
    news_searchbar_frame = ttk.Frame(news_search_frame)
    news_searchbar_frame.pack(side="left")
    news_search_var = tk.StringVar()
    news_placeholder = "Search News..."

    #Placeholder function
    def clear_news_placeholder(event=None):
        if news_search_var.get() == news_placeholder:
            news_searchbar.delete(0, tk.END)

    def restore_news_placeholder(event=None):
        if news_search_var.get() == "":
            news_searchbar.insert(0, news_placeholder)

    news_searchbar = ttk.Entry(news_searchbar_frame, textvariable=news_search_var, width=40)
    news_searchbar.insert(0, news_placeholder)
    news_searchbar.bind("<FocusIn>", clear_news_placeholder)
    news_searchbar.bind("<FocusOut>", restore_news_placeholder)
    news_searchbar.pack(side=tk.LEFT, padx=10, pady=10)

    return news_search_var, news_searchbar

def all_news_frame(news_tab):
    # Create a frame to hold all the news entries
    all_news_frame = ttk.Frame(news_tab)
    all_news_frame.pack(padx=10, pady=10, fill="both", expand=True)

    # Create a canvas to add a scrollbar to the news frame
    news_canvas = tk.Canvas(all_news_frame)
    news_canvas.pack(side="left", fill="both", expand=True)

    # Add a scrollbar to the canvas
    news_scrollbar = ttk.Scrollbar(all_news_frame, orient="vertical", command=news_canvas.yview)
    news_scrollbar.pack(side="right", fill="y")
    news_canvas.configure(yscrollcommand=news_scrollbar.set)

    # Create a frame to contain the news items
    inner_frame = ttk.Frame(news_canvas)
    news_canvas.create_window((0, 0), window=inner_frame, anchor="nw")

    return inner_frame, news_canvas

# Function to display news in the news tab
def display_news_async(news_tab, games):
    news_canvas = all_news_frame
    for game in games:
        appid = game["appid"]
        future_news = fetch_news_async(appid)
        future_news.add_done_callback(
            lambda f, game=game: display_news_callback(f.result(), news_tab, game)
        )

    # Bind mouse wheel event to news canvas for scrolling
    news_canvas.bind_all("<MouseWheel>", lambda event: news_canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

def display_news_callback(news, news_tab, game):
    inner_frame = all_news_frame
    news_canvas = all_news_frame
    appid = game["appid"]
    if news:
        game_frame = ttk.Frame(inner_frame)
        game_frame.pack(side="top", anchor="w", padx=10, pady=10, fill="x")

        # Display game name
        game_name_label = ttk.Label(game_frame, text=game["name"], font=("Arial", 12, "bold"))
        game_name_label.pack(anchor="w", padx=10, pady=(0, 5))

        # Create a subframe for news items
        news_frame = ttk.Frame(game_frame)
        news_frame.pack(anchor="w", padx=10)

        # Display news items in a list
        for item in news:
            news_title_label = ttk.Label(news_frame, text=item["title"], font=("Arial", 10, "bold"), wraplength=600, justify="left")
            news_title_label.pack(anchor="w", padx=10, pady=5)
            news_date_label = ttk.Label(news_frame, text=item["date"])
            news_date_label.pack(anchor="w", padx=10, pady=2)
            news_content_label = ttk.Label(news_frame, text=item["contents"], wraplength=600, justify="left")
            news_content_label.pack(anchor="w", padx=10, pady=5)
            empty_line_label = ttk.Label(news_frame, text="")
            empty_line_label.pack(anchor="w", padx=10, pady=5)
        
        # Update the scroll region of the canvas
        inner_frame.update_idletasks()
        news_canvas.config(scrollregion=news_canvas.bbox("all"))

    else:
        print(f"No news found for appid {appid}")

# Display news
games = samplus.load_games_from_csv("owned_games.csv")
def exe_display_news(news_tab):
    display_news_async(news_tab, games)

# Scroll to news entry
"""
def scroll_to_news_entry(event=None):
    inner_frame = all_news_frame
    news_canvas = all_news_frame
    news_search_var = news_search_frame
    search_term = news_search_var.get().lower()

    # Iterate over the news items to find a match for the search term
    for game_frame in inner_frame.winfo_children():
        game_name_label = game_frame.winfo_children()[0]  # First child is the game name label
        game_name = game_name_label.cget("text").lower()

        # Check if the search term matches the game name
        if search_term in game_name:
            # Get the position of the game frame relative to the canvas height
            relative_y = game_frame.winfo_y() / news_canvas.winfo_height()
            # Scroll to the position of the game frame
            news_canvas.yview_moveto(relative_y)
            break

# Bind the function to the search bar
news_searchbar = news_search_frame
news_searchbar.bind("<Return>", scroll_to_news_entry)
"""