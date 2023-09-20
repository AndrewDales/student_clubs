import pytest

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from tk_sql_app import db
from tk_sql_app.db import models as m
from tk_sql_app.db.queries import create_person

# Creates a temporary test database in memory (RAM)
engine = create_engine('sqlite:///:memory:')


@pytest.fixture
def session():
    Session = sessionmaker(bind=engine)
    db_session = Session()
    yield db_session
    db_session.rollback()
    db_session.close()


@pytest.fixture(autouse=True)
def setup_db(session, request):
    def teardown():
        m.Base.metadata.drop_all(engine)

    m.Base.metadata.create_all(engine)

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
    session.add_all(participants + activities)
    session.commit()

    request.addfinalizer(teardown)


# @pytest.mark.usefixtures("setup_db")
class TestSetup:
    def test_query_people(self, session):
        people = session.query(m.Person).all()
        assert len(people) == 7
        assert people[0].first_name == "Elyse"
        assert people[0].last_name == "O'Connor"

    def test_qry_person_activities(self, session):
        person_data = db.queries.qry_person_activities(session, 5)
        assert person_data == {'name': 'Aiden Richards',
                               'id': 5,
                               'activities': ['Lower School Politics'],
                               }

    def test_qry_activities_register(self, session):
        activity_data = db.queries.qry_activities_register(session, 4)
        assert activity_data == {'activity': 'Boardgames',
                                 'id': 4,
                                 'attendees': ['Adrian Pearce', 'Dominique Peters'],
                                 }

    def test_qry_names(self, session):
        names_data = db.queries.qry_names(session)
        assert names_data == [(6, 'Joey Evans'),
                              (1, "Elyse O'Connor"),
                              (3, 'Adrian Pearce'),
                              (2, 'Dominique Peters'),
                              (4, 'Tristan Rees'),
                              (5, 'Aiden Richards'),
                              (7, 'Dennis Thomson'),
                              ]

    def test_qry_activities(self, session):
        activities_data = db.queries.qry_activities(session)
        assert activities_data == [(4, 'Boardgames'),
                                   (8, 'Classics Society'),
                                   (5, 'Lower School Politics'),
                                   (1, 'Masaryk Society'),
                                   (6, 'Mindfulness'), (7, 'Origami'),
                                   (3, 'Pride Society'), (2, 'Rap Group'),
                                   (9, 'VEX Robotics'),
                                   ]
