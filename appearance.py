import tkinter as tk
import sv_ttk
import TKinterModernThemes as TKMT
from tkinter import ttk
from utils import ScrollableFrame

def set_default_theme():
    sv_ttk.set_theme("dark")

def lightmode_switch(appearance_tab):
    # Create a scrollable frame for news entries
    scrollable_frame = ScrollableFrame(appearance_tab)
    scrollable_frame.pack(fill="both", expand=True)

    # Create frame for lightmode switch in the main window
    lightmode_frame = ttk.Frame(scrollable_frame.scrollable_frame)
    lightmode_frame.pack(side="top", anchor="nw", padx=10, pady=10)

    # Create lightmode switch in the main window
    lightmode_switch = ttk.Checkbutton(lightmode_frame, text="Lightmode", style="Switch.TCheckbutton", command=sv_ttk.toggle_theme)
    lightmode_switch.pack(side="left", padx=10, pady=10)