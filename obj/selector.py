# ---
# Encoding: utf-8
# Module name: selector
# Description: Resource selector utility.
# ----------------------------------------------------------------------------------------------------------------------

# Import(s):
# PySide6:
from PySide6 import QtCore
from PySide6 import QtWidgets

# QtAwesome for icons:
import qtawesome as qta

# Class Selector: A resource selector utility.
class Selector(QtWidgets.QToolBar):

    # Signal:
    sig_selection_changed = QtCore.Signal(str)

    # Default constructor:
    def __init__(self, parent: QtWidgets.QWidget | None = None):

        # Base-class initialization:
        super().__init__(parent)

        self.setIconSize(QtCore.QSize(24, 24))
        self.setStyleSheet("QToolBar {margin: 1px; padding: 0px;}")

        # Expander:
        self._wide = QtWidgets.QWidget(self)
        self._wide.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self._wide.setStyleSheet("background: transparent;")
        self.addWidget(self._wide)

        # Add actions:
        self.addAction(qta.icon('mdi.weight-gram', color='lightblue'), 'Mass')