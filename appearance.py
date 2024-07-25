import sv_ttk
import customtkinter as ctk
from tkinter import ttk
from database import save_default_theme, load_default_theme
from info import update_info_bar

is_azure_initialized = False
current_theme_label = None
default_theme_label = None

def set_button_style():
    # Define a custom style for the green "Playing..." button
    button_style = ttk.Style()
    button_style.configure("Green.TButton", foreground="green")

def set_default_theme():
    system_mode = ctk.get_appearance_mode()
    if system_mode == "Dark":
        set_button_style()
    else:
        set_button_style()
    update_current_theme_label(system_mode)
    
def toggle_sv_dark(info_bar_label):
    sv_ttk.set_theme("dark")
    ctk.set_appearance_mode("dark")
    set_button_style()
    update_current_theme_label("Sun Valley Dark")
    update_info_bar(info_bar_label, "Sun Valley Dark theme applied successfully.")

def toggle_sv_light(info_bar_label):
    sv_ttk.set_theme("light")
    ctk.set_appearance_mode("light")
    set_button_style()
    update_current_theme_label("Sun Valley Light")
    update_info_bar(info_bar_label, "Sun Valley Light theme applied successfully.")

"""
def initialize_azure_theme(main):
    global is_azure_initialized
    if not is_azure_initialized:
        main.tk.call("source", resource_path("Resources/Themes/Azure-ttk-theme-2.1.0/azure.tcl"))
        is_azure_initialized = True

def toggle_azure_dark(main, info_bar_label):
    initialize_azure_theme(main)
    main.tk.call("set_theme", "dark")
    ctk.set_appearance_mode("dark")
    set_button_style()
    update_current_theme_label("Azure Dark")
    update_info_bar(info_bar_label, "Azure Dark theme applied successfully.")

def toggle_azure_light(main, info_bar_label):
    initialize_azure_theme(main)
    main.tk.call("set_theme", "light")
    ctk.set_appearance_mode("light")
    set_button_style()
    update_current_theme_label("Azure Light")
    update_info_bar(info_bar_label, "Azure Light theme applied successfully.")
"""

def update_current_theme_label(theme):
    theme_display_map = {
        "Dark": "Sun Valley Dark",
        "Light": "Sun Valley Light",
        "Azure Dark": "Azure Dark",
        "Azure Light": "Azure Light"
    }

    display_theme = theme_display_map.get(theme, theme)
    if current_theme_label:
        current_theme_label.config(text=f"Current Theme: {display_theme}")

def set_default_theme_label(theme):
    theme_display_map = {
        "Dark": "Sun Valley Dark",
        "Light": "Sun Valley Light",
        "Azure Dark": "Azure Dark",
        "Azure Light": "Azure Light"
    }

    display_theme = theme_display_map.get(theme, theme)
    if default_theme_label:
        default_theme_label.config(text=f"Default Theme: {display_theme}")

def apply_default_theme(main, info_bar_label):
    default_theme = load_default_theme()
    if default_theme:
        if default_theme == "Dark":
            toggle_sv_dark(info_bar_label)
        elif default_theme == "Light":
            toggle_sv_light(info_bar_label)
        """
        elif default_theme == "Azure Dark":
            toggle_azure_dark(main, info_bar_label)
        elif default_theme == "Azure Light":
            toggle_azure_light(main, info_bar_label)
        """
        update_current_theme_label(default_theme)
        set_default_theme_label(default_theme)

def save_and_update_default_theme(theme_name, info_bar_label):
    theme_map = {
        "Sun Valley Dark": "Dark",
        "Sun Valley Light": "Light",
        "Azure Dark": "Azure Dark",
        "Azure Light": "Azure Light"
    }

    # Get the simplified theme name for saving
    theme = theme_map.get(theme_name)

    # Save the default theme to the file
    if theme:
        save_default_theme(theme)
        set_default_theme_label(theme_name)
        update_info_bar(info_bar_label, f"Default Theme successfully set to {theme_name}.")
    else:
        update_info_bar(info_bar_label, "Theme not found.")

