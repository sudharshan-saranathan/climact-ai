# Encoding: utf-8
# Module name: tabber
# Description: A tab-switching widget for the Climact application

# -------
# Imports
# Qtawesome
import qtawesome as qta
from PySide6.QtCore import QSize

# PySide6:
from PySide6.QtGui import QShortcut
from PySide6.QtWidgets import QTabWidget, QApplication

from apps.schema.viewer import Viewer


# Tab switcher class:
class Tabber(QTabWidget):

    # Constants:
    MAX_TABS = 8

    # Default constructor:
    def __init__(self, *args, **kwargs):

        # Base-class initialization:
        super().__init__(*args, **kwargs)

        # Set class-level attribute(s):
        self.setTabPosition(QTabWidget.TabPosition.North)
        self.setTabShape(QTabWidget.TabShape.Rounded)
        self.setIconSize(QSize(20, 20))

        # Create two default tabs:
        self.create_tab(None)
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

        # Add a new tab:
        self.addTab(Viewer(), name or f"Tab {self.count() + 1}")
        self.setTabIcon(self.count() - 1, qta.icon('mdi.lightbulb', color='orange'))

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