# ---
# Encoding: utf-8
# Module name: combo
# Description: A combo box widget for selecting different views in the Climact application GUI.
# ----------------------------------------------------------------------------------------------------------------------

from PySide6 import QtCore
from PySide6 import QtWidgets

import qtawesome as qta

class ComboBox(QtWidgets.QComboBox):

    # Default constructor:
    def __init__(self, parent: QtWidgets.QWidget | None = None, **kwargs):

        # Base-class initialization:
        super().__init__(parent)

        # Set style:
        self.setStyleSheet("QComboBox {"
                          "margin: 4px 0px 4px 0px;"
                          "}"
                          "QComboBox QAbstractItemView {"
                          "background: #363e43;"
                          "border-radius: 4px;"
                          "}")

        # Set icon size:
        self.setIconSize(QtCore.QSize(16, 16))

        # Add combo items if available:
        for icon, color, text in kwargs.get('actions', []):
            self.addItem(qta.icon(icon, color=color), text)