""" File to start-up the database in a console for testing purposes """

# tk_sql_app/console/startup.py
import pathlib

from tk_sql_app import db
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from tk_sql_app.settings import ROOT_DIR
import tk_sql_app.db.models as m
from tk_sql_app.db import queries
from tk_sql_app.cli.cli_application import CliApplication
from tk_sql_app.cli.menus import Menu
from tk_sql_app.gui.tkinter_application import TkApplication

sql_path = pathlib.Path(ROOT_DIR).joinpath('var', 'db.sqlite')
engine = create_engine(f'sqlite:///{pathlib.Path(sql_path)}', echo=True)
Session = sessionmaker(bind=engine)

# test_app = CliApplication(echo=False, interface="cli", display=None)
# main_menu = test_app.open_main_menu()

test_gui = TkApplication(display=False, echo=False)