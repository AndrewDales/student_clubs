""" Contains classes for CLI Menus"""
from pyinputplus import inputInt


class Menu:
    def __init__(self, title=None, data=None, menu_options=None):
        self.title = title
        self.data = data
        self.menu_options = menu_options

    def show_title(self):
        print("\n" + self.title)
        print("_" * len(self.title) + "\n")

    def show_options(self):
        print('Select from the following options:\n')
        for i, option in enumerate(self.menu_options["option_list"], 1):
            print(f'\t{i}\t{option[0]}')

    def select_option(self):
        option = inputInt('\nChoose option number: ', min=1, max=len(self.menu_options["option_list"]) + 1)
        callback = self.menu_options["option_list"][option-1][1]
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
            self.select_option()

