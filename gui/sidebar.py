# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: dashboard
# Description: A dashboard widget for the Climact application
# ----------------------------------------------------------------------------------------------------------------------

# Import(s):
# PySide6
from PySide6 import QtWidgets
from PySide6.QtWidgets import QWidget

from apps.gemini.widget import Chat


# Class Board:
class SideBar(QtWidgets.QStackedWidget):

    # Default constructor:
    def __init__(self, parent: QtWidgets.QWidget | None = None):

        # Base-class initialization:
        super().__init__(parent)

        # Schematic Tree:
        self._library   = QtWidgets.QWidget(self)
        self._assistant = Chat(self)
        self._schematic = QtWidgets.QTreeWidget(self)
        self._schematic.setHeaderHidden(True)

        # Add widgets to the stack:
        self.addWidget(self._schematic)
        self.addWidget(self._assistant)
        self.addWidget(self._library)

        # Set default index:
        self.setCurrentIndex(0)

    # Switch to a particular page:
    def switch(self, index: int) -> None:
        """
        Switch to a particular page.
        :param index: The index of the page to switch to.
        :return: None
        """
        self.setCurrentIndex(index)