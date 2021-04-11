""" Code to create the initial database"""

# tk_sql_app/db/create_initial_db.py

import os
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tk_sql_app.db import models as m
from tk_sql_app.settings import ROOT_DIR

print("Deleting current database and starting new")

sql_path = pathlib.Path(ROOT_DIR).joinpath('var', 'db.sqlite')
if os.path.exists(sql_path):
    os.remove(sql_path)

engine = create_engine(f'sqlite:///{pathlib.Path(sql_path)}', echo=True)
m.Base.metadata.create_all(engine)