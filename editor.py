import customtkinter as ctk


class Editor(ctk.CTkTextbox):
    def __init__(self, master, **kwargs):
        self.current_editor_font_size = 18
        self.editor_font : ctk.CTkFont = ctk.CTkFont(family="JetBrainsMono Nerd Font", size=self.current_editor_font_size)
        self.editor_font.configure(size=self.current_editor_font_size)

        super().__init__(master, corner_radius=0, border_spacing=10, font=self.editor_font, **kwargs)


        self.bind("<Control-a>", self.select_all)

        self.bind("<plus>", command=self.increase_editor_font_size)
        self.bind("<Control-plus>", command=self.increase_editor_font_size)

        self.bind("<minus>", command=self.decrease_editor_font_size)
        self.bind("<Control-minus>", command=self.decrease_editor_font_size)


    def increase_editor_font_size(self, event):
        textbox = event.widget
        self.current_editor_font_size += 2
        self.editor_font.configure(size=self.current_editor_font_size)
        textbox.update_idletasks()
        return "break"

    def decrease_editor_font_size(self, event):
        textbox = event.widget
        self.current_editor_font_size -= 2
        self.editor_font.configure(size=self.current_editor_font_size)
        textbox.update_idletasks()
        return "break"

    def select_all(self, event):
        textbox = event.widget
        textbox.tag_add("sel", "1.0", "end")
        return "break"

