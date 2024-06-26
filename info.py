from tkinter import ttk

# Create info bar
def create_info_bar(main):
    info_bar = ttk.Frame(main)
    info_bar.pack(fill="x", side="bottom")

    info_bar_label = ttk.Label(info_bar, text="SAM+ successfully started.")
    info_bar_label.pack(padx=10, pady=10, expand=True)

    return info_bar, info_bar_label

# Change info bar content
def update_info_bar(info_bar_label, message):
    info_bar_label.config(text=message)