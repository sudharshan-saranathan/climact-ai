# Encoding: utf-8
# Module name: startup_dialog
# Description: Startup dialog for the Climact-ai application.

# Import - standard libraries
from dataclasses import dataclass

# Import - third party
from PySide6 import QtCore, QtWidgets

# Import - local
from path import rpath


@dataclass(frozen=True)
class StartupAttrs:
    width: int = 1200
    height: int = 800


# Startup dialog class
class StartupDialog(QtWidgets.QDialog):
    """
    The startup dialog class for the Climact-ai application.
    """

    def __init__(self):
        super().__init__(None)  # Dialog has no parent

        # Set attributes
        self.attrs = StartupAttrs()
        self.setObjectName("StartupDialog")
        self.setFixedSize(self.attrs.width, self.attrs.height)
        self.setWindowFlag(QtCore.Qt.WindowType.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_TranslucentBackground)

        # Initialize the container
        self._container = QtWidgets.QFrame(self)
        self._container.setObjectName("StartupFrame")
        self._container.setGeometry(0, 0, self.attrs.width, self.attrs.height)

        # Define layout
        layout = QtWidgets.QGridLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(4)

        # Create buttons for different actions
        _button_new_p = QtWidgets.QPushButton("New Project", self._container, flat=True)
        _button_dir_t = QtWidgets.QPushButton("Templates", self._container, flat=True)
        _button_dir_m = QtWidgets.QPushButton("Models", self._container, flat=True)

        _style = (
            "QPushButton {"
            "    background: transparent;"
            "    border: none;"
            "}"
            "QPushButton:hover {"
            "    padding-left: 2px;"
            "    border-radius: 0px;"
            "    border-left: 2px solid #ffcb00;"
            "}"
        )

        _button_new_p.setStyleSheet(_style)
        _button_dir_t.setStyleSheet(_style)
        _button_dir_m.setStyleSheet(_style)

        # Initialize the file-table:

        layout.addWidget(_button_new_p, 0, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(_button_dir_t, 1, 0, QtCore.Qt.AlignmentFlag.AlignRight)
        layout.addWidget(_button_dir_m, 2, 0, QtCore.Qt.AlignmentFlag.AlignRight)
