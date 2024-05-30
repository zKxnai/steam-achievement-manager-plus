import sv_ttk
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk

is_azure_initialized = False

def set_button_style():
    # Define a custom style for the green "Playing..." button
    button_style = ttk.Style()
    button_style.configure("Green.TButton", foreground="green")

def set_default_theme():
    system_mode = ctk.get_appearance_mode()
    if system_mode == "Dark":
        sv_ttk.set_theme("dark")
        set_button_style()
    else:
        sv_ttk.set_theme("light")
        set_button_style()

def toggle_dark_mode():
    sv_ttk.set_theme("dark")
    ctk.set_appearance_mode("dark")
    set_button_style()

def toggle_light_mode():
    ctk.set_appearance_mode("light")
    sv_ttk.set_theme("light")
    set_button_style()

def toggle_forest_dark(main):
    main.tk.call("source", "Resources/Forest-ttk-theme-1.0/forest-dark.tcl")
    ttk.Style(main).theme_use("forest-dark")
    ctk.set_appearance_mode("dark")
    set_button_style()

def toggle_forest_light(main):
    main.tk.call("source", "Resources/Forest-ttk-theme-1.0/forest-light.tcl")
    ttk.Style(main).theme_use("forest-light")
    ctk.set_appearance_mode("light")
    set_button_style()

def initialize_azure_theme(main):
    global is_azure_initialized
    if not is_azure_initialized:
        main.tk.call("source", "Resources/Azure-ttk-theme-2.1.0/azure.tcl")
        is_azure_initialized = True

def toggle_azure_dark(main):
    initialize_azure_theme(main)
    main.tk.call("set_theme", "dark")
    ctk.set_appearance_mode("dark")
    set_button_style()

def toggle_azure_light(main):
    initialize_azure_theme(main)
    main.tk.call("set_theme", "light")
    ctk.set_appearance_mode("light")
    set_button_style()
        
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
    placeholder_label = ttk.Label(theme_change_frame, text="")
    placeholder_label.grid(row=3, column=0, sticky="nw", padx=10, pady=10)
    toggle_theme_label = ttk.Label(theme_change_frame, text='Change theme to "Forest"')
    toggle_theme_label.configure(font=("Helvetica", 13, "bold underline"))
    toggle_theme_label.grid(row=4, column=0, sticky="nw", padx=10, pady=10)

    # Create forest lightmode switch in the appearance tab
    forest_lightmode_label = ttk.Label(theme_change_frame, text="Toogle Lightmode:")
    forest_lightmode_label.grid(row=5, column=0, sticky="nw", padx=10, pady=10)
    forest_lightmode_switch = ttk.Button(theme_change_frame, text="Lightmode", command=lambda: toggle_forest_light(main))
    forest_lightmode_switch.grid(row=5, column=1, sticky="nw", padx=10, pady=5)

    # Create forest darkmode switch in the appearance tab
    forest_darkmode_label = ttk.Label(theme_change_frame, text="Toogle Darkmode:")
    forest_darkmode_label.grid(row=6, column=0, sticky="nw", padx=10, pady=10)
    forest_darkmode_switch = ttk.Button(theme_change_frame, text="Darkmode", command=lambda: toggle_forest_dark(main))
    forest_darkmode_switch.grid(row=6, column=1, sticky="nw", padx=10, pady=5)

    # Create label for additional theme switches
    placeholder_label2 = ttk.Label(theme_change_frame, text="")
    placeholder_label2.grid(row=7, column=0, sticky="nw", padx=10, pady=10)
    toggle_theme_label2 = ttk.Label(theme_change_frame, text='Change theme to "Azure"')
    toggle_theme_label2.configure(font=("Helvetica", 13, "bold underline"))
    toggle_theme_label2.grid(row=8, column=0, sticky="nw", padx=10, pady=10)

    # Create azure lightmode switch in the appearance tab
    azure_lightmode_label = ttk.Label(theme_change_frame, text="Toogle Lightmode:")
    azure_lightmode_label.grid(row=9, column=0, sticky="nw", padx=10, pady=10)
    azure_lightmode_switch = ttk.Button(theme_change_frame, text="Lightmode", command=lambda: toggle_azure_light(main))
    azure_lightmode_switch.grid(row=9, column=1, sticky="nw", padx=10, pady=5)

    # Create azure darkmode switch in the appearance tab
    azure_darkmode_label = ttk.Label(theme_change_frame, text="Toogle Darkmode:")
    azure_darkmode_label.grid(row=10, column=0, sticky="nw", padx=10, pady=10)
    azure_darkmode_switch = ttk.Button(theme_change_frame, text="Darkmode", command=lambda: toggle_azure_dark(main))
    azure_darkmode_switch.grid(row=10, column=1, sticky="nw", padx=10, pady=5)