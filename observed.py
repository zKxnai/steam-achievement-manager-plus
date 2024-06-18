from tkinter import ttk
from utils import ScrollableFrame

def observedframe(observed_tab):
    # Create a scrollable frame for observed game entries
    observed_frame = ScrollableFrame(observed_tab)
    observed_frame.pack(fill="both", expand=True)