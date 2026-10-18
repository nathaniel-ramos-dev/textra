import customtkinter as ctk
from ctk_markdown import CTkMarkdown

WIN_WIDTH = 1000
WIN_HEIGHT = 700
TITLE = "My Notes App"


class TopBar(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        frame_font: ctk.CTkFont = kwargs.pop("font", ctk.CTkFont("Arial", 15))

        super().__init__(master, **kwargs)

        self.label = ctk.CTkLabel(master=self, text=TITLE, font=frame_font)
        self.label.cget("font").configure(size=18)
        self.label.grid(row=0, column=0, padx=20)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        MAIN_FONT = ctk.CTkFont("JetBrainsMono Nerd Font", size=15)
        UI_FONT = ctk.CTkFont("Noto Sans", size=15)

        self.title("Notes App")
        self.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        self.minsize(900, 600)
        self.grid_rowconfigure(1, weight=1)

        self.topBar = TopBar(master=self, font=UI_FONT)
        self.topBar.grid(row=0, column=0, sticky="nsew", columnspan=2)

        self.grid_columnconfigure(0, weight=1, uniform="my_split")
        self.grid_columnconfigure(1, weight=1, uniform="my_split")


        self.editor = ctk.CTkTextbox(
            master=self,
            corner_radius=0,
            border_spacing=10,
            font=MAIN_FONT
        )

        self.editor.bind("<Control-a>", self.select_all)

        self.editor.grid(row=1, column=0, sticky="nsew", padx=(0, 2), pady=0)

        # 1. Initialize the markdown widget with the dark theme settings
        self.preview_pane = CTkMarkdown(
            master=self,
            bg_color="#000000",
            text_color="#ffffff"
        )
        # 2. Access the underlying textbox tags to force left justification and custom visibility
        self.preview_pane._textbox.tag_config("hr", justify="left")
        self.preview_pane._textbox.tag_config("hr", foreground="#555555") # Soft, visible grey for dark background

        self.preview_pane.grid(row=1, column=1, sticky="nsew", padx=(2, 0), pady=0)

        self.editor.bind("<KeyRelease>", self.update_preview)

    def select_all(self, event):
        textbox = event.widget
        textbox.tag_add("sel", "1.0", "end")
        return "break"

    def update_preview(self, event):
        raw_text = self.editor.get("1.0", "end-1c")
        self.preview_pane.set_markdown(raw_text)

        # Re-apply the formatting every time the Markdown renderer refreshes the text content
        self.preview_pane._textbox.tag_config("hr", justify="left")
        self.preview_pane._textbox.tag_config("hr", foreground="#ffffff") # Pure bright white


if __name__ == '__main__':
    app = App()
    app.mainloop()
