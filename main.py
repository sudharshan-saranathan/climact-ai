# Encoding: utf-8
# Module name: main
# Description: The entry point for the Climact application

# Global variable(s):
__author__      = 'Sudharshan Saranathan'
__version__     = '1.0'
__license__     = 'N/A'

# --------------
# Module imports
# --------------
# Standard:
import os
import sys

# PySide6:
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QApplication, QMainWindow

# Climact submodule(s):
from gui.gui import MainGui
from opts    import GlobalConfig

# Main application class:
def main():
    """
    Run the Climact application.
    :return:
    """

    app = Climact()     # Instantiate the application
    app.exec()          # Enter event-loop

    sys.exit(None)      # Exit to OS

# Main method:
class Climact(QApplication):

    # Default constructor:
    def __init__(self):

        # Base-class initialization:
        super().__init__()

        # Set class-level attribute(s)
        self.setApplicationName(GlobalConfig['name'])
        self.setStyleSheet(self.parse_qss(GlobalConfig['qss']))
        self.setWindowIcon(QIcon(GlobalConfig['logo']))
        self.setFont(GlobalConfig['font'])

        # Instantiate window:
        self._window = MainGui()

    # Parse style-sheet:
    @staticmethod
    def parse_qss(qss):     return open(qss, 'r').read() if os.access(qss, os.R_OK) else str()

# Invoke main():
if  __name__ == '__main__': main()