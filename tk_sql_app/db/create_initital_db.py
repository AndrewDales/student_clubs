""" Code to create the initial database and populate with some test data"""

# tk_sql_app/db/create_initial_db.py

import os
import pathlib

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from tk_sql_app.db import models as m
from tk_sql_app.settings import ROOT_DIR
from tk_sql_app.db.queries import create_person


def create_new_db():
    print("Deleting current database and starting new")

    sql_path = pathlib.Path(ROOT_DIR).joinpath('var', 'db.sqlite')
    if os.path.exists(sql_path):
        os.remove(sql_path)

    engine = create_engine(f'sqlite:///{pathlib.Path(sql_path)}', echo=True)
    m.Base.metadata.create_all(engine)

    return sessionmaker(bind=engine)


def populate_database(sess):
    # Create some participants (random names used
    participants = [create_person("Elyse O'Connor"),
                    create_person("Dominique Peters"),
                    create_person("Joey Evans"),
                    create_person("Dennis Thomson"),
                    create_person("Tristan Rees"),
                    create_person("Adrian Pearce"),
                    create_person("Aiden Richards")
                    ]

    # Create some activities
    activities = [m.Activity(name="Classics Society"),
                  m.Activity(name="Rap Group"),
                  m.Activity(name="Lower School Politics"),
                  m.Activity(name="Masaryk Society"),
                  m.Activity(name="Origami"),
                  m.Activity(name="Pride Society"),
                  m.Activity(name="Boardgames"),
                  m.Activity(name="Mindfulness"),
                  m.Activity(name="VEX Robotics")]

    # Assign activities to participants
    person_activities = {0: [3, 1, 5],
                         1: [6, 2],
                         2: [],
                         3: [0, 8],
                         4: [7, 2, 4],
                         5: [6, 2],
                         6: [2]}

    for person_key, activity_list in person_activities.items():
        for activity in activity_list:
            participants[person_key].activities.append(activities[activity])

    # Add changes to the database and commit
    sess.add_all(participants + activities)
    sess.commit()


if __name__ == "__main__":
    Session = create_new_db()
    with Session() as session:
        populate_database(session)
    # session.close()
