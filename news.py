import tkinter as tk
from tkinter import ttk
from concurrent.futures import ThreadPoolExecutor

# Define ThreadPoolExecutor with 5 threads
news_executor = ThreadPoolExecutor(max_workers=5)

# Temporarily deprecated
def newsinfolabel(news_tab):
    news_info = ttk.Label(news_tab, text="Development temporarily paused")
    news_info.pack(side="top", padx=10, pady=10)