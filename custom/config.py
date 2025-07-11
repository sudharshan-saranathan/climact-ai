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

        # Store stream-reference:
        self._stream = stream

        # Buttons:
        self._add = QToolButton(self)
        self._add.setText("Add")
        self._add.setIcon(qta.icon('mdi.plus', color='black'))
        self._add.pressed.connect(self.on_add_pressed)

        self._save = QToolButton(self)
        self._save.setText("Save")
        self._save.setIcon(qta.icon('mdi.check-bold', color='darkgreen'))
        self._save.pressed.connect(self.on_save_pressed)

        # QTableWidget to define custom properties:
        self._prop = QTableWidget(self)
        self._prop.setStyleSheet("QTableWidget {background: white;}")
        self._prop.setColumnCount(2)
        self._prop.verticalHeader().setVisible(False)
        self._prop.verticalScrollBar().setVisible(True)
        self._prop.horizontalHeader().setSectionResizeMode(1, QHeaderView.ResizeMode.Stretch)
        self._prop.setHorizontalHeaderLabels(["Attribute", "Value"])

        for attr in stream.constant_attr:
            row  = self._prop.rowCount()
            item = QTableWidgetItem(attr)
            item.setFlags(item.flags() & ~Qt.ItemFlag.ItemIsEditable)  # Make the constant attribute non-editable
            item.setIcon(qta.icon('mdi.check-bold', color='darkgreen'))

            if  attr in ["strid", "color", "units"]:
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

    def on_add_pressed(self):

        attr_value = QTableWidgetItem()
        attr_label = QTableWidgetItem()
        attr_label.setIcon(qta.icon('ph.warning', color='orange'))

        self._prop.insertRow(self._prop.rowCount())
        self._prop.setItem(self._prop.rowCount() - 1, 0, attr_label)
        self._prop.setItem(self._prop.rowCount() - 1, 1, attr_value)

    def on_save_pressed(self):

        self._stream.variable_attr.clear()
        for row in range(self._prop.rowCount()):
            label_item = self._prop.item(row, 0)
            value_item = self._prop.item(row, 1)

            if  label_item.text():
                attr_label = label_item.text()
                attr_value = value_item.text()

                self._stream.variable_attr[attr_label] = attr_value
                label_item.setIcon(qta.icon('mdi.check-bold', color='darkgreen'))

# Class to configure resource-type_db:
class StreamConfig(QDialog):

    # Constructor:
    def __init__(self, type_db: set, parent: QWidget | None = None):
        super().__init__(parent)
        super().setWindowFlag(Qt.WindowType.Window)

        # Instantiate the toolbox for stream editors:
        self._box = QToolBox(self)

        # Buttons:
        self._add  = QPushButton(qta.icon('mdi.plus', color='black'), "New", self)
        self._del  = QPushButton(qta.icon('mdi.close-circle', color='red'), "Del", self)
        self._okay = QPushButton(qta.icon('mdi.check-bold', color='lightgreen'), "Ok", self)
        self._okay.pressed.connect(self.accept)

        # Add items to the toolbox:
        for stream in type_db:
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

    def on_new_stream(self):
        new_stream = Stream(strid="New Stream", color=Qt.GlobalColor.blue)
        self._box.addItem(StreamEditor(new_stream, self), new_stream.icon or QIcon(), new_stream.strid)
