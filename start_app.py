""" Launching point for cli or TKinter applications """
from tk_sql_app.cli.cli_application import CliApplication
from tk_sql_app.gui.tkinter_application import TkApplication

interface = "gui"
display = True

if interface == "cli":
    cli_app = CliApplication(echo=False, interface="cli", display=True)
    cli_app.open_main_menu()
elif interface == "gui":
    tk_app = TkApplication(display=display, echo=False)
    tk_app.root.mainloop()