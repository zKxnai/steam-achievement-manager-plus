import tkinter as tk
from tkinter import ttk
from utils import ScrollableFrame

# Temporarily deprecated
def observedinfolabel(observed_tab):
    # Create a scrollable frame for news entries
    scrollable_frame = ScrollableFrame(observed_tab)
    scrollable_frame.pack(fill="both", expand=True)

    observed_info = ttk.Label(scrollable_frame.scrollable_frame, text="Development temporarily paused")
    observed_info.pack(side="top", padx=10, pady=10)