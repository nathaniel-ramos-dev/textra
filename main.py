import customtkinter as ctk

class PreviewFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Notes App")
        self.geometry("800x600")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.editor = ctk.CTkTextbox(master=self, width=400, height=600, corner_radius=0, border_spacing=10, font=ctk.CTkFont(family="JetBrainsMono Nerd Font", size=15))
        self.editor.grid(row=0, column=0, sticky="nsw")

        self.preview = PreviewFrame(master=self, width=400, height=600)
        self.preview.grid(row=0, column=1, sticky="nse")

if __name__ == '__main__':
    app = App()
    app.mainloop()
