""" Command Line Interface main application"""
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from tk_sql_app.settings import SQL_PATH
from tk_sql_app import cli
from tk_sql_app.db import queries


class MenuOption:
    def __init__(self, display, callback=None, callback_params=None):
        self.display = display
        self.callback = callback
        self.callback_params = callback_params or {}

    def execute_option(self):
        if self.callback:
            return self.callback(**self.callback_params)

    def __repr__(self):
        return self.display


class CliApplication:
    def __init__(self, interface=None, display=None, **kwargs):
        engine = create_engine(SQL_PATH, echo=kwargs.get("echo", True))
        self.Session = sessionmaker(bind=engine)
        self.callbacks = {
            'open_main_menu': self.open_main_menu,
            'open_person_menu': self.open_person_menu,
            'open_activity_menu': self.open_activity_menu,
            'open_select_person': self.open_select_person,
            'open_select_activity': self.open_select_activity,
            'add_person_activity': self.add_person_activity
        }
        self.interface = interface
        self.display = display
        self.menus = {}

    @contextmanager
    def session_scope(self):
        session = self.Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            print(e)
            session.rollback()
            raise
        finally:
            session.close()

    def create_cli_menu(self, menu_name, menu):
        menu = cli.menus.Menu(**menu)
        self.menus[menu_name] = menu
        if self.display:
            menu.display_menu()
        return menu

    def open_main_menu(self):
        title = "Main Menu"
        menu_options = {"option_title": "Select from the following options",
                        "option_list": [
                            MenuOption("Select person", self.callbacks["open_select_person"],
                                       {"next_menu_callback": self.callbacks["open_person_menu"]}),
                            MenuOption("Select activity", self.callbacks["open_select_activity"],
                                       {"next_menu_callback": self.callbacks["open_activity_menu"]}),
                            MenuOption("Quit", None)]}

        menu = {"title": title, "menu_options": menu_options}
        if self.interface == "cli":
            menu = self.create_cli_menu("main_menu", menu)
        return menu

    def open_select_person(self, next_menu_callback=None, **kwargs):
        callback = next_menu_callback

        with self.session_scope() as session:
            name_data = queries.qry_names(session)

        title = "Select Person"
        menu_options = {"option_title": "Select one of the following people",
                        "option_list": [MenuOption(name, callback, dict({"person_id": name_id}, **kwargs))
                                        for name_id, name in name_data]}
        menu = {"title": title, "menu_options": menu_options, "data": {"ref_data": name_data}}

        if self.interface == "cli":
            menu = self.create_cli_menu("select_person", menu)
        return menu

    def open_select_activity(self, next_menu_callback=None, **kwargs):
        callback = next_menu_callback

        with self.session_scope() as session:
            activity_data = queries.qry_activities(session)

        title = "Select Activity"
        menu_options = {"option_title": "Select one of the following activities",
                        "option_list": [MenuOption(activity, callback, dict({"activity_id": activity_id}, **kwargs))
                                        for activity_id, activity in activity_data]}
        menu = {"title": title, "menu_options": menu_options, "data": {"ref_data": activity_data}}
        if self.interface == "cli":
            menu = self.create_cli_menu("select_person", menu)
        return menu

    def open_person_menu(self, person_id=None, **kwargs):
        id_num = person_id
        with self.session_scope() as session:
            person_data = queries.qry_person_activities(session, id_num)
            if not person_data["activities"]:
                person_data["activities"] = ["No activities"]

        title = person_data["name"]
        data = {"data_title": "Activities", "data_list": person_data["activities"],
                "person_id": id_num}
        menu_options = dict(option_title="Select from the following options",
                            option_list=[MenuOption("Add new activity",
                                                    self.callbacks["add_person_activity"],
                                                    {"next_menu_callback": self.callbacks["open_person_menu"],
                                                     "person_id": id_num}),
                                         MenuOption("Select new person",
                                                    self.callbacks["open_select_person"],
                                                    {"next_menu_callback": self.callbacks["open_person_menu"]}),
                                         MenuOption("Return to main menu", self.callbacks["open_main_menu"])
                                         ])
        menu = {"title": title, "data": data, "menu_options": menu_options}
        if self.interface == "cli":
            menu = self.create_cli_menu("person_activity_menu", menu)
        return menu

    def open_activity_menu(self, activity_id=None, **kwargs):
        id_num = activity_id
        with self.session_scope() as session:
            activity_data = queries.qry_activities_register(session, id_num)
            if not activity_data["attendees"]:
                activity_data["attendees"] = ["No attendees"]
        title = activity_data["activity"]

        data = {"data_title": "Attendees", "data_list": activity_data["attendees"],
                "activity_id": id_num}
        menu_options = dict(option_title="Select from the following options",
                            option_list=[MenuOption("Add new attendee",
                                                    self.callbacks["add_person_activity"],
                                                    {"next_menu_callback": self.callbacks["open_activity_menu"],
                                                     "activity_id": id_num}),
                                         MenuOption("Select new activity",
                                                    self.callbacks["open_select_activity"],
                                                    {"next_menu_callback": self.callbacks["open_activity_menu"]}),
                                         MenuOption("Return to main menu",
                                                    self.callbacks["open_main_menu"])
                                         ])
        menu = {"title": title, "data": data, "menu_options": menu_options}
        if self.interface == "cli":
            menu = self.create_cli_menu("activity_register_menu", menu)
        return menu

    def add_person_activity(self, person_id=None, activity_id=None, next_menu_callback=None):
        if not activity_id:
            menu = self.callbacks["open_select_activity"]()
            option = menu.last_selected
            activity_id = menu.data["ref_data"][option][0]

        if not person_id:
            menu = self.callbacks["open_select_person"]()
            option = menu.last_selected
            person_id = menu.data["ref_data"][option][0]

        with self.session_scope() as session:
            try:
                queries.add_person_activity(session, person_id, activity_id)
            except IntegrityError:
                print("That person is already attending that activity")


        next_menu_callback(person_id=person_id, activity_id=activity_id)
