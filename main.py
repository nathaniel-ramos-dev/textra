import customtkinter as ctk
from ctk_markdown import CTkMarkdown

from main_content import MainFrame

WIN_WIDTH = 1000
WIN_HEIGHT = 700
TITLE = "My Notes App"


class TopBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        frame_font: ctk.CTkFont = kwargs.pop("font", ctk.CTkFont("Arial", 15))

        super().__init__(master, **kwargs)
        self.grid_rowconfigure(0, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self.label = ctk.CTkLabel(master=self, text=TITLE, font=frame_font)
        self.label.cget("font").configure(size=18)
        self.label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        MAIN_FONT = ctk.CTkFont("monospace", size=16)
        UI_FONT = ctk.CTkFont("Noto Sans", size=15)

        self.title(TITLE)
        self.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        self.minsize(900, 600)
        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.topBar = TopBar(master=self, font=UI_FONT)
        self.topBar.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.mainFrame = MainFrame(master=self, font=MAIN_FONT)
        self.mainFrame.grid(row=1, column=0, sticky="nsew", columnspan=2)

if __name__ == '__main__':
    app = App()
    app.mainloop()
