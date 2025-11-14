# Encoding: utf-8
# Module name: tabber
# Description: A tab-switching widget for the Climact application

# -------
# Imports
# PySide6:
from PySide6.QtGui import QShortcut
from PySide6.QtCore import QSize, Signal
from PySide6.QtWidgets import QTabWidget, QWidget, QApplication, QInputDialog, QGraphicsObject, QToolBar

# Qtawesome
import qtawesome as qta

from apps.schema.viewer import Viewer

# Tab switcher class:
class TabView(QTabWidget):

    # Signals:
    sig_canvas_updated = Signal(QGraphicsObject)

    # Constants:
    MAX_TABS = 8

    # Default constructor:
    def __init__(self, parent: QWidget | None = None, **kwargs):

        # Base-class initialization:
        super().__init__(parent, **kwargs)

        # Set class-level attribute(s):
        self.setTabPosition(QTabWidget.TabPosition.North)
        self.setTabShape(QTabWidget.TabShape.Rounded)
        self.setIconSize(QSize(20, 20))

        # Create two default tabs:
        self.create_tab(None)

        # Connect tab-signals:
        self.tabCloseRequested.connect(self.on_tab_close)

        # Add a toolbar in the corner:
        self._toolbar = QToolBar(self)
        self._toolbar.addAction(qta.icon('mdi.keyboard', color='white'), 'Shortcuts', )
        self._toolbar.addAction(qta.icon('mdi.tab-plus', color='white'), 'New Tab'  , self.create_tab)
        self._toolbar.setIconSize(QSize(20, 20))
        self.setCornerWidget(self._toolbar)

        # Shortcuts:
        QShortcut('Ctrl+T', self, self.create_tab)
        QShortcut('Ctrl+W', self, self.remove_tab)
        QShortcut('Ctrl+R', self, self.rename_tab)

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
        self.addTab(viewer := Viewer(), name or f"Tab {self.count() + 1}")
        self.setTabIcon(self.count() - 1, qta.icon('mdi.lightbulb', color='darkcyan'))

        # Forward the canvas' signals as this tabview's signals:
        viewer.canvas.sig_canvas_updated.connect(self.sig_canvas_updated.emit)

    # Remove the current tab:
    def remove_tab(self) -> None:
        """
        Remove the current tab.
        :return:
        """

        # Remove the current tab:
        self.on_tab_close(self.currentIndex())

    # Rename an existing tab:
    def rename_tab(self, index: int = -1, name: str = str()) -> None:
        """
        Rename an existing tab.
        :param index: The index of the tab to rename.
        :param name: The new name for the tab.
        :return: None
        """

        # If no index provided, use the current tab:
        if index == -1:    index = self.currentIndex()

        # If no name is provided, get name from user:
        name = name or QInputDialog.getText(self, 'Tab Rename', 'Enter new label:')[0]

        # Rename the tab:
        if 0 <= index < self.count() and name:  self.setTabText(index, name)

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