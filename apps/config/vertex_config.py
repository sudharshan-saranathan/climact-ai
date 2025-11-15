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
from PySide6.QtWidgets import QComboBox, QFormLayout

class VertexConfig(QtWidgets.QDialog):

    # Default constructor:
    def __init__(self,
                 vertex: QtWidgets.QGraphicsObject,
                 parent: QtWidgets.QWidget | None = None):

        # Base-class initialization:
        super().__init__(parent)

        # Set properties:
        self.resize(900, 720)
        self.setStyleSheet("QScrollArea {background: #3a4043;}")

        # Widget selector:
        self._selector = QtWidgets.QComboBox(self)
        self._selector.addItems(['Global Settings', 'Parameters', 'Equations'])
        self._selector.setMinimumWidth(360)

        # Widget(s):
        self._table  = QtWidgets.QTableWidget()
        self._input  = QtWidgets.QListWidget(); self._input.addItems(["Input_A", "Input_B", "Input_C"])
        self._output = QtWidgets.QListWidget(); self._output.addItems(["Output_X", "Output_Y"])
        self._params = QtWidgets.QListWidget(); self._params.addItems(["Param_1", "Param_2", "Param_3", "Param_4"])

        # Form Layout:
        self._form = QFormLayout()
        self._form.setSpacing(8)
        self._form.setContentsMargins(8, 8, 0, 0)
        self._form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self._form.addRow("Vertex:" , QtWidgets.QLabel(f"<p style='color: darkcyan'>{vertex.property('label')}</p>"))
        self._form.addRow("Group:"  , QtWidgets.QLabel(f"<p style='color: darkcyan'>{vertex.property('group')}</p>"))
        self._form.addRow("Inputs:" , self._input)
        self._form.addRow("Params:" , self._params)
        self._form.addRow("Outputs:", self._output)

        # Initialize layout:
        self._layout = QtWidgets.QGridLayout(self)
        self._layout.setContentsMargins(4, 0, 4, 4)
        self._layout.setSpacing(2)
        self._layout.addWidget(self._selector, 0, 0, QtCore.Qt.AlignmentFlag.AlignTop | QtCore.Qt.AlignmentFlag.AlignLeft)
        self._layout.addLayout(self._form , 1, 0)
        self._layout.addWidget(self._table, 0, 1, 2, 1)
        self._layout.setRowStretch(1, 10)
        self._layout.setColumnStretch(1, 10)
