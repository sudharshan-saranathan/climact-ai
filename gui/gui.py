# Encoding: utf-8
# Module name: gui
# Description: The main GUI window for the Climact application

# --------------
# Module imports
# --------------
# PySide6:
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QMenuBar, QDockWidget

from gui.navbar import NavBar
# Climact submodule(s):
from gui.tabber import Tabber

class MainGui(QMainWindow):

    # Default constructor:
    def __init__(self):

        # Base-class initialization:
        super().__init__()

        # Instantiate additional widget(s):
        self._docket = QDockWidget()
        self._navbar = NavBar(self)
        self._switch = Tabber(self, movable=True, tabsClosable=True)

        # Install widget(s):
        self.addToolBarBreak(Qt.ToolBarArea.LeftToolBarArea)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self._navbar)
        self.setCentralWidget(self._switch)

        # Show the GUI:
        self.showMaximized()

    #