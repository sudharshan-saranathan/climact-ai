# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: dock
# Description: A dockable widget for the Climact application GUI.
# ----------------------------------------------------------------------------------------------------------------------

from PySide6 import QtCore
from PySide6 import QtWidgets

import qtawesome as qta

from apps.gemini.chat import Chat
from gui.schema import Schema
from gui.setting import GlobalSettings

# class Dock: A dockable widget for the Climact application GUI.
class Dock(QtWidgets.QDockWidget):

    # Default constructor:
    def __init__(self, title: str = "Dock", parent: QtWidgets.QWidget | None = None, **kwargs):

        # Base-class initialization:
        super().__init__(title, parent)

        self.setProperty('tabview', kwargs.get('tabview', None))
        self.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)

        # Header widgets:
        self._header = QtWidgets.QFrame(self)
        self._header.setStyleSheet('QFrame { background: transparent;}')

        self._layout = QtWidgets.QHBoxLayout(self._header)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(2)

        # Child widget(s):
        self._combo = QtWidgets.QComboBox(self)
        self._combo.setStyleSheet("QComboBox {"
                                  "margin: 4px 0px 4px 0px;"
                                  "}"
                                  "QComboBox QAbstractItemView {"
                                  "background: #363e43;"
                                  "border-radius: 4px;"
                                  "}")

        self._combo.addItem(qta.icon('ph.gear-fill', color='#ffcb00'), "Global Settings")
        self._combo.addItem(qta.icon('ph.tree-structure-fill', color='#ffcb00'), "Schematic")
        self._combo.addItem(qta.icon('ph.chat-fill', color='#ffcb00'), "Assistant")
        self._combo.addItem(qta.icon('ph.database-fill', color='#ffcb00'), "Library")
        self._combo.addItem(qta.icon('ph.laptop-fill', color='#ffcb00'), "Optimization")
        self._combo.setIconSize(QtCore.QSize(20, 20))

        # Add the combo-box and toolbar to the layout:
        self._layout.addWidget(self._combo)

        # Tree Widget:
        self._global = GlobalSettings()
        self._tree = Schema(self)
        self._chat = Chat(self)

        # Stacked widget:
        self._stack = QtWidgets.QStackedWidget(self)
        self._stack.addWidget(self._global)
        self._stack.addWidget(self._tree)
        self._stack.addWidget(self._chat)
        self._stack.addWidget(QtWidgets.QLabel("Library widget goes here", self))

        # Set widget:
        self.setTitleBarWidget(self._header)
        self.setWidget(self._stack)

        # Connect the combo-box's signal to the switch_to method:
        self._combo.currentIndexChanged.connect(self.switch_to)

        # If the tabview property is set, connect to its currentChanged signal:
        if  tabview := kwargs.get('tabview', None):
            tabview.sig_canvas_updated.connect(self.refresh_tree)

    # Switch stacked widget page:
    def switch_to(self, index: int):    self._stack.setCurrentIndex(index)

    # Refresh items in the tree:
    def refresh_tree(self):

        if  not self.property('tabview'):
            return

        tabview = self.property('tabview')
        current = tabview.currentWidget().canvas

        # Reconstruct the tree using the canvas:
        self._tree.reload(current)