# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: config
# Description: Configuration utility for different QGraphicsObject-subclasses.
# ----------------------------------------------------------------------------------------------------------------------

# Import(s):
# PySide6:
from PySide6 import QtCore
from PySide6 import QtWidgets

import qtawesome as qta

class Configurator(QtWidgets.QWidget):

    # Default constructor:
    def __init__(self, parent: QtWidgets.QWidget | None = None):

        # Base-class initialization:
        super().__init__(parent)
        super().resize(640, 480)

        # QListWidget:
        self._list = QtWidgets.QListWidget(self)
        self._list.addItem("Hello")

        # Initialize layout:
        self._layout = QtWidgets.QGridLayout()
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(2)
        self._layout.addWidget(self._list)