""" Module contains unittests for the cli_application"""

# tk_sql_app/tests/test_cli_application

# import unittest

from .test_db import TestDbInteractions

from tk_sql_app.cli.cli_application import CliApplication
from tk_sql_app.cli.menus import Menu


# Subclass TestDBInteractions in order to use the sample database
class TestCliApplication(TestDbInteractions):
    def setUp(self):
        super().setUp()
        self.test_app = CliApplication(echo=False, interface="cli", display=None)
        self.main_menu = self.test_app.open_main_menu()

    def test_main_menu(self):
        self.assertTrue(isinstance(self.main_menu, Menu), "main menu is not a menu type")
        self.assertEqual(str(self.main_menu),
                         '1 Select person\n2 Select activity\n3 Quit')
        # Check if the correct callback are run
        select_person_menu = self.main_menu.run_callback(0)
        self.assertEqual(select_person_menu.title, "Select Person")
        select_activity_menu = self.main_menu.run_callback(1)
        self.assertEqual(select_activity_menu.title, "Select Activity")

    def test_person_menu(self):
        person_activities = self.test_app.callbacks["open_person_menu"](3)
        self.assertEqual(person_activities.title, "Adrian Pearce")
        self.assertEqual(str(person_activities),
                         '1 Add new activity\n2 Select new person\n3 Return to main menu')
        self.assertDictEqual(person_activities.data,
                             {'data_title': 'Activities', 'data_list': ['Lower School Politics', 'Boardgames'],
                              'person_id': 3})

    def test_activity_menu(self):
        activity_attendees = self.test_app.callbacks["open_activity_menu"](3)
        self.assertEqual(activity_attendees.title, "Pride Society")
        self.assertEqual(str(activity_attendees),
                         '1 Add new attendee\n2 Select new activity\n3 Return to main menu')
        self.assertDictEqual(activity_attendees.data,
                             {'data_title': 'Attendees', 'data_list': ["Elyse O'Connor", 'Ronald McDonald'],
                              'activity_id': 3})
