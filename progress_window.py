import customtkinter as ctk
from utils import resource_path

icon_path = resource_path("Resources/Icons/SAM+ Logo.ico")

class ProgressWindow:
    def __init__(self, root):
        self.root = root
        self.progress_window = ctk.CTkToplevel(root)
        self.progress_window.title("Loading SAM+...")
        self.progress_window.geometry("300x100")
        self.progress_window.resizable(False, False)
        self.progress_window.after(250, lambda: self.progress_window.iconbitmap(icon_path))

        self.progress_label = ctk.CTkLabel(self.progress_window, text="Initializing...")
        self.progress_label.pack(pady=10)

        self.progress_bar = ctk.CTkProgressBar(self.progress_window, orientation="horizontal")
        self.progress_bar.pack(pady=10, padx=20, fill="x")
        self.progress_bar.start()

        self.progress_window.protocol("WM_DELETE_WINDOW", self.on_close)

    def update_progress(self, text):
        self.progress_label.configure(text=text)

    def on_close(self):
        pass  # Override the close button to prevent closing

    def close(self):
        self.progress_bar.stop()
        self.progress_window.destroy()
