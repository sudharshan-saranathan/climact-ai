# Encoding: utf-8
# Module name: util
# Description: Utility functions and classes for the Climact application.
# ----------------------------------------------------------------------------------------------------------------------

# Import(s):
# Typing:
from typing import Any

# PySide6:\
from PySide6 import QtCore
from PySide6 import QtWidgets

# QtAwesome:
import qtawesome as qta

# Creates a toolbar with optional widgets and actions:
def toolbar(parent: QtWidgets.QWidget | None = None,
            alignment: QtCore.Qt.AlignmentFlag = QtCore.Qt.AlignmentFlag.AlignRight,
            widgets: list[QtWidgets.QWidget] | None = None,
            actions: list[tuple[str, str, str, Any]] | None = None
) -> QtWidgets.QToolBar:

    """
    Creates a toolbar with optional widgets and actions.
    :param parent: parent widget
    :param alignment: Alignment of the toolbar contents.
    :param widgets: A list of widgets to add to the toolbar.
    :param actions: A list of actions to add to the toolbar.
    :return: A QToolBar instance with the specified widgets and actions.
    """

    # Expander to push items to the specified alignment:
    _expander = QtWidgets.QFrame()
    _expander.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

    _toolbar = QtWidgets.QToolBar(parent)
    _toolbar.setIconSize(QtCore.QSize(16, 16))
    _toolbar.setContentsMargins(0, 0, 0, 0)

    # Add expander based on alignment:
    if  alignment == QtCore.Qt.AlignmentFlag.AlignRight:

        _toolbar.addWidget(_expander)                           # Add expander first for right alignment
        for _widget in widgets or []:                           # Then add widgets
            _toolbar.addWidget(_widget)

        for _icon, _color, _text, _callback in actions or []:   # Then add actions (icons)
            _toolbar.addAction(
                qta.icon(_icon, color = _color),
                _text,
                _callback
            )

    elif alignment == QtCore.Qt.AlignmentFlag.AlignLeft:        # Left alignment (reverse order)

        for _widget in widgets or []:
            _toolbar.addWidget(_widget)

        for _icon, _color, _text, _callback in actions or []:
            _toolbar.addAction(
                qta.icon(_icon, color = _color),
                _text,
                _callback
            )

        _toolbar.addWidget(_expander)                           # Add expander last for left alignment

    # Return the toolbar:
    return _toolbar

# Returns a combo box with specified actions:
def combobox(parent: QtWidgets.QWidget | None = None,
             actions: list[tuple[str, str, str]] | None = None
) -> QtWidgets.QComboBox:

    """
    Creates a combo box with specified actions.
    :param parent: parent widget
    :param actions: A list of actions to add to the combo box.
    :return: A QComboBox instance with the specified actions.
    """

    # Create the combo box and set style:
    _combo = QtWidgets.QComboBox(parent)
    _combo.setStyleSheet("QComboBox {"
                         "margin: 4px 0px 4px 0px;"
                         "}"
                         "QComboBox QAbstractItemView {"
                         "background: #363e43;"
                         "border-radius: 4px;"
                         "}")

    # Set icon size and add items:
    _combo.setIconSize(QtCore.QSize(16, 16))
    for _icon, _color, _text in actions or []:
        _combo.addItem(qta.icon(_icon, color=_color), _text)

    # Return the combo box:
    return _combo