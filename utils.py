import tkinter as tk
import re
import requests
import sys
import os
from tkinter import ttk
from PIL import Image
from io import BytesIO

app_version = "1.0.1"

class ScrollableFrame(ttk.Frame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.canvas.bind("<Enter>", self._bind_mouse_wheel)
        self.canvas.bind("<Leave>", self._unbind_mouse_wheel)

    def _bind_mouse_wheel(self, event):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbind_mouse_wheel(self, event):
        self.canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        if event.num == 5 or event.delta == -120:
            self.canvas.yview_scroll(1, "units")
        elif event.num == 4 or event.delta == 120:
            self.canvas.yview_scroll(-1, "units")

def clean_news_text(news_text):
    news_text = re.sub(r"{STEAM_CLAN_IMAGE}/\S+\.(png|jpg|gif)", "", news_text, flags=re.IGNORECASE)
    news_text = re.sub(r"https?://\S+(\s|$)", "", news_text)
    return news_text.strip()
    
def resize_image(image, size):
    return image.resize(size)

def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return Image.open(BytesIO(response.content))
        else:
            print(f"Failed to download image from {url}: {response.status_code}")
    except Exception as e:
        print(f"Error downloading image from {url}: {e}")

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)