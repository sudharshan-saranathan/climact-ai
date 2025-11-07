# Encoding: utf-8
# Module name: gui
# Description: The main GUI window for the Climact application

# --------------
# Module imports
# --------------
# PySide6:
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QMenuBar, QDockWidget, QStatusBar, QTextEdit, QWidget, QListWidget, QLineEdit

from apps.gemini.widget import Assistant
from gui.dashboard import Dashboard
# Climact submodule(s):
from gui.navbar import NavBar
from gui.tabber import Tabber
from obj.search import SearchBar


class MainGui(QMainWindow):

    # Default constructor:
    def __init__(self):

        # Base-class initialization:
        super().__init__()

        # Instantiate additional widget(s):
        self._status = QStatusBar()
        self._navbar = NavBar(self)
        self._switch = Tabber(self, movable = True, tabsClosable = True)
        self._docket = self._init_dock()

        # Install dock, status, and central widget:
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._docket)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self._navbar)

        # Set the central widget and status bar:
        self.setCentralWidget(self._switch)
        self.setStatusBar(self._status)

        # Show the GUI:
        self.setWindowFlag(Qt.WindowType.Widget)
        self.showMaximized()

    # Initialize the dock widget:
    def _init_dock(self) -> QDockWidget:

        # Add an instance of the Assistant widget to the dock:
        assistant = Assistant()
        assistant.sig_get_response.connect(self._switch.get_response_from_llm)

        # Instantiate the dock:
        dock = QDockWidget("Dashboard")
        dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        dock.setMinimumWidth(320)

        # Return the dock-widget:
        return dock