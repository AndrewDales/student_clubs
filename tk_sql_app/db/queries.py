""" Database Queries"""

# tk_sql_app/db/queries

from tk_sql_app.db import models as m


def create_person(name, last_name=None):
    if last_name is None:
        name, last_name = name.split(' ')
    return m.Person(first_name=name, last_name=last_name)
