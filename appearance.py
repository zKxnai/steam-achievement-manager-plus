import tkinter as tk
import sv_ttk
from tkinter import ttk

def lightmode_switch(appearance_tab):
    # Create frame for lightmode switch in the main window
    lightmode_frame = ttk.Frame(appearance_tab)
    lightmode_frame.pack(side="top", anchor="nw", padx=10, pady=10)

    # Create lightmode switch in the main window
    lightmode_switch = ttk.Checkbutton(lightmode_frame, text="Lightmode", style="Switch.TCheckbutton", command=sv_ttk.toggle_theme)
    lightmode_switch.pack(side="left")