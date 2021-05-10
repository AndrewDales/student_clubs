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
        self.test_app = CliApplication(echo=False, display=None)
        self.main_menu = self.test_app.open_main_menu()

    def test_main_menu(self):
        self.assertTrue(isinstance(self.main_menu, Menu), "main menu is not a menu type")
        self.assertTrue(self.main_menu.title, "Main Menu")
        self.assertEqual(str(self.main_menu),
                         '1 Select person\n2 Select activity\n3 Quit')
        # Check if the correct callback are run
        select_person_menu = self.main_menu.run_callback(0)
        select_activity_menu = self.main_menu.run_callback(1)
        self.assertEqual(select_person_menu, "You opened the select person option")
        self.assertEqual(select_activity_menu, "You opened the select activity option")

    def test_open_activity_menu(self):
        person_menu = self.test_app.open_person_menu(3)
        self.assertTrue(isinstance(person_menu, Menu), "main menu is not a menu type")
        self.assertEqual(person_menu.title, "Adrian Pearce")
        self.assertEqual(str(person_menu),
                         '1 Add new activity\n2 Select new person\n3 Return to main menu')
        self.assertEqual(person_menu.data,
                         {'data_title': 'Activities',
                          'data_list': ['Lower School Politics', 'Boardgames'],
                          'person_id': 3})
        menu_0 = person_menu.run_callback(0)
        menu_1 = person_menu.run_callback(1)
        menu_2 = person_menu.run_callback(2)
        self.assertEqual(menu_0, "You opened the select activity option")
        self.assertEqual(menu_1, "You opened the select person option")
        self.assertTrue(isinstance(menu_2, Menu))
        self.assertEqual(menu_2.title, "Main Menu")
