""" Database Queries"""

# tk_sql_app/db/queries

from tk_sql_app.db import models as m


# Create a person in the database by splitting first name and last name
def create_person(name, last_name=None):
    if last_name is None:
        name, last_name = name.split(' ')
    return m.Person(first_name=name, last_name=last_name)


# Query all the persons in the database
def qry_names(session):
    qry = session.query(m.Person).order_by(m.Person.last_name, m.Person.first_name)
    return [(row.id, f'{row.first_name} {row.last_name}') for row in qry.all()]


# Query all the activities in the database
def qry_activities(session):
    pass


# Query the activities of a given person
def qry_person_activities(session, id_num):
    person = session.query(m.Person).get(id_num)
    return {"name": f"{person.first_name} {person.last_name}", "id": id_num,
            "activities": [act.name for act in person.activities]}


# Query the activities of a given person
def qry_activities_register(session, id_num):
    pass
