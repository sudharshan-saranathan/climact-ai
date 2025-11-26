# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: dock
# Description: A dockable widget for the Climact application GUI.
# ----------------------------------------------------------------------------------------------------------------------

# Import(s):
# PySide6:
from PySide6 import QtCore
from PySide6 import QtWidgets

# QtAwesome and util:
import util
import qtawesome as qta

# Climact submodules:
from apps.gemini.chat import Chat
from gui.schematic import Schematic
from gui.setting import GlobalSettings

# class Dock: A dockable widget for the Climact application GUI.
class Dock(QtWidgets.QDockWidget):

    # Default constructor:
    def __init__(
            self,
            title: str = "Dock",
            parent: QtWidgets.QWidget | None = None,
            **kwargs
    ):

        # Base-class initialization:
        super().__init__(title, parent)

        # Set properties:
        self.setProperty('tabview', kwargs.get('tabview', None))
        self.setFeatures(QtWidgets.QDockWidget.DockWidgetFeature.NoDockWidgetFeatures)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)

        # Header widgets:
        self._header = QtWidgets.QFrame(self)
        self._layout = QtWidgets.QHBoxLayout(self._header)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(2)

        # Child widget(s):
        self._combo = util.combobox(self,
                               actions = [
                                   ('ph.gear-fill', '#efefef', "Global Settings"),
                                   ('ph.tree-structure-fill', '#efefef', "Schematic"),
                                   ('ph.chat-fill', '#efefef', "Assistant"),
                                   ('ph.database-fill', '#efefef', "Database"),
                                   ('ph.laptop-fill', '#efefef', "Optimise")
                                ]
                               )

        # Add the combo-box and toolbar to the layout:
        self._layout.addWidget(self._combo)

        # Tree Widget:
        self._global = GlobalSettings()
        self._tree = Schematic(self)
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
            if  hasattr(tabview, 'sig_reload_canvas'):
                tabview.sig_reload_canvas.connect(self._tree.reload)

    # Switch stacked widget page:
    def switch_to(self, index: int):    self._stack.setCurrentIndex(index)