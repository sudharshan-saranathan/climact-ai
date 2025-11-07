# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: tabber
# Description: A tab-switching widget for the Climact application
# ----------------------------------------------------------------------------------------------------------------------

# QtAwesome for iconography:
import qtawesome as qta

# PySide6 submodule(s):
from PySide6.QtGui import QShortcut, QIcon
from PySide6.QtCore import QSize, Signal, Qt
from PySide6.QtWidgets import QTabWidget, QApplication, QWidget, QLineEdit, QTabBar, QToolButton, QToolBar

# Climact submodule(s):
from apps.schema.viewer import Viewer
from obj.search import SearchBar


class SchemaActions(QToolBar):

    def __init__(self, parent: QWidget | None = None):

        # Invoke base-class constructor:
        super().__init__(parent)
        super().setObjectName("SchemaActionsToolbar")
        super().setContentsMargins(4, 4, 0, 0)

        self.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)
        self.setIconSize(QSize(32, 32))

        # Add actions:
        self._execute  = self.addAction(qta.icon('mdi.play', color='green'), "Execute")
        self._validate = self.addAction(qta.icon('mdi.check', color='blue'), "Validate")

# Tab switcher class:
class Tabber(QTabWidget):

    # Constants:
    MAX_TABS = 8

    # Signals:
    sig_display_config = Signal(QWidget)

    # Default constructor:
    def __init__(self, *args, **kwargs):

        # Base-class initialization:
        super().__init__(*args, **kwargs)

        self.setTabPosition(QTabWidget.TabPosition.North)
        self.setTabShape(QTabWidget.TabShape.Rounded)
        self.setIconSize(QSize(20, 20))

        # Create two default tabs:
        self.create_tab(None)

        # Connect tab-signals:
        self.tabCloseRequested.connect(self.on_tab_close)

        # Shortcuts:
        QShortcut('Ctrl+T', self, self.create_tab)
        QShortcut('Ctrl+W', self, self.remove_tab)

    # Create a new tab:
    def create_tab(self, name: str = None) -> None:
        """
        Create a new tab.
        :param name: The name of the new tab.
        :return: None
        """

        # Check if maximum tabs reached:
        if self.count() >= self.MAX_TABS:   QApplication.beep(); return

        # Instantiate Viewer:
        viewer = Viewer()
        viewer.canvas.sig_display_config.connect(self.sig_display_config.emit)

        button = QToolButton()
        button.setIcon(QIcon("rss/icons/pack-one/close.png"))
        button.setIconSize(QSize(12, 12))

        # Add a new tab:
        self.addTab(viewer, name or f"Tab {self.count() + 1}")
        self.setTabIcon(self.count() - 1, qta.icon('mdi.lightbulb', color='orange'))
        self.tabBar().setTabButton(self.count() - 1, QTabBar.ButtonPosition.RightSide, button)

    # Remove the current tab:
    def remove_tab(self) -> None:
        """
        Remove the current tab.
        :return:
        """

        # Remove the current tab:
        self.on_tab_close(self.currentIndex())

    # Rename an existing tab:
    def rename_tab(self, index: int, name: str) -> None:
        """
        Rename an existing tab.
        :param index: The index of the tab to rename.
        :param name: The new name for the tab.
        :return: None
        """

        # Rename the tab:
        if 0 <= index < self.count():   self.setTabText(index, name)
        else:                           raise IndexError("Tab index out of range.")

    # Remove the current tab:
    def on_tab_close(self, index: int) -> None:
        """
        Remove the current tab.
        :param index: The index of the tab to remove.
        :return: None
        """

        # Remove the tab:
        if self.count() > 1:    self.removeTab(index)   # Remove the tab if more than one exists.
        else:                   QApplication.beep()     # Emit a beep if only one tab remains.

    # Execute a command from the command prompt:
    def get_response_from_llm(self, message: str) -> None:

        print(f"Received message in Tabber: {message}")
        if  isinstance(viewer := self.currentWidget(), Viewer):
            viewer.get_response_from_llm(message)

