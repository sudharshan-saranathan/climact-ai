# Encoding: utf-8
# Module name: switcher
# Description: A tab-switching widget for the Climact application

# -------
# Imports
# PySide6:
from PySide6.QtGui import QIcon
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QToolBar, QWidget, QSizePolicy, QLineEdit

from conf import GlobalIcons

import qtawesome as qta

# Navigation pane:
class NavBar(QToolBar):

    # Default constructor:
    def __init__(self, *args, **kwargs):

        # Base-class initialization:
        super().__init__(*args, **kwargs)
        super().setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)

        # Set the default icon size:
        self.setIconSize(QSize(24, 24))

        # Install tool-buttons:
        self._home   = self.addAction(QIcon(GlobalIcons["NavBar"]['home']), "Home")
        self.addSeparator()

        """
        self._open   = self.addAction(QIcon(GlobalIcons["NavBar"]['open']), "Open")
        self._save   = self.addAction(QIcon(GlobalIcons["NavBar"]['save']), "Save")
        self._build  = self.addAction(QIcon(GlobalIcons["NavBar"]['build']), "Build")
        self._conf   = self.addAction(QIcon(GlobalIcons["NavBar"]['conf']), "Config")
        self._plot   = self.addAction(QIcon(GlobalIcons["NavBar"]['plot']), "Plot")
        self._libs   = self.addAction(QIcon(GlobalIcons["NavBar"]['libs']), "Library")
        self._python = self.addAction(QIcon(GlobalIcons["NavBar"]['python']), "Python")
        """

        self._import = self.addAction(qta.icon('mdi.plus', color='black'), "New")
        self._export = self.addAction(qta.icon('mdi.content-save', color='blue'), "Save")
        self._run    = self.addAction(qta.icon('mdi.play-circle', color='green'), "Run")
        self.addSeparator()

        self._charts = self.addAction(qta.icon('mdi.chart-box', color='darkmagenta'), "Charts")
        self._script = self.addAction(qta.icon('mdi.xml', color='darkred'), "Script")
        self._config = self.addAction(qta.icon('mdi.cog', color='gray'), "Settings")