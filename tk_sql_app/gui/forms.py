""" Module to contain the tkinter code for the forms"""

# tk_sql_app/gui/forms
from tkinter import ttk
import tkinter as tk


class BaseWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Clubs Application")
        self.resizable(False, False)

        # creating a header
        header_frame = tk.Frame(self)
        header_frame.pack()

        # Create an overall title and pack it into the top of the container
        title_label = tk.Label(header_frame,
                               text="Student Clubs Database Application",
                               bg="blue", fg="white",
                               width=30,
                               font=("Arial", 20))
        title_label.pack()

        # Initialise frames to an empty dictionary
        self.frames = {}

    # Method to show the desired game class, which is a subclass of tk.Frame
    def show_frame(self, current_frame):
        for frame in self.frames.values():
            frame.pack_forget()
        self.frames[current_frame].pack(fill=tk.X)


class MainMenu(tk.Frame):
    def __init__(self, menu_data, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.title_label = ttk.Label(self, text=menu_data["title"], font=("Arial", 12))
        self.selection_buttons = []
        for item in menu_data["menu_options"]["option_list"]:
            self.selection_buttons.append(
                tk.Button(self, text=item.display, command=item.execute_option)
            )

        self.grid_columnconfigure(0, weight=1)

        self.title_label.grid(row=0, column=0, pady=5)
        for i, btn in enumerate(self.selection_buttons, 1):
            btn.grid(row=i, column=0, pady=(0, 5))
