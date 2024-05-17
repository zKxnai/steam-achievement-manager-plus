import tkinter as tk
import sv_ttk
from tkinter import ttk

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

        # Bind mouse wheel events when the mouse enters and leaves the canvas
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

def set_default_theme():
    sv_ttk.set_theme("dark")

def lightmode_switch(appearance_tab):
    # Create a scrollable frame for news entries
    scrollable_frame = ScrollableFrame(appearance_tab)
    scrollable_frame.pack(fill="both", expand=True)

    # Create frame for lightmode switch in the main window
    lightmode_frame = ttk.Frame(scrollable_frame.scrollable_frame)
    lightmode_frame.pack(side="top", anchor="nw", padx=10, pady=10)

    # Create lightmode switch in the main window
    lightmode_switch = ttk.Checkbutton(lightmode_frame, text="Lightmode", style="Switch.TCheckbutton", command=sv_ttk.toggle_theme)
    lightmode_switch.pack(side="left", padx=10, pady=10)