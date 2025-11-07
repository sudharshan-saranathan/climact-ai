# Encoding: utf-8
# Module name: switcher
# Description: A tab-switching widget for the Climact application

# -------
# Imports
# PySide6: `pip install PySide6`
from PySide6.QtCore import Qt, QSize
from PySide6.QtWidgets import QToolBar, QWidget, QSizePolicy

# QtAwesome: `pip install qtawesome`
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

        # Define an expander widget:
        self._expander = QWidget(self)
        self._expander.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        # Install tool-buttons:
        self._home   = self.addAction(qta.icon('mdi.home-account', color='#CEEC97'), 'Home')
        self.addSeparator()

        self._new  = self.addAction(qta.icon('mdi.plus', color='#E0C879'), "New")
        self._run  = self.addAction(qta.icon('mdi.play-box', color='lightgreen'), "Run")
        self._save = self.addAction(qta.icon('mdi.content-save', color='lightblue'), "Save")
        self.addSeparator()

        self._clone = self.addAction(qta.icon('ph.copy-simple-fill', color='cyan'), 'Clone')
        self._paste = self.addAction(qta.icon('ph.clipboard-fill', color='cyan'), 'Paste')
        self._undo  = self.addAction(qta.icon('mdi.undo', color='lightpink'), "Undo")
        self._redo  = self.addAction(qta.icon('mdi.redo', color='lightpink'), "Redo")

        self.addWidget(self._expander)
        self._charts = self.addAction(qta.icon('mdi.chart-box', color='yellow'), "Charts")
        self._script = self.addAction(qta.icon('mdi.xml', color='red'), "Script")
        self._config = self.addAction(qta.icon('mdi.cog', color='lightgray'), "Settings")
        self._help   = self.addAction(qta.icon('mdi.help-box', color='gray'), "Help")