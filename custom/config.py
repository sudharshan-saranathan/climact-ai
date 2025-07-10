import qtawesome as qta
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QDialog, QWidget, QToolBox, QGridLayout, QHeaderView, QListWidget, QListWidgetItem, \
    QTableWidget, \
    QTableWidgetItem, QToolButton, QLabel, QLineEdit, QColorDialog, QPushButton


class StreamEditor(QWidget):

    def __init__(self, stream, parent: QWidget | None = None, **kwargs):
        super().__init__(parent)
        super().setStyleSheet("QWidget {"
                              "background: lightgray;"
                              "}"
                              "QToolButton {"
                              "padding: 0px;"
                              "}")

        # Buttons:
        self._add = QToolButton(self)
        self._add.setText("Add")
        self._add.setIcon(qta.icon('mdi.plus', color='black'))
        self._add.pressed.connect(lambda: self._prop.insertRow(self._prop.rowCount()))

        self._save = QToolButton(self)
        self._save.setText("Save")
        self._save.setIcon(qta.icon('mdi.check-bold', color='darkgreen'))

        # QTableWidget to define custom properties:
        self._prop = QTableWidget(self)
        self._prop.setStyleSheet("QTableWidget {background: white;}")
        self._prop.setColumnCount(2)
        self._prop.verticalHeader().setVisible(False)
        self._prop.verticalScrollBar().setVisible(True)
        self._prop.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self._prop.setHorizontalHeaderLabels(["Attribute", "Value"])

        for attr in stream.attr:
            row  = self._prop.rowCount()
            item = QTableWidgetItem(attr)

            if attr in ["strid", "color", "units"]:
                item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make the attribute name non-editable

            self._prop.insertRow(row)
            self._prop.setItem(row, 0, item)
            self._prop.setItem(row, 1, QTableWidgetItem())

        self._grid = QGridLayout(self)
        self._grid.setSpacing(2)
        self._grid.setContentsMargins(0, 0, 0, 2)
        self._grid.setColumnStretch(0, 10)

        self._grid.addWidget(self._prop, 0, 0, 1, 3)
        self._grid.addWidget(self._add , 1, 1, Qt.AlignmentFlag.AlignRight)
        self._grid.addWidget(self._save, 1, 2, Qt.AlignmentFlag.AlignRight)

# Class to configure resource-streams:
class StreamConfig(QDialog):

    # Constructor:
    def __init__(self, streams: set, parent: QWidget | None = None):
        super().__init__(parent)
        super().setWindowFlag(Qt.WindowType.Window)

        # Instantiate the toolbox for stream editors:
        self._box = QToolBox(self)

        # Buttons:
        self._add  = QPushButton(qta.icon('mdi.plus', color='black'), "New", self)
        self._del  = QPushButton(qta.icon('mdi.close-circle', color='red'), "Delete", self)
        self._okay = QPushButton(qta.icon('mdi.check-bold', color='lightgreen'), "Ok", self)

        for stream in streams:
            self._box.addItem(
                StreamEditor(stream, self, editable=False),
                stream.icon or QIcon(),
                stream.strid
            )

        # Create a layout:
        self._lay = QGridLayout(self)
        self._lay.setColumnStretch(0, 10)
        self._lay.setContentsMargins(4, 4, 4, 4)
        self._lay.setSpacing(2)

        self._lay.addWidget(self._box , 0, 0, 1, 4)
        self._lay.addWidget(self._add , 1, 1, Qt.AlignmentFlag.AlignRight)
        self._lay.addWidget(self._del , 1, 2, Qt.AlignmentFlag.AlignRight)
        self._lay.addWidget(self._okay, 1, 3, Qt.AlignmentFlag.AlignRight)
