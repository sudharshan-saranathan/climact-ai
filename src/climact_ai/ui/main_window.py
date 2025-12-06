# Encoding: utf-8
# Module name: main_window
# Description: Main window UI for the Climact-ai application.

# Import - third party
from PySide6 import QtWidgets

# Import - standard libraries
from dataclasses import dataclass


@dataclass(frozen=True)
class MainWindowAttr:
    """
    Data class for main window attributes.
    """

    title: str = "Climact-ai"
    width: int = 1440
    height: int = 900


# Main window class
class MainWindow(QtWidgets.QMainWindow):
    """
    The main window class for the Climact-ai application.
    """

    def __init__(self):
        super().__init__()

        self.attrs = MainWindowAttr()
        self.setWindowTitle(self.attrs.title)
        self.resize(self.attrs.width, self.attrs.height)

        # Central widget setup
