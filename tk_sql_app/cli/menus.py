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
        self.menu_options = {"Select person": callbacks["open_select_person"],
                             "Select activity": callbacks["open_select_activity"],
                             "Quit": None}


class SelectPersonMenu(Menu):
    def __init__(self, callbacks, data):
        super().__init__()
        self.person_data = data
        person_callback = callbacks['open_person_menu']
        self.title = "Select Person"
        self.menu_options = {name: lambda i=name_id: person_callback(i)
                             for name_id, name in data.items()}


class SelectActivityMenu(Menu):
    def __init__(self, callbacks, data):
        super().__init__()
        self.activity_data = data
        activity_callback = callbacks['open_activity_menu']
        self.title = "Select Activity"
        self.menu_options = {activity: lambda i=activity_id: activity_callback(i)
                             for activity_id, activity in data.items()}


class PersonActivityMenu(Menu):
    def __init__(self, callbacks, data):
        super().__init__()
        self.title = data["name"]
        self.data = {'data_title': 'Activities', 'data_list': data["activities"]}
        self.menu_options = {"Select new person": callbacks["open_select_person"],
                             "Return to main menu": callbacks["open_main_menu"]}


class ActivityRegisterMenu(Menu):
    def __init__(self, callbacks, data):
        super().__init__()
        self.title = data["activity"]
        self.data = {'data_title': 'Attendees', 'data_list': data["names"]}
        self.menu_options = {"Select new activity": callbacks["open_select_activity"],
                             "Return to main menu": callbacks["open_main_menu"]}
