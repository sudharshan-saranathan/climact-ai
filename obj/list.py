# -
# Encoding: utf-8
# Module name: map
# Description: A widget for displaying the schematic's contents.
# ----------------------------------------------------------------------------------------------------------------------
from typing import Any

# PySide6:
from PySide6 import QtCore, QtGui
from PySide6 import QtWidgets

# QtAwesome:
import qtawesome as qta

# Climact submodule:
from apps.schema.canvas import Canvas


# List widget for displaying canvas items of a specific class:
class List(QtWidgets.QListWidget):

    # Default constructor:
    def __init__(self, parent: QtWidgets.QWidget | None = None):

        # Base-class initialization:
        super().__init__(parent)

    # Method to construct a widget:
    @classmethod
    def _widget(
            cls,
            _object: QtWidgets.QGraphicsObject,
            _widgets: list[QtWidgets.QWidget] | None = None,
            _actions: list[tuple[str, str, str]] | None = None
    ) -> QtWidgets.QToolBar:

        expander = QtWidgets.QFrame()
        expander.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        toolbar = QtWidgets.QToolBar()
        toolbar.setIconSize(QtCore.QSize(16, 16))
        toolbar.addWidget(QtWidgets.QLabel(_object.property('label')))
        toolbar.addWidget(expander)

        for widget in _widgets or []:
            toolbar.addWidget(widget)

        for icon, color, text in _actions or []:
            toolbar.addAction(qta.icon(icon, color=color), text, getattr(_object, text.lower()))

        return toolbar

    # Method to reload canvas contents:
    def load(
            self,
            _list: list,
            widgets: list[QtWidgets.QWidget] | None = None,
            actions: list[tuple[str, str, str]] | None = None
    ):
        # Clear the current list:
        self.clear()

        # Add each object in the provided list:
        for _object in _list:

            tool = self._widget(_object, widgets, actions)
            item = QtWidgets.QListWidgetItem(self)
            item.setIcon(_object.icon())

            self.setItemWidget(item, tool)