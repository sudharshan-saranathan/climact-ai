# Encoding: utf-8
# Module name: switcher
# Description: A tab-switching widget for the Climact application

# -------
# Imports
# PySide6:
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QToolBar, QSizePolicy, QWidget, QLabel

import qtawesome as qta

from opts import GlobalConfig


# Navigation pane:
class ToolBar(QToolBar):

    # Signal:
    sig_action_triggered = Signal(str)

    # Default constructor:
    def __init__(
            self,
            parent: QWidget | None = None,
            **kwargs
    ):

        # Base-class initialization:
        super().__init__(parent)
        super().setMovable(False)
        super().setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        # Set the default icon size:
        self.setIconSize(QSize(24, 24))

        # Expander widget:
        self._wide = QWidget()
        self._wide.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        self._open = self.addAction(qta.icon('ph.plus', color = '#efefef'), 'New')
        self._save = self.addAction(qta.icon('ph.floppy-disk', color = '#efefef'), 'Save')
        self._play = self.addAction(qta.icon('ph.play', color = '#efefef'), 'Run')
        self._plot = self.addAction(qta.icon('ph.chart-line-up', color = '#efefef'), 'Plot')
        self._opts = self.addAction(qta.icon('mdi.function', color = '#efefef'), 'Solve')
        self.addSeparator()

        self._undo  = self.addAction(qta.icon('ph.arrow-u-up-left' , color = '#efefef'), 'Undo')
        self._redo  = self.addAction(qta.icon('ph.arrow-u-up-right', color = '#efefef'), 'Redo')
        self._clone = self.addAction(qta.icon('fa5.clone', color = '#efefef'), 'Clone')
        self._paste = self.addAction(qta.icon('ph.clipboard', color = '#efefef'), 'Paste')
        self.addSeparator()

        self._reset = self.addAction(qta.icon('ph.arrow-counter-clockwise', color = 'red'), 'Reset')
        self._templ = self.addAction(qta.icon('mdi.library', color = '#efefef'), 'Templates')
        self.addWidget(self._wide)

        self._conf = self.addAction(qta.icon('mdi.cog', color = 'gray'), 'Settings')
        self._help = self.addAction(qta.icon('mdi.help-circle', color = 'lightgray'), 'Help')

        # If available, connect the callback function to this toolbar's signal:
        if  kwargs.get('callback'):
            self.sig_action_triggered.connect(kwargs['callback'])