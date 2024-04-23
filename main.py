import tkinter as tk
import sv_ttk
import news
import appearance
import api
import observed
import achievements
from tkinter import ttk

# Main window
main = tk.Tk()
main.title("Steam Achievement Manager+ 0.6.1")
main.geometry("843x600")

# Create a Notebook (tabbed layout)
notebook = ttk.Notebook(main)
notebook.pack(fill="both", expand=True)

# Create frames for each tab
landing_tab = ttk.Frame(notebook)
achievements_tab = ttk.Frame(notebook)
news_tab = ttk.Frame(notebook)
observed_games_tab = ttk.Frame(notebook)
appearance_tab = ttk.Frame(notebook)

# Add tabs to the notebook
notebook.add(landing_tab, text="Landing Page")
notebook.add(achievements_tab, text='Achievements')
notebook.add(news_tab, text='News')
notebook.add(observed_games_tab, text='Observed Games')
notebook.add(appearance_tab, text='Appearance')

# Change app icon
icon_image = tk.PhotoImage(file="Resources/SAM+ Logo.png")
main.iconphoto(True, icon_image)

# Change theme
sv_ttk.set_theme("dark")

# Pass to news
news.newsinfolabel(news_tab)

# Pass to appearance
appearance.lightmode_switch(appearance_tab)

##### Landing page ########

main.mainloop()