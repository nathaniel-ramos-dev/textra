# type: ignore
from collections.abc import Callable
import os

import customtkinter as ctk

from main_content import MainFrame

WIN_WIDTH = 1000
WIN_HEIGHT = 700
TITLE = "My Notes App"

class OpenDialog(ctk.CTkToplevel):
    def __init__(self, master, main_frame, **kwargs):
        super().__init__(master, **kwargs)

        self.main_frame = main_frame

        self.title("Open File")
        self.geometry("400x400")

        self.widgets = []
        self.current_dir = os.getcwd()

        self.item_font = ctk.CTkFont(family="Noto Sans", size=15)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        self.current_dir_var = ctk.StringVar(value=self.current_dir)

        self.address_bar = ctk.CTkEntry(
            master=self, 
            corner_radius=0,
            font=self.item_font,
            textvariable=self.current_dir_var,
        )
        self.address_bar.grid(row=0, column=0, sticky="ew")
        self.address_bar.bind("<Enter>", self.update_list)

        self.list_frame = ctk.CTkScrollableFrame(
            master=self,
            corner_radius=0
        )
        self.list_frame.grid(
            row=1, column=0, sticky="nsew",
            padx=0, pady=0
        )

        self.build_list(self.current_dir)

    def update_list(self, event):
        dir = self.current_dir_var.get()
        self.current_dir = dir
        self.current_dir_var.set(self.current_dir)
        self.build_list(self.current_dir)

    def build_list(self, dir):
        for widget in self.widgets:
            widget.destroy()

        self.widgets = []

        try:

            list_items = os.listdir(dir)
            parent = os.path.dirname(dir)

            back_btn = ctk.CTkButton(
                self.list_frame,
                text="..",
                fg_color="transparent",
                text_color=("black", "white"),
                hover_color=("#dbdbdb", "#2b2b2b"),
                anchor="w",
                font=self.item_font,
                command=lambda x=parent: self.on_item_click(x)
            )
            back_btn.pack(fill="x", padx=5, pady=2)
            self.widgets.append(back_btn)

            for item in list_items:
                item_dir = os.path.join(dir, item)
                if os.path.isdir(item_dir) and not item.startswith('.') or os.path.isfile(item_dir) and item.endswith('.md'):
                    btn = ctk.CTkButton(
                        self.list_frame,
                        text=item,
                        fg_color="transparent",
                        text_color=("black", "white"),
                        hover_color=("#dbdbdb", "#2b2b2b"),
                        font=self.item_font,
                        anchor="w",
                        command=lambda x=item_dir: self.on_item_click(x)
                    )
                    btn.pack(fill="x", padx=5, pady=2)
                    self.widgets.append(btn)

            self.list_frame.update_idletasks()

        except PermissionError as e:
            print(e)
            label = ctk.CTkLabel(
                master=self.list_frame,
                text="Access Denied",
                font=ctk.CTkFont(family="Noto Sans", size=20)
            )
            label.pack(fill="x", padx=5, pady=2)
            self.widgets.append(label)
        except FileNotFoundError as e:
            print(e)
            label = ctk.CTkLabel(
                master=self.list_frame,
                text="Access Denied",
                font=ctk.CTkFont(family="Noto Sans", size=20)
            )
            label.pack(fill="x", padx=5, pady=2)
            self.widgets.append(label)

    def open_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            file_content = f.read()

            self.main_frame.add_tab_with_content(os.path.basename(file_path), file_content)

            self.destroy()

    def on_item_click(self, item_name):
        if os.path.isfile(item_name):
            self.open_file(item_name)
        elif os.path.isdir(item_name):
            self.current_dir = item_name
            self.current_dir_var.set(self.current_dir)
            self.build_list(self.current_dir)


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

        self.open_dialog_window = None

        self.bind("<Control-n>", lambda event: self.new_note())
        self.bind("<Control-o>", lambda event: self.open_note())
        self.bind("<Control-s>", lambda event: self.save_note())
        self.bind("<Control-Shift-S>", lambda event: self.save_note_as())

    def open_note(self):
        if self.open_dialog_window is None or not self.open_dialog_window.winfo_exists():
            self.open_dialog_window = OpenDialog(self, self.mainFrame)
        else:
            self.open_dialog_window.focus()

    def new_note(self):
        self.mainFrame.add_tab("New Note")
        tab = self.mainFrame.tab_bar.get()

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
    ctk.set_default_color_theme("./themes/coffee.json")
    app = App()
    app.mainloop()
