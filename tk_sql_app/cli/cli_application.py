""" Command Line Interface main application"""
from contextlib import contextmanager
from functools import partial
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from tk_sql_app.settings import SQL_PATH
from tk_sql_app import cli
from tk_sql_app.db import queries


class CliApplication:
    def __init__(self, **kwargs):
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
        self.interface = kwargs.get("interface", None)
        self.display = kwargs.get("display", True)
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
        menu_options = {"option_list":
                        [("Select person", partial(self.callbacks["open_select_person"],
                                                   self.callbacks["open_person_menu"])),
                         ("Select activity", partial(self.callbacks["open_select_activity"],
                                                     self.callbacks["open_activity_menu"])),
                         ("Quit", None)]
                        }
        menu = {"title": title, "menu_options": menu_options}
        if self.interface == "cli":
            menu = self.create_cli_menu("main_menu", menu)
        return menu

    def open_select_person(self, person_callback=lambda i: None):
        # person_callback = person_callback or self.callbacks["open_person_menu"]
        with self.session_scope() as session:
            name_data = queries.qry_names(session)
        title = "Select Person"
        menu_options = dict(option_title="Select one of the following people",
                            option_list=[(name, partial(person_callback, name_id))
                                         for name_id, name in name_data])
        menu = {"title": title, "menu_options": menu_options, "data": {"ref_data": name_data}}
        if self.interface == "cli":
            menu = self.create_cli_menu("select_person", menu)
        return menu

    def open_select_activity(self, activity_callback=lambda i: None):
        with self.session_scope() as session:
            activity_data = queries.qry_activities(session)
        title = "Select Activity"
        menu_options = dict(option_title="Select one of the following activities",
                            option_list=[(activity, partial(activity_callback, activity_id))
                                         for activity_id, activity in activity_data])
        menu = {"title": title, "menu_options": menu_options, "data": {"ref_data": activity_data}}
        if self.interface == "cli":
            menu = self.create_cli_menu("select_person", menu)
        return menu

    def open_person_menu(self, id_num):
        with self.session_scope() as session:
            person_data = queries.qry_person_activities(session, id_num)
            if not person_data["activities"]:
                person_data["activities"] = ["No activities"]
        title = person_data["name"]

        data = {"data_title": "Activities", "data_list": person_data["activities"],
                "person_id": id_num}
        menu_options = dict(option_list=[("Add new activity",
                                          partial(self.callbacks["add_person_activity"],
                                                  person_id=id_num,
                                                  show_callback=partial(self.callbacks["open_person_menu"], id_num))),
                                         ("Select new person", self.callbacks["open_select_person"]),
                                         ("Return to main menu", self.callbacks["open_main_menu"])])
        menu = {"title": title, "data": data, "menu_options": menu_options}
        if self.interface == "cli":
            menu = self.create_cli_menu("person_activity_menu", menu)
        return menu

    def open_activity_menu(self, id_num):
        with self.session_scope() as session:
            activity_data = queries.qry_activities_register(session, id_num)
            if not activity_data["attendees"]:
                activity_data["attendees"] = ["No attendees"]
        title = activity_data["activity"]

        data = {"data_title": "Attendees", "data_list": activity_data["attendees"],
                "activity_id": id_num}
        menu_options = dict(option_list=[("Add new attendee",
                                          partial(self.callbacks["add_person_activity"],
                                                  activity_id=id_num,
                                                  show_callback=partial(self.callbacks["open_activity_menu"], id_num))),
                                         ("Select new activity", self.callbacks["open_select_activity"]),
                                         ("Return to main menu", self.callbacks["open_main_menu"])])
        menu = {"title": title, "data": data, "menu_options": menu_options}
        if self.interface == "cli":
            menu = self.create_cli_menu("activity_register_menu", menu)
        return menu

    def add_person_activity(self, person_id=None, activity_id=None, show_callback=None):
        if not activity_id:
            menu = self.callbacks["open_select_activity"]()
            option = menu.last_selected
            activity_id = menu.data["ref_data"][option][0]

        if not person_id:
            menu = self.callbacks["open_select_person"]()
            option = menu.last_selected
            person_id = menu.data["ref_data"][option][0]

        with self.session_scope() as session:
            queries.add_person_activity(session, person_id, activity_id)

        show_callback()
