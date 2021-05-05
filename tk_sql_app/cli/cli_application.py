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

    def open_main_menu(self):
        self.menus["main_menu"] = cli.menus.MainMenu(self.callbacks)
        self.menus["main_menu"].display_menu()

    def open_select_person(self):
        with self.session_scope() as session:
            name_data = queries.qry_names(session)
        pass

    def open_person_menu(self, id_num):
        pass

    def open_select_activity(self):
        pass

    def open_activity_menu(self, id_num):
        pass
