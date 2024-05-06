import tkinter as tk
from tkinter import ttk

# Temporarily deprecated
def obserevedinfolabel(observed_tab):
    observed_info = ttk.Label(observed_tab, text="Development temporarily paused")
    observed_info.pack(side="top", padx=10, pady=10)