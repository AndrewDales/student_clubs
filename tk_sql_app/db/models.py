""" Module sets up the database tables using SQLAlchemy"""

# tk_sql_app/db/models.py

from sqlalchemy import (
    Column, ForeignKey, ForeignKeyConstraint, Table, UniqueConstraint, event,
    Boolean, Date, Integer, Text, String, Unicode
)
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

# Sets up a link table with activity_id and person_id as foreign keys
# Base.metadata is a container object that keeps together many different features of the database
person_activity = Table('person_activity',
                        Base.metadata,
                        Column('id', Integer, primary_key=True),
                        Column('activity_id', ForeignKey('activity.id')),
                        Column('person_id', ForeignKey('person.id')),
                        UniqueConstraint('activity_id', 'person_id')
                        )


# Sets up an Activity table, this references "attendees" via the person_activities table
class Activity(Base):
    __tablename__ = 'activity'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, unique=True, nullable=False)
    attendees = relationship("Person",
                             secondary=person_activity,
                             back_populates="activities")

    # Gives a representation of an Activity (for printing out)
    def __repr__(self):
        return f"<Activity({self.name})>"


# Sets up a Person table, this references "activities" via the person_activities table
class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, autoincrement=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    activities = relationship("Activity",
                              secondary=person_activity,
                              back_populates="attendees")

    # Gives a representation of a Person (for printing out)
    def __repr__(self):
        return f"<Person({self.first_name} {self.last_name})>"
