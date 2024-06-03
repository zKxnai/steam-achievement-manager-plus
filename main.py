import customtkinter as ctk
from tkinter import ttk
from achievements import mainframe, display_games
from appearance import set_default_theme, theme_switch
from news import display_news
from observed import observedinfolabel

# Main window
main = ctk.CTk()
main.title("Steam Achievement Manager+ 0.6.8.3")
main.iconbitmap("Resources/SAM+ Logo.ico")
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

# Configure the appearance_tab's row and columns
appearance_tab.columnconfigure(0, weight=1)

# Change theme
set_default_theme()

# Creating landing page
landing_page_frame = ttk.Frame(landing_tab)
landing_page_frame.grid(row=0, column=0, sticky="w", padx=10, pady=10)

landing_page_label = ttk.Label(landing_page_frame, text="Welcome to SAM+!")
landing_page_label.configure(font=("Helvetica", 15, "bold underline"))
landing_page_label.grid(row=0, column=0, sticky="w", padx=10, pady=10)

landing_page_text = ttk.Label(landing_page_frame, text="Choose one of the tabs above to continue.")
landing_page_text.grid(row=1, column=0, sticky="w", padx=10, pady=10)

landing_page_text_achievements = ttk.Label(landing_page_frame, text="- Achievements: Enables you to farm playtime or edit your achievements for your desired game.")
landing_page_text_achievements.grid(row=2, column=0, sticky="w", padx=10, pady=10)

landing_page_text_news = ttk.Label(landing_page_frame, text="- News: Shows you the latest news released for every owned game.")
landing_page_text_news.grid(row=3, column=0, sticky="w", padx=10, pady=10)

landing_page_text_observed = ttk.Label(landing_page_frame, text="- Observed Games: Lets you view your observed games.")
landing_page_text_observed.grid(row=4, column=0, sticky="w", padx=10, pady=10)

landing_page_text_appearance = ttk.Label(landing_page_frame, text="- Appearance: Change the appearance of SAM+.")
landing_page_text_appearance.grid(row=5, column=0, sticky="w", padx=10, pady=10)

# Pass to achievements
mainframe(achievements_tab)
display_games(achievements_tab)

# Pass to news
display_news(news_tab)

# Pass to observed
observedinfolabel(observed_games_tab)

# Pass to appearance
theme_switch(appearance_tab, main)

main.mainloop()