def theme_switch(appearance_tab, main, info_bar_label):
    global current_theme_label, default_theme_label
    # Create frame for lightmode switch in the main window
    theme_change_frame = ttk.Frame(appearance_tab)
    theme_change_frame.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

    # Create info frame
    info_frame = ttk.Frame(appearance_tab)
    info_frame.grid(row=0, column=1, sticky="ne", padx=10, pady=10)

    # Create label for current theme
    current_theme_label = ttk.Label(info_frame, text="Current Theme: ")
    current_theme_label.grid(row=0, column=0, padx=10, pady=10, sticky="e")

    # Create label for default theme
    default_theme_label = ttk.Label(info_frame, text="Default Theme: ")
    default_theme_label.grid(row=1, column=0, padx=10, pady=10, sticky="e")

    # Create Set Default button
    set_default_button = ttk.Button(info_frame, text="Set Current Theme as Default", command=lambda: save_and_update_default_theme(current_theme_label.cget("text").replace("Current Theme: ", ""), info_bar_label))
    set_default_button.grid(row=2, column=0, padx=10, pady=10, sticky="e")

    # Create label for theme mode switch
    sv_toggle_theme_label = ttk.Label(theme_change_frame, text='Set theme to "Sun Valley"')
    sv_toggle_theme_label.configure(font=("Helvetica", 13, "bold underline"))
    sv_toggle_theme_label.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

    # Create lightmode switch in the appearance tab
    sv_lightmode_label = ttk.Label(theme_change_frame, text="Toogle Lightmode:")
    sv_lightmode_label.grid(row=1, column=0, sticky="nw", padx=10, pady=10)
    sv_lightmode_switch = ttk.Button(theme_change_frame, text="Lightmode", command=lambda: toggle_sv_light(info_bar_label))
    sv_lightmode_switch.grid(row=1, column=1, sticky="nw", padx=10, pady=5)

    # Create darkmode switch in the appearance tab
    sv_darkmode_label = ttk.Label(theme_change_frame, text="Toogle Darkmode:")
    sv_darkmode_label.grid(row=2, column=0, sticky="nw", padx=10, pady=10)
    sv_darkmode_switch = ttk.Button(theme_change_frame, text="Darkmode", command=lambda: toggle_sv_dark(info_bar_label))
    sv_darkmode_switch.grid(row=2, column=1, sticky="nw", padx=10, pady=5)

    # Info text regarding theme switch
    theme_info_text = ttk.Label(theme_change_frame, text="\n\n\nDisclaimer: When changing the theme, please set it as Default to fully apply it.")
    theme_info_text.grid(row=3, column=0, sticky="nw", padx=10, pady=10)

    """
    # Create label for additional theme switches
    azure_placeholder_label = ttk.Label(theme_change_frame, text="")
    azure_placeholder_label.grid(row=3, column=0, sticky="nw", padx=10, pady=10)
    azure_toggle_theme_label = ttk.Label(theme_change_frame, text='Set theme to "Azure"')
    azure_toggle_theme_label.configure(font=("Helvetica", 13, "bold underline"))
    azure_toggle_theme_label.grid(row=4, column=0, sticky="nw", padx=10, pady=10)

    # Create azure lightmode switch in the appearance tab
    azure_lightmode_label = ttk.Label(theme_change_frame, text="Toogle Lightmode:")
    azure_lightmode_label.grid(row=5, column=0, sticky="nw", padx=10, pady=10)
    azure_lightmode_switch = ttk.Button(theme_change_frame, text="Lightmode", command=lambda: toggle_azure_light(main, info_bar_label))
    azure_lightmode_switch.grid(row=5, column=1, sticky="nw", padx=10, pady=5)

    # Create azure darkmode switch in the appearance tab
    azure_darkmode_label = ttk.Label(theme_change_frame, text="Toogle Darkmode:")
    azure_darkmode_label.grid(row=6, column=0, sticky="nw", padx=10, pady=10)
    azure_darkmode_switch = ttk.Button(theme_change_frame, text="Darkmode", command=lambda: toggle_azure_dark(main, info_bar_label))
    azure_darkmode_switch.grid(row=6, column=1, sticky="nw", padx=10, pady=5)
    """

    # Apply the default theme on startup
    apply_default_theme(main, info_bar_label)