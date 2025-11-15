# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: setting
# Description: A global settings widget for the Climact application.
# ----------------------------------------------------------------------------------------------------------------------

# Import(s):
# PySide6:
from PySide6 import QtCore
from PySide6 import QtWidgets

# Climact submodule(s):
from apps.config.stream_config import StreamConfigWidget

# Global settings widget:
class GlobalSettings(QtWidgets.QWidget):

    # Default constructor:
    def __init__(self, parent: QtWidgets.QWidget | None = None):

        # Base-class initialization:
        super().__init__(parent)
        super().setStyleSheet("QScrollArea {background: #3a4043;}")

        # Buttons layout:
        self._meta_buttons = QtWidgets.QHBoxLayout()
        self._meta_buttons.setSpacing(4)
        self._meta_buttons.setContentsMargins(0, 0, 0, 0)
        self._meta_buttons.addStretch(10)
        self._meta_buttons.addWidget(reset := QtWidgets.QPushButton("Reset"), QtCore.Qt.AlignmentFlag.AlignRight)
        self._meta_buttons.addWidget(apply := QtWidgets.QPushButton("Apply"), QtCore.Qt.AlignmentFlag.AlignRight)

        reset.setObjectName("Reset Button")
        apply.setObjectName("Apply Button")
        apply.pressed.connect(self._on_save_settings)

        # Form Layout:
        self._form = QtWidgets.QFormLayout(self)
        self._form.setSpacing(8)
        self._form.setContentsMargins(8, 8, 0, 0)
        self._form.setFormAlignment(QtCore.Qt.AlignmentFlag.AlignTop)
        self._form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignRight | QtCore.Qt.AlignmentFlag.AlignBottom)
        self._form.addRow("Project Label:", QtWidgets.QLineEdit())
        self._form.addRow("Description:", description := QtWidgets.QTextEdit())
        self._form.addRow("", QtWidgets.QPushButton("Generate Schematic"))
        self._form.addRow("Start Epoch:", start := QtWidgets.QSpinBox())
        self._form.addRow("Final Epoch:", final := QtWidgets.QSpinBox())
        self._form.addRow("Time Step:"  , delta := QtWidgets.QSpinBox())
        self._form.addRow("Resources:"  , resources := StreamConfigWidget())
        self._form.addRow("", self._meta_buttons)

        description.setMaximumHeight(200)
        start.setRange(-100, 100)
        final.setRange(-100, 100)
        delta.setRange(0, 10)
        final.setValue(50)
        delta.setValue(1)

    # Slot to handle saving settings:
    def _on_save_settings(self):

        apply = self.findChild(QtWidgets.QPushButton, "Apply Button")
        apply.setText("Apply")

    def _on_settings_changed(self):

        apply = self.findChild(QtWidgets.QPushButton, "Apply Button")
        apply.setText("Apply")