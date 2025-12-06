# Encoding: utf-8
# Module main: main
# Description: Main entry point for the Climact-ai application.

# Import - local:
import sys
import path

# Imports - third party:
from PySide6 import QtGui, QtCore, QtWidgets

# Imports - local:
from ui.main_window import MainWindow

# Application metadata
__NAME__ = "Climact-ai"
__VERSION__ = "0.1.0"
__AUTHORS__ = "EnERG Lab, IIT Madras"


# Main application class
class Climact(QtWidgets.QApplication):
    """
    The main application class for the Climact application.
    """

    def __init__(self, argv):
        super().__init__(argv)

        self.setApplicationName("Climact-ai")
        self.setApplicationVersion("0.1.0")
        self.setApplicationDisplayName("Climact-ai")
        self.setOrganizationName("EnERG Lab, IIT Madras")

        # Main window setup:
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
