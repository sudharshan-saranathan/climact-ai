# Encoding: utf-8
# Module main: main
# Description: Main entry point for the Climact-ai application.


# Import - standard libraries
import sys
from dataclasses import dataclass

# Imports - third party
from PySide6 import QtGui, QtCore, QtWidgets

# Imports - local
import path
from ui.main_window import MainWindow


class ClimactAttrs:
    """
    Class to hold application attributes.
    """

    NAME: str = "Climact-ai"
    VERSION: str = "0.1.0"
    AUTHORS: str = "EnERG Lab, IIT Madras"
    THEME: str = path.rpath("assets", "themes", "dark.qss")
    FONT: dict[str, QtGui.QFont] = {
        "windows": QtGui.QFont("Consolas", 12),
        "linux": QtGui.QFont("DejaVu Sans Mono", 12),
        "darwin": QtGui.QFont("Monaco", 10),
    }


# Main application class
class Climact(QtWidgets.QApplication):
    """
    The main application class for the Climact application.
    """

    def __init__(self, argv):
        super().__init__(argv)

        self.attrs = ClimactAttrs()

        # Set font
        os_platform = sys.platform.lower()
        self.setFont(
            self.attrs.FONT["windows"]
            if "win" in os_platform
            else (
                self.attrs.FONT["linux"]
                if "linux" in os_platform
                else self.attrs.FONT["darwin"]
            )
        )

        # Set theme:
        with open(self.attrs.THEME, "r") as theme_file:
            self.setStyleSheet(theme_file.read())

        # Load the startup dialog:
        from startup.startup_dialog import StartupDialog

        startup = StartupDialog()
        startup.exec()
        startup.deleteLater()  # Delete the startup to ensure transfer of focus

        # Main window setup
        self._ui = MainWindow()
        self._ui.show()


def main():
    """
    Main function to run the Climact application.
    """

    climact = Climact(sys.argv)
    climact.exec()
    sys.exit(0)


if __name__ == "__main__":
    main()
