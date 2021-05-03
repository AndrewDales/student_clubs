""" Command Line Interface main application"""
from contextlib import contextmanager
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from tk_sql_app.settings import SQL_PATH
from tk_sql_app import cli
from tk_sql_app.db import queries, models


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
        # self.menus = {'main_menu': None,
        #                'select_person': None,
        #                'person_activity_menu': None}
        self.menus = {}

        # Start main menu
        # self.open_main_menu()

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

    def open_main_menu(self):
        self.menus["main_menu"] = cli.menus.MainMenu(self.callbacks)
        self.menus["main_menu"].display_menu()

    def open_person_menu(self, id_num):
        with self.session_scope() as session:
            person_data = queries.qry_person_activities(session, id_num)
        self.menus["person_activity_menu"] = cli.menus.PersonActivityMenu(self.callbacks, person_data)
        self.menus["person_activity_menu"].display_menu()

    def open_select_person(self):
        with self.session_scope() as session:
            name_data = queries.qry_names(session)
        self.menus["select_person"] = cli.menus.SelectPersonMenu(self.callbacks, name_data)
        self.menus["select_person"].display_menu()

    def open_select_activity(self):
        with self.session_scope() as session:
            activity_data = queries.qry_activities(session)
        self.menus["select_activity"] = cli.menus.SelectActivityMenu(self.callbacks, activity_data)
        self.menus["select_activity"].display_menu()

    def open_activity_menu(self, id_num):
        with self.session_scope() as session:
            activity_data = queries.qry_activities_register(session, id_num)
        self.menus["activity_register_menu"] = cli.menus.ActivityRegisterMenu(self.callbacks, activity_data)
        self.menus["activity_register_menu"].display_menu()
