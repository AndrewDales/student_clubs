""" Module contains constants and settings for the entire app"""

# tk_sql_app/settings
import os
import pathlib

# Constants
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SQL_PATH = f"sqlite:///{pathlib.Path(ROOT_DIR).joinpath('var', 'db.sqlite')}"