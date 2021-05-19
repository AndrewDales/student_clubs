""" Module contains unittests for the db classes and functions"""

# tk_sql_app/tests/__init__

import unittest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tk_sql_app import db
from tk_sql_app.db import models as m
from tk_sql_app.db.queries import create_person


class TestDbInteractions(unittest.TestCase):
    def setUp(self):
        # The test database is setup in directly in a "memory" location
        self.engine = create_engine('sqlite:///:memory:', echo=False)
        Session = sessionmaker(bind=self.engine)
        self.session = Session()
        m.Base.metadata.create_all(self.engine)
        # Create some participants (random names used)
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
        self.session.add_all(participants + activities)
        self.session.commit()

    def tearDown(self):
        # m.Base.meta.drop_all(self.engine)
        self.session.close()

    def test_qry_person_activities(self):
        person_data = db.queries.qry_person_activities(self.session, 5)
        self.assertDictEqual(person_data, {'name': 'Aiden Richards',
                                           'id': 5,
                                           'activities': ['Lower School Politics']})

    def test_qry_activities_register(self):
        activity_data = db.queries.qry_activities_register(self.session, 4)
        self.assertDictEqual(activity_data, {'activity': 'Boardgames',
                                             'id': 4,
                                             'attendees': ['Adrian Pearce', 'Dominique Peters']})

    def test_qry_names(self):
        names_data = db.queries.qry_names(self.session)
        for item in [(6, 'Joey Evans'),
                     (1, "Elyse O'Connor"), (3, 'Adrian Pearce'),
                     (2, 'Dominique Peters'), (4, 'Tristan Rees'),
                     (5, 'Aiden Richards'), (7, 'Dennis Thomson')]:
            self.assertIn(item, names_data)

    def test_qry_activities(self):
        activities_data = db.queries.qry_activities(self.session)
        self.assertEqual(activities_data, [(4, 'Boardgames'), (8, 'Classics Society'),
                                           (5, 'Lower School Politics'), (1, 'Masaryk Society'),
                                           (6, 'Mindfulness'), (7, 'Origami'),
                                           (3, 'Pride Society'), (2, 'Rap Group'),
                                           (9, 'VEX Robotics')])
