
import tkinter as tk
import sv_ttk
import appearance
import news
import achievements
import api
from tkinter import ttk

# Main window
main = tk.Tk()
main.title("Steam Achievement Manager+ 0.5.6")
main.geometry("725x550")

# Create a Notebook (tabbed layout)
notebook = ttk.Notebook(main)
notebook.pack(fill="both", expand=True)

# Create frames for each tab
achievements_tab = ttk.Frame(notebook)
news_tab = ttk.Frame(notebook)
observed_games_tab = ttk.Frame(notebook)
appearance_tab = ttk.Frame(notebook)

# Add tabs to the notebook
notebook.add(achievements_tab, text='Achievements')
notebook.add(news_tab, text='News')
notebook.add(observed_games_tab, text='Observed Games')
notebook.add(appearance_tab, text='Appearance')

# Change app icon
icon_image = tk.PhotoImage(file="Resources/SAM+ Logo.png")
main.iconphoto(True, icon_image)

# Change theme
sv_ttk.set_theme("dark")

# Pass .csv file
games = api.load_games_from_csv("owned_games.csv")

# Pass to appearance
appearance.lightmode_switch(appearance_tab)

# Pass to news
news.news_search_frame(news_tab)
news.all_news_frame(news_tab)
news.display_news_async(news_tab, games)
news.exe_display_news(news_tab)

# Pass to achievements
achievements.containerframe(achievements_tab)
achievements.played_games_frame(achievements_tab)
achievements.display_games(achievements_tab)

# Define a custom style for the green color
main_style = ttk.Style()
main_style.configure("Green.TButton", foreground="green")

main.mainloop()

# Display games
achievements.display_games()
