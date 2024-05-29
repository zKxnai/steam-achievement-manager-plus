import sv_ttk
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk

def set_default_theme():
    system_mode = ctk.get_appearance_mode()
    print(system_mode)
    if system_mode == "Dark":
        sv_ttk.set_theme("dark")
    else:
        sv_ttk.set_theme("light")

def toggle_dark_mode():
    sv_ttk.set_theme("dark")
    ctk.set_appearance_mode("dark")

def toggle_light_mode():
    ctk.set_appearance_mode("light")
    sv_ttk.set_theme("light")

def toggle_forest_dark(main):
    main.tk.call("source", "Resources/Forest-ttk-theme-1.0/forest-dark.tcl")
    ttk.Style(main).theme_use("forest-dark")

def toggle_forest_light(main):
    main.tk.call("source", "Resources/Forest-ttk-theme-1.0/forest-light.tcl")
    ttk.Style(main).theme_use("forest-light")
        
def theme_switch(appearance_tab, main):
    # Create frame for lightmode switch in the main window
    theme_change_frame = ttk.Frame(appearance_tab)
    theme_change_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

    # Create label for theme mode switch
    toggle_theme_label = ttk.Label(theme_change_frame, text="Change appearance")
    toggle_theme_label.configure(font=("Helvetica", 13, "bold underline"))
    toggle_theme_label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

    # Create lightmode switch in the appearance tab
    lightmode_label = ttk.Label(theme_change_frame, text="Toogle Lightmode:")
    lightmode_label.grid(row=1, column=0, sticky="nw", padx=10, pady=10)
    lightmode_switch = ttk.Button(theme_change_frame, text="Lightmode", command=toggle_light_mode)
    lightmode_switch.grid(row=1, column=1, sticky="nw", padx=10, pady=5)

    # Create darkmode switch in the appearance tab
    darkmode_label = ttk.Label(theme_change_frame, text="Toogle Darkmode:")
    darkmode_label.grid(row=2, column=0, sticky="nw", padx=10, pady=10)
    darkmode_switch = ttk.Button(theme_change_frame, text="Darkmode", command=toggle_dark_mode)
    darkmode_switch.grid(row=2, column=1, sticky="nw", padx=10, pady=5)

    # Create label for additional theme switches
    toggle_theme_label = ttk.Label(theme_change_frame, text='Change theme to "Forest"')
    toggle_theme_label.configure(font=("Helvetica", 13, "bold underline"))
    toggle_theme_label.grid(row=3, column=0, sticky="nw", padx=10, pady=10)

    # Create forest lightmode switch in the appearance tab
    forest_lightmode_label = ttk.Label(theme_change_frame, text="Toogle Lightmode:")
    forest_lightmode_label.grid(row=4, column=0, sticky="nw", padx=10, pady=10)
    forest_lightmode_switch = ttk.Button(theme_change_frame, text="Lightmode", command=lambda: toggle_forest_light(main))
    forest_lightmode_switch.grid(row=4, column=1, sticky="nw", padx=10, pady=5)

    # Create forest darkmode switch in the appearance tab
    forest_darkmode_label = ttk.Label(theme_change_frame, text="Toogle Darkmode:")
    forest_darkmode_label.grid(row=5, column=0, sticky="nw", padx=10, pady=10)
    forest_darkmode_switch = ttk.Button(theme_change_frame, text="Darkmode", command=lambda: toggle_forest_dark(main))
    forest_darkmode_switch.grid(row=5, column=1, sticky="nw", padx=10, pady=5)