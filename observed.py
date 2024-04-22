import tkinter as tk
from tkinter import ttk

def add_observed_game(name_label, observed_games_tab):
    # Create a frame to hold the observed game
    observed_game_frame = ttk.Frame(observed_games_tab)
    observed_game_frame.pack(fill="x", padx=10, pady=5)

    # Add game name label
    game_name_label = ttk.Label(observed_game_frame, text=name_label)
    game_name_label.pack(side="left", padx=10, pady=5)