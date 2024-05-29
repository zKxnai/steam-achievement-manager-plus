import sv_ttk
import customtkinter as ctk
from tkinter import ttk

def set_default_theme():
    sv_ttk.set_theme("dark")
    ctk.set_appearance_mode("dark")

def toggle_light_mode():
    ctk.set_appearance_mode("light")
    sv_ttk.set_theme("light")
        
def theme_switch(appearance_tab):
    # Create frame for lightmode switch in the main window
    theme_change_frame = ttk.Frame(appearance_tab)
    theme_change_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)
    toggle_theme_label = ttk.Label(theme_change_frame, text="Change appearance")
    toggle_theme_label.configure(font=("Helvetica", 13, "bold underline"))
    toggle_theme_label.grid(row=0, column=0, sticky="n", padx=10, pady=10)

    # Create lightmode switch in the appearance tab
    lightmode_label = ttk.Label(theme_change_frame, text="Toogle Lightmode:")
    lightmode_label.grid(row=1, column=0, sticky="n", padx=10, pady=10)
    lightmode_switch = ttk.Button(theme_change_frame, text="Lightmode", command=toggle_light_mode)
    lightmode_switch.grid(row=1, column=1, sticky="n", padx=10, pady=5)

    # Create darkmode switch in the appearance tab
    darkmode_label = ttk.Label(theme_change_frame, text="Toogle Darkmode:")
    darkmode_label.grid(row=2, column=0, sticky="n", padx=10, pady=10)
    darkmode_switch = ttk.Button(theme_change_frame, text="Darkmode", command=set_default_theme)
    darkmode_switch.grid(row=2, column=1, sticky="n", padx=10, pady=5)