# Encoding: utf-8
# Module name: switcher
# Description: A tab-switching widget for the Climact application

# -------
# Imports
# PySide6:
from PySide6.QtGui import QShortcut, QIcon
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QToolBar, QWidget, QSizePolicy

from conf import GlobalIcons


# Navigation pane:
class NavBar(QToolBar):

    # Default constructor:
    def __init__(self, *args, **kwargs):

        # Base-class initialization:
        super().__init__(*args, **kwargs)
        super().setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        # Spacer(s):
        self._l = QWidget()
        self._r = QWidget()
        self._l.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._r.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self._l.setStyleSheet("background: transparent;")
        self._r.setStyleSheet("background: transparent;")

        self.addWidget(self._l)

        # Set the default icon size:
        self.setIconSize(QSize(36, 36))

        # Install tool-buttons:
        self._open   = self.addAction(QIcon(GlobalIcons["NavBar"]['open'])  , "Open")
        self._save   = self.addAction(QIcon(GlobalIcons["NavBar"]['save'])  , "Save")
        self._draw   = self.addAction(QIcon(GlobalIcons["NavBar"]['draw'])  , "Draw")
        self._conf   = self.addAction(QIcon(GlobalIcons["NavBar"]['conf'])  , "Config")
        self._plot   = self.addAction(QIcon(GlobalIcons["NavBar"]['plot'])  , "Plot")
        self._libs   = self.addAction(QIcon(GlobalIcons["NavBar"]['libs'])  , "Library")
        self._python = self.addAction(QIcon(GlobalIcons["NavBar"]['python']), "Python")
        self.addWidget(self._r)
