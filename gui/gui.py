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
from PySide6.QtWidgets import QMainWindow, QDockWidget, QToolBar, QComboBox, QStatusBar

import qtawesome as qta

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
        super().setWindowFlag(Qt.WindowType.FramelessWindowHint)

        # Instantiate additional widget(s):
        self._navbar = ToolBar(self, callback = self._on_action_triggered)
        self._switch = TabView(self, movable=True, tabsClosable=True)
        self._docket = self._init_dock()
        self._assist = Assistant()

        # Minimize, maximize, close buttons:
        self._trio = QToolBar(self)
        self._trio.setIconSize(QSize(14, 14))
        self._trio.setStyleSheet("QToolBar {background: transparent;}")
        self._trio.addAction(qta.icon('ph.minus' , color='#efefef'), "Minimize", self.showMinimized)
        self._trio.addAction(qta.icon('ph.square', color='#efefef'), "Maximize", self.showMaximized)
        self._trio.addAction(qta.icon('ph.x', color='red'), "Close", self.close)

        # Define menus:
        self._menubar = self.menuBar()
        self._menubar.setNativeMenuBar(False)
        self._menubar.addMenu("File")
        self._menubar.addMenu("Edit")
        self._menubar.addMenu("View")
        self._menubar.addMenu("Help")
        self._menubar.setCornerWidget(self._trio)

        # Install widget(s):
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self._docket)
        self.addToolBar(Qt.ToolBarArea.LeftToolBarArea, self._navbar)
        self.setCentralWidget(self._switch)
        self.setStatusBar(QStatusBar(self))
        self.statusBar().setFixedHeight(24)

        # Show the GUI:
        self.showMaximized()

    # Initialize dock widget:
    def _init_dock(self):

        combo = QComboBox(self)
        combo.addItem(qta.icon('mdi.file-tree', color='#ffa300'), "Schematic")
        combo.addItem(qta.icon('mdi.chat'     , color='#ffa300'), "Assistant")
        combo.addItem(qta.icon('mdi.library'  , color='#ffa300'), "Library")
        combo.setIconSize(QSize(20, 20))

        dock = QDockWidget(str(), self)
        dock.setFeatures(QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        dock.setWidget(stack := SideBar(self))
        dock.setTitleBarWidget(combo)
        dock.setMinimumWidth(400)

        combo.currentIndexChanged.connect(stack.switch)
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

