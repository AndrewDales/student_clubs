""" Module contains the application that will run the tkinter GUI """

# tk_sql_app/gui/tkinter_application

import tkinter as tk
from tk_sql_app.cli.cli_application import CliApplication
from .forms import BaseWindow, MainMenu


class TkApplication(CliApplication):
    def __init__(self, display, **kwargs):
        super().__init__(interface="gui", display=display, **kwargs)
        self.root = BaseWindow()
        if not display:
            self.root.withdraw()
        self.main_menu = self.open_main_menu()

    def open_main_menu(self):
        menu = super().open_main_menu()
        main_menu_frame = MainMenu(menu, parent=self.root)
        main_menu_frame.pack(fill=tk.X)
        return main_menu_frame

    def open_select_person(self, next_menu_callback=None, **kwargs):
        print("Opening Select Person")

    def open_select_activity(self, next_menu_callback=None, **kwargs):
        print("Opening Select Activity")
