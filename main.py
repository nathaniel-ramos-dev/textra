import customtkinter as ctk
from ctk_markdown import CTkMarkdown

WIN_WIDTH = 1000
WIN_HEIGHT = 700

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Notes App")
        self.geometry(f"{WIN_WIDTH}x{WIN_HEIGHT}")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)


        self.editor = ctk.CTkTextbox(master=self, width=int(WIN_WIDTH/2), height=int(WIN_HEIGHT), corner_radius=0, border_spacing=10, font=ctk.CTkFont(family="JetBrainsMono Nerd Font", size=15))
        self.editor.grid(row=0, column=0, sticky="nsw")

        # 1. Initialize the markdown widget with the dark theme settings
        self.preview_pane = CTkMarkdown(self, width=int(WIN_WIDTH)/2, height=int(WIN_HEIGHT), bg_color="#000000", text_color="#ffffff")

        # 2. Access the underlying textbox tags to force left justification and custom visibility
        self.preview_pane._textbox.tag_config("hr", justify="left")
        self.preview_pane._textbox.tag_config("hr", foreground="#555555") # Soft, visible grey for dark background

        self.preview_pane.grid(row=0, column=1, sticky="nse")

        self.editor.bind("<KeyRelease>", self.update_preview)

    def update_preview(self, event):
        raw_text = self.editor.get("1.0", "end-1c")
        self.preview_pane.set_markdown(raw_text)

        # Re-apply the formatting every time the Markdown renderer refreshes the text content
        self.preview_pane._textbox.tag_config("hr", justify="left")
        self.preview_pane._textbox.tag_config("hr", foreground="#ffffff") # Pure bright white


if __name__ == '__main__':
    app = App()
    app.mainloop()
