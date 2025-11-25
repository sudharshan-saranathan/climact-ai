# Encoding: utf-8
# Module name: tabview
# Description: A tab-switching widget for the Climact application

# -------
# Imports
# PySide6:
from PySide6 import QtGui
from PySide6 import QtCore
from PySide6 import QtWidgets

# Qtawesome
import qtawesome as qta

from apps.schema.viewer import Viewer
from apps.schema.canvas import Canvas

TabViewOpts = {
    'max-tabs'  : 8,
}

# Tab switcher class:
class TabView(QtWidgets.QTabWidget):

    # Signals:
    sig_reload_canvas = QtCore.Signal(Canvas)

    # Default constructor:
    def __init__(self, parent: QtWidgets.QWidget | None = None, **kwargs):

        # Base-class initialization:
        super().__init__(parent, **kwargs)

        # Set class-level attribute(s):
        self.setTabPosition(QtWidgets.QTabWidget.TabPosition.North)
        self.setTabShape(QtWidgets.QTabWidget.TabShape.Rounded)
        self.setIconSize(QtCore.QSize(20, 20))

        # Create a default tab:
        self.create_tab(None)
        self.setCornerWidget(self._init_toolbar())

        # Connect the tab widget's signals to appropriate slots:
        self.tabCloseRequested.connect(self._on_tab_close)
        self.tabBarClicked.connect(self._on_tab_clicked)

        # Shortcuts:
        QtGui.QShortcut('Ctrl+T', self, self.create_tab)
        QtGui.QShortcut('Ctrl+W', self, self.remove_tab)
        QtGui.QShortcut('Ctrl+R', self, self.rename_tab)

    # Initialize the toolbar:
    def _init_toolbar(self) -> QtWidgets.QToolBar:

        toolbar = QtWidgets.QToolBar(self)
        toolbar.setIconSize(QtCore.QSize(20, 20))
        toolbar.addAction(qta.icon('mdi.keyboard', color='white'), 'Shortcuts')
        toolbar.addAction(qta.icon('mdi.plus-box', color='white'), 'New Tab', self.create_tab)
        toolbar.addAction(qta.icon('mdi.camera', color='white'), 'Save Snapshot')

        return toolbar

    # Create a new tab:
    def create_tab(
            self,
            name: str = None,
            widget: QtWidgets.QWidget | None = None
    ):
        """
        Create a new tab.
        :param name: The name of the new tab.
        :param widget: The widget to display in the tab.
        :return: None
        """

        # Check if maximum tabs reached:
        if self.count() >= TabViewOpts['max-tabs']:   QtWidgets.QApplication.beep(); return

        count  = self.count()
        widget = widget or Viewer()
        name   = name   or f"Tab {count + 1}"

        # Create a new tab and set the widget:
        self.addTab(widget, name)
        self.setTabIcon(count, qta.icon('mdi.lightbulb', color='darkcyan'))

        # If the widget is a Viewer, connect its canvas-updated signal to the tab-updated signal:
        if  isinstance(widget, Viewer):
            widget.canvas.sig_canvas_updated.connect(lambda: self.sig_reload_canvas.emit(widget.canvas))

    # Remove the current tab:
    def remove_tab(self) -> None:
        """
        Remove the current tab.
        :return:
        """

        # Remove the current tab:
        self._on_tab_close(self.currentIndex())

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
        name = name or QtWidgets.QInputDialog.getText(self, 'Tab Rename', 'Enter new label:')[0]

        # Rename the tab:
        if 0 <= index < self.count() and name:  self.setTabText(index, name)

    # ------------------------------------------------------------------------------------------------------------------
    # Event handlers for user-driven events:

    # Remove the tab at the specified index:
    def _on_tab_close(self, index: int) -> None:
        """
        Remove the current tab.
        :param index: The index of the tab to remove.
        :return: None
        """

        # Remove the tab:
        if self.count() > 1:    self.removeTab(index)   # Remove the tab if more than one exists.
        else:                   QtWidgets.QApplication.beep()     # Emit a beep if only one tab remains.

    # When the user clicks a tab:
    def _on_tab_clicked(self, index: int) -> None:
        """
        When the user clicks a tab.
        :param index: The index of the clicked tab.
        :return: None
        """

        if  isinstance(viewer := self.widget(index), Viewer):
            self.sig_reload_canvas.emit(viewer.canvas)