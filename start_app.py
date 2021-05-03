""" Launching point for cli or TKinter applications """
from tk_sql_app.cli.cli_application import CliApplication

cli_app = CliApplication(echo=False)
cli_app.open_main_menu()