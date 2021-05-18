""" Module contains the application that will run the tkinter GUI """

# tk_sql_app/gui/tkinter_application

from tk_sql_app.cli.cli_application import CliApplication
from .forms import BaseWindow, MainMenu, SelectMenu


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
        self.root.show_frame(main_menu_frame)
        return main_menu_frame

    def open_select_person(self, next_menu_callback=None, **kwargs):
        menu = super().open_select_person(next_menu_callback, **kwargs)
        select_person_frame = SelectMenu(menu, parent=self.root)
        self.root.show_frame(select_person_frame)
        return select_person_frame

    def open_select_activity(self, next_menu_callback=None, **kwargs):
        print("Opening Select Activity")

    def open_person_menu(self, person_id=None, **kwargs):
        print("Opening Person Menu", person_id)
