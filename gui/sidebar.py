# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: dashboard
# Description: A dashboard widget for the Climact application
# ----------------------------------------------------------------------------------------------------------------------

# PySide6: `pip install PySide6`
from PySide6 import QtCore
from PySide6 import QtWidgets

# QtAwesome for icons:
import qtawesome as qta
from PySide6.QtWidgets import QLineEdit, QTreeWidgetItem


# Class Board:
class Board(QtWidgets.QTreeWidget):

    # Default constructor:
    def __init__(self, parent: QtWidgets.QWidget | None = None):

        # Base-class initialization:
        super().__init__(parent)
        super().setHeaderHidden(True)

        # Add top-level widgets:
        self.addTopLevelItem(QtWidgets.QTreeWidgetItem(self))
        self.addTopLevelItem(QtWidgets.QTreeWidgetItem(self))
        self.addTopLevelItem(QtWidgets.QTreeWidgetItem(self))

        # Customize the top-level items:
        assistant = self.topLevelItem(0)
        assistant.setText(0, 'Assistant')
        assistant.setFlags(assistant.flags() & ~QtCore.Qt.ItemFlag.ItemIsSelectable)
        assistant.addChild(QTreeWidgetItem(assistant))
        self.setItemWidget(assistant.child(0), 0, QtWidgets.QTextEdit())

        schematic = self.topLevelItem(1)
        schematic.setText(0, 'Explorer')
        schematic.setFlags(schematic.flags() & ~QtCore.Qt.ItemFlag.ItemIsSelectable)
        schematic.addChild(QTreeWidgetItem(self))