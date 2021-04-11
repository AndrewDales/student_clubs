""" Module contains unittests for the db classes and functions"""

# tk_sql_app/tests/__init__

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tk_sql_app import db
from tk_sql_app.db import models as m
from tk_sql_app.db.forms import *
