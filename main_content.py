import customtkinter as ctk
from ctk_markdown import CTkMarkdown

EDITOR_FONT_SIZE = 18

class MainFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        frame_font: ctk.CTkFont = kwargs.pop("font", ctk.CTkFont("Arial", 15))
        preview_visible: bool = kwargs.pop("preview_visible", True)

        super().__init__(master, **kwargs)

        self.preview_visible = preview_visible

        self.rowconfigure(0, weight=1)

        self.editor: ctk.CTkTextbox = ctk.CTkTextbox(
            master=self,
            corner_radius=0,
            border_spacing=10,
            font=frame_font
        )

        self.editor.bind("<Control-a>", self.select_all)

        self.editor.grid(row=0, column=0, sticky="nsew", pady=0)

        # 1. Initialize the markdown widget with the dark theme settings
        self.preview_pane = CTkMarkdown(
            master=self,
            bg_color="#000000",
            text_color="#ffffff",
            corner_radius=0,
            font=frame_font
        )

        # 2. Access the underlying textbox tags to force left justification and custom visibility
        self.preview_pane._textbox.tag_config("hr", justify="left")
        self.preview_pane._textbox.tag_config("hr", foreground="#555555") # Soft, visible grey for dark background


        self.set_preview_visible(self.preview_visible)

        self.editor.bind("<KeyRelease>", self.update_preview)

    def increase_font_size(self, event):
        textbox: ctk.CTkTextbox = event.widget
        textbox.cget("font").configure(size=)


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

    def set_preview_visible(self, toggle: bool):
        if toggle:
            self.editor.grid_configure(columnspan=1)
            self.preview_pane.grid(row=0, column=1, sticky="nsew", padx=(2, 0), pady=0)
            self.grid_columnconfigure(0, weight=1, uniform="my_split")
            self.grid_columnconfigure(1, weight=1, uniform="my_split")
        else:
            self.editor.grid_configure(columnspan=2)
            self.preview_pane.grid_remove()
            self.grid_columnconfigure(0, weight=1, uniform="my_split")
            self.grid_columnconfigure(1, weight=0, uniform="my_split")
