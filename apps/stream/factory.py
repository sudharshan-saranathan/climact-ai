# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: factory
# Description: Factory for resource stream types.
# ----------------------------------------------------------------------------------------------------------------------

from PySide6 import QtCore
from PySide6 import QtWidgets

from typing import Dict, Type
from apps.stream.base    import FlowBases
from apps.stream.params  import ParamBases
from apps.stream.derived import DerivedStreams

import qtawesome as qta

class StreamGrid(QtWidgets.QFrame):
    """
    A grid layout to display resource streams.
    """

    # Default constructor:
    def __init__(self, parent: QtWidgets.QWidget = None):

        # Base-class initialization:
        super().__init__(parent)
        super().setStyleSheet("QToolButton {background: transparent; border: none;}")

        # Helper function to create a button:
        def _button(icon: str, label: str, color: str) -> QtWidgets.QToolButton:

            tool = QtWidgets.QToolButton(self)
            tool.setIcon(qta.icon(icon, color=color))
            tool.setText(label)
            tool.setToolButtonStyle(QtCore.Qt.ToolButtonStyle.ToolButtonIconOnly)
            return tool

        # Set up the grid layout:
        self.layout = QtWidgets.QGridLayout(self)
        self.layout.setContentsMargins(2, 2, 2, 2)
        self.layout.setSpacing(2)

        for i, (key, stream) in enumerate((FlowBases | DerivedStreams).items()):

            self.layout.addWidget(
                _button(stream.ICON, stream.LABEL, stream.COLOR),
                i // 4,
                i % 4
            )