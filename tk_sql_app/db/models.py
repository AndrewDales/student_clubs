""" Module sets up the database tables using SQLAlchemy"""

# tk_sql_app/db/models.py

from sqlalchemy import (
    Column, ForeignKey, ForeignKeyConstraint, Table, UniqueConstraint, event,
    Boolean, Date, Integer, Text, String
)
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship




