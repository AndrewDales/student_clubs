""" Contains classes for CLI Menus"""
from pyinputplus import inputInt


class Menu:
    def __init__(self, title=None, data=None, menu_options=None):
        self.title = title
        self.data = data
        self.menu_options = menu_options
        self.last_selected = None

    def show_title(self):
        print("\n" + self.title)
        print("_" * len(self.title) + "\n")

    def show_options(self):
        option_title = self.menu_options.get("option_title", "Select from the following options:")
        print(f'{option_title}\n')
        for i, option in enumerate(self.menu_options["option_list"], 1):
            print(f'\t{i}\t{option[0]}')

    def select_option(self):
        option = inputInt(f'\nChoose option number: ', min=1, max=len(self.menu_options["option_list"]) + 1)
        self.last_selected = option - 1
        return option - 1

    def run_callback(self, cb_number):
        callback = self.menu_options["option_list"][cb_number][1]
        if callback:
            return callback()

    def show_data(self):
        print(self.data['data_title'])
        for item in self.data['data_list']:
            print(f'\t{item}')
        print()

    def display_menu(self):
        if self.title:
            self.show_title()
        if self.data and "data_list" in self.data:
            self.show_data()
        if self.menu_options:
            self.show_options()
            call_back_option = self.select_option()
            self.run_callback(call_back_option)

    def __repr__(self):
        return "\n".join([f"{i} {option[0]}" for i, option in enumerate(self.menu_options["option_list"], 1)])
