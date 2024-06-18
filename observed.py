from tkinter import ttk
from utils import ScrollableFrame

def observedframe(observed_tab):
    # Create a scrollable frame for news entries
    scrollable_frame = ScrollableFrame(observed_tab)
    scrollable_frame.pack(fill="both", expand=True)