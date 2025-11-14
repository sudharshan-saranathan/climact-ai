# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: config
# Description: Configuration utility for different QGraphicsObject-subclasses.
# ----------------------------------------------------------------------------------------------------------------------

# Import(s):
# PySide6:
from PySide6 import QtCore
from PySide6 import QtWidgets

class Configurator(QtWidgets.QDialog):

    # Default constructor:
    def __init__(self, item: QtWidgets.QGraphicsObject, parent: QtWidgets.QWidget | None = None):

        # Base-class initialization:
        super().__init__(parent)

        # Set window properties:
        self.setWindowTitle(f"Configure: {item.property('label')}")
        self.setFixedSize(1200, 720)

        # Tabs:
        selector = QtWidgets.QComboBox(self)
        selector.addItem("Global Settings")
        selector.addItem("Parameters")
        selector.addItem("Equations")
        selector.setFixedWidth(240)

        # Layout:
        self._layout = QtWidgets.QGridLayout(self)
        self._layout.setContentsMargins(4, 4, 4, 4)
        self._layout.setSpacing(2)

        self._layout.addWidget(selector, 0, 0, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self._layout.addWidget(QtWidgets.QStackedWidget(), 1, 0)
        self._layout.setRowStretch(1, 10)

