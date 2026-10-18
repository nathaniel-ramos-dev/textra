# type: ignore
from collections.abc import Callable

import customtkinter as ctk

from main_content import MainFrame

WIN_WIDTH = 1000
WIN_HEIGHT = 700
TITLE = "My Notes App"

class TopBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        frame_font: ctk.CTkFont = kwargs.pop("font", ctk.CTkFont("Arial", 15))
        toggle_preview_fn: Callable = kwargs.pop("toggle_preview_fn", None)

        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=0) 
        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(master=self, text=TITLE, font=frame_font)
        self.label.cget("font").configure(size=18)
        self.label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.toggle_preview = ctk.CTkButton(master=self, text="Hide Preview", command=toggle_preview_fn)
        self.toggle_preview.grid(row=0, column=2, pady=5, padx=(0, 10), sticky="ew")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.preview_visible = True

        MAIN_FONT = ctk.CTkFont("monospace", size=16)
        UI_FONT = ctk.CTkFont("Noto Sans", size=15)

        self.title(TITLE)
        self.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        self.minsize(900, 600)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.topBar = TopBar(master=self, font=UI_FONT, toggle_preview_fn=self.toggle_preview)
        self.topBar.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.mainFrame = MainFrame(master=self, font=MAIN_FONT, preview_visible=self.preview_visible)
        self.mainFrame.grid(row=1, column=0, sticky="nsew", columnspan=2)

    def toggle_preview(self):
        self.preview_visible = not self.preview_visible
        self.mainFrame.set_preview_visible(self.preview_visible)

        btn = self.topBar.toggle_preview
        if self.preview_visible:
            btn.configure(text="Hide Preview")
        else:
            btn.configure(text="Show Preview")

if __name__ == '__main__':
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("./themes/rime.json")
    app = App()
    app.mainloop()
