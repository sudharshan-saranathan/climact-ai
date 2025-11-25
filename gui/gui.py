# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: gui
# Description: The main GUI window for the Climact application
# ----------------------------------------------------------------------------------------------------------------------

# Library Imports
# Library Name: PySide6
# Installation: pip install PySide6
# Description:  PySide6 is the official Python module from the Qt for Python project, which provides access to the complete Qt 6.x framework.

from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QMainWindow, QFrame, QToolBar, QStatusBar, QDockWidget

import qtawesome as qta

from gui.dock import Dock
from gui.llm import Assistant
from gui.navigator import Navigator

# Climact submodule(s):
from gui.tabview import TabView
from obj.search import Search

class MainGui(QMainWindow):

    # Default constructor:
    def __init__(self):

        # Base-class initialization:
        super().__init__()

        # Instantiate additional widget(s):
        self._navbar = Navigator(self, callback=self._on_action_triggered)
        self._switch = TabView(self, movable=True, tabsClosable=True)
        self._docket = Dock("Widget Stack", self, tabview=self._switch)
        self._assist = Assistant()

        # Minimize, maximize, close buttons:
        self._trio = QToolBar(self)
        self._trio.setIconSize(QSize(20, 20))
        self._trio.addAction(qta.icon('mdi.minus-circle', color='#ffcb00'), "Minimize", self.showMinimized)
        self._trio.addAction(qta.icon('mdi.stop-circle' , color='#aaff00'), "Maximize", self.showMaximized)
        self._trio.addAction(qta.icon('mdi.close-circle', color='#db5461'), "Close", self.close)
        self._trio.setStyleSheet("QToolBar {"
                                 "background: black;"
                                 "border-radius: 6px;"
                                 "padding: 2px;"
                                 "}"
                                 "QToolBar QToolButton {"
                                 "margin: 0px;"
                                 "padding: 0px;"
                                 "}")

        # Initialize the menu bar:
        self._init_menubar()

        # Install widget(s):
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._docket)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self._navbar)
        self.setCentralWidget(self._switch)
        self.setStatusBar(QStatusBar(self))
        self.statusBar().setFixedHeight(24)

        # Show the GUI:
        self.showMaximized()

    # Initialize the menu bar:
    def _init_menubar(self):

        menubar = self.menuBar()
        menubar.setNativeMenuBar(False)
        menubar.addMenu("File")
        menubar.addMenu("Edit")
        menubar.addMenu("View")
        menubar.addMenu("Help")
        menubar.setCornerWidget(self._trio)

    # Event to handle the navbar's actions:
    def _on_action_triggered(self, string: str):

        # Toggle the visibility of the dock widget:
        if  string.lower() == "dock":
            self._docket.setVisible(not self._docket.isVisible())

        # Handle other actions: