import customtkinter as ctk
from ctk_markdown import CTkMarkdown

from editor import Editor


class MainFrame(ctk.CTkFrame):
    def __init__(self, master, **kwargs):
        frame_font: ctk.CTkFont = kwargs.pop("font", ctk.CTkFont("Arial", 15))
        preview_visible: bool = kwargs.pop("preview_visible", True)

        super().__init__(master, **kwargs)
        self.frame_font = frame_font
        self.preview_visible = preview_visible

        self.rowconfigure(0, weight=1)

        self.editors: dict[str, Editor] = {}

        self.grid_columnconfigure(0, weight=1, uniform="my_split")
        self.grid_columnconfigure(1, weight=1, uniform="my_split")

        self.tab_bar = ctk.CTkTabview(master=self, command=self.update_preview_on_tab_change)
        self.tab_bar.grid(row=0, column=0, sticky="nsew")
        self.add_tab("Untitled Note")


        # 1. Initialize the markdown widget with the dark theme settings
        self.preview_pane = CTkMarkdown(
            master=self,
            corner_radius=0,
            font=self.frame_font
        )

        # 2. Access the underlying textbox tags to force left justification and custom visibility
        self.preview_pane._textbox.tag_config("hr", justify="left")
        self.preview_pane._textbox.tag_config("hr", foreground="#555555") # Soft, visible grey for dark background
        self.preview_pane.grid(row=0, column=1, sticky="nsew", padx=(2, 0), pady=0)

        self.set_preview_visible(self.preview_visible)


    def update_preview_on_tab_change(self):
        current_tab = self.tab_bar.get()
        editor = self.editors[current_tab]
        raw_text = editor.get("1.0", "end-1c")
        self.preview_pane.set_markdown(raw_text)

    def update_preview(self, event):
        textbox: ctk.CTkTextbox = event.widget
        raw_text = textbox.get("1.0", "end-1c")
        self.preview_pane.set_markdown(raw_text)

    def set_preview_visible(self, toggle: bool):
        if toggle:
            self.tab_bar.grid(columnspan=1)
            self.preview_pane.grid(row=0, column=1, sticky="nsew", padx=(2, 0), pady=0)
            self.grid_columnconfigure(0, weight=1)
            self.grid_columnconfigure(1, weight=1)
        else:
            self.tab_bar.grid(columnspan=2)
            self.preview_pane.grid_remove()
            self.grid_columnconfigure(1, weight=0)

    def add_tab_with_content(self, name: str, content: str):
        self.add_tab(name)
        self.editors[name].delete("1.0", "end")
        self.editors[name].insert("1.0", content)
        self.preview_pane.set_markdown(content)

    def add_tab(self, name: str):
        self.tab_bar.add(name)
        self.tab_bar.set(name)

        tab = self.tab_bar.tab(name)
        tab.rowconfigure(0, weight=1)
        tab.columnconfigure(0, weight=1)

        editor = Editor(master=tab)
        editor.bind("<KeyRelease>", self.update_preview)
        editor.grid(row=0, column=0, sticky="nsew", pady=0)

        self.editors[name] = editor

