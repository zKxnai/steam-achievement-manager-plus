import tkinter as tk
from tkinter import ttk

def mainframe(achievements_tab):
    #Create main frame for achievements content
    main_frame = ttk.Frame(achievements_tab)
    main_frame.pack(side="top", fill="both")

    # Create frame for search bar
    searchbar_frame = ttk.Frame(main_frame)
    searchbar_frame.pack(side="left")
    search_var = tk.StringVar()
    placeholder = "Enter AppID or Name..."

    #Placeholder function
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
