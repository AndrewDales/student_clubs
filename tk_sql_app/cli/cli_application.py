""" Command Line Interface main application"""
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from tk_sql_app.settings import SQL_PATH
from tk_sql_app import cli
from tk_sql_app.db import queries


class CliApplication:
    def __init__(self, *args, **kwargs):
        engine = create_engine(SQL_PATH, echo=kwargs.get("echo", True))
        self.Session = sessionmaker(bind=engine)
        self.callbacks = {
            'open_main_menu': self.open_main_menu,
            'open_person_menu': self.open_person_menu,
            'open_activity_menu': self.open_activity_menu,
            'open_select_person': self.open_select_person,
            'open_select_activity': self.open_select_activity
        }
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
                        [("Select person", self.callbacks["open_select_person"]),
                         ("Select activity", self.callbacks["open_select_activity"]),
                         ("Quit", None)]
                        }
        menu = {"title": title, "menu_options": menu_options}
        menu = self.create_cli_menu("main_menu", menu)
        return menu

    def open_select_person(self):
        print("Running open_select_person ... ")
        return "You opened the select person option"

    def open_person_menu(self, id_num):
        with self.session_scope() as session:
            person_data = queries.qry_person_activities(session, id_num)
        title = person_data["name"]

        data = {"data_title": "Activities", "data_list": person_data["activities"],
                "person_id": id_num}
        menu_options = dict(option_list=[("Add new activity", self.callbacks["open_select_activity"]),
                                         ("Select new person", self.callbacks["open_select_person"]),
                                         ("Return to main menu", self.callbacks["open_main_menu"])])
        menu = {"title": title, "data": data, "menu_options": menu_options}
        menu = self.create_cli_menu("person_activity_menu", menu)
        return menu

    def open_select_activity(self):
        print("Running open_select_activity ... ")
        return "You opened the select activity option"

    def open_activity_menu(self, id_num):
        pass
