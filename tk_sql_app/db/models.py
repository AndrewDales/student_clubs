""" Module sets up the database tables using SQLAlchemy"""

# tk_sql_app/db/models.py

from sqlalchemy import (
    Column, ForeignKey, ForeignKeyConstraint, Table, UniqueConstraint, event,
    Boolean, Date, Integer, Text, String
)
from sqlalchemy.engine import Engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

person_activities = Table('person_activities',
                          Base.metadata,
                          Column('id', Integer, primary_key=True),
                          Column('activity_id', ForeignKey('activity.id')),
                          Column('person_id', ForeignKey('person.id'))
                          )
person_activities.__table_args__ = UniqueConstraint('name', 'vehiclemodel_id')


class Activity(Base):
    __tablename__ = 'activity'
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    attendees = relationship("Person",
                             secondary=person_activities,
                             back_populates="activities")

    def __repr__(self):
        return f"<Activity({self.name})>"


class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True)
    first_name = Column(String, nullable=False)
    second_name = Column(String, nullable=False)
    activities = relationship("Activity",
                              secondary=person_activities,
                              back_populates="attendees")

    def __repr__(self):
        return f"<Person({self.firt_name} {self.second_name})>"


