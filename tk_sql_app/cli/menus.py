""" Contains classes for CLI Menus"""


class Menu:
    def __init__(self):
        self.title = None
        self.data = None
        self.menu_options = None

    def show_title(self):
        print("\n" + self.title)
        print("_" * len(self.title) + "\n")

    def show_options(self):
        print('Select from the following options:\n')
        for i, option in enumerate(self.menu_options, 1):
            print(f'\t{i}\t{option}')
        option = int(input('\nChoose option number: '))
        callback = list(self.menu_options.values())[option-1]
        if callback:
            callback()

    def show_data(self):
        print(self.data['data_title'])
        for item in self.data['data_list']:
            print(f'\t{item}')
        print()

    def display_menu(self):
        if self.title:
            self.show_title()
        if self.data:
            self.show_data()
        if self.menu_options:
            self.show_options()


class MainMenu(Menu):
    def __init__(self, callbacks):
        super().__init__()
        self.title = "Main Menu"
        # Add self.menu_options


