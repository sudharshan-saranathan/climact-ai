# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: gui
# Description: The main GUI window for the Climact application
# ----------------------------------------------------------------------------------------------------------------------

# Library Imports
# Library Name: PySide6
# Installation: pip install PySide6
# Description:  PySide6 is the official Python module from the Qt for Python project, which provides access to the complete Qt 6.x framework.

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMainWindow, QDockWidget

from gui.llm import Assistant
from gui.sidebar import SideBar
from gui.toolbar import ToolBar

# Climact submodule(s):
from gui.tabview import TabView
from obj.search import Search


class MainGui(QMainWindow):

    # Default constructor:
    def __init__(self):

        # Base-class initialization:
        super().__init__()

        # Instantiate additional widget(s):
        self._navbar = ToolBar(self, callback = self._on_action_triggered)
        self._switch = TabView(self, movable=True, tabsClosable=True)
        self._docket = self._init_dock()
        self._assist = Assistant()

        # Install widget(s):
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._docket)
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, self._navbar)
        self.setCentralWidget(self._switch)

        # Show the GUI:
        self.showMaximized()

    # Initialize dock widget:
    def _init_dock(self):

        dock = QDockWidget("Dashboard", None)
        dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        dock.setMinimumWidth(240)

        dock.setWidget(SideBar(self))
        return dock

    # Event to handle the navbar's actions:
    def _on_action_triggered(self, string: str):

        if  string.lower() == "pane":
            self._docket.setVisible(not self._docket.isVisible())

    # Search callback:
    def on_search(self):

        sender = self.sender()
        if  isinstance(sender, Search):
            print(self._assist.get_response(sender.text()))

