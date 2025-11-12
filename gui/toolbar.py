# Encoding: utf-8
# Module name: switcher
# Description: A tab-switching widget for the Climact application

# -------
# Imports
# PySide6:
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtWidgets import QToolBar, QSizePolicy, QWidget


import qtawesome as qta

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
        super().setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextUnderIcon)

        # Set the default icon size:
        self.setIconSize(QSize(24, 24))

        # Expander widget:
        self._wide = QWidget()
        self._wide.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        # Home and sidebar:
        self._home = self.addAction(qta.icon('mdi.home-account', color='lightgray'), 'Home', lambda: self.sig_action_triggered.emit('home'))
        self._pane = self.addAction(qta.icon('mdi.view-dashboard', color='lightgray'), 'Pane', lambda: self.sig_action_triggered.emit('Pane'))
        self._pane.setCheckable(True)
        self._pane.setChecked(True)
        self.addSeparator()

        self._open = self.addAction(qta.icon('mdi.folder-open', color = 'red'), 'Open')
        self._save = self.addAction(qta.icon('mdi.content-save', color = 'blue'), 'Save')
        self._play = self.addAction(qta.icon('mdi.play-circle', color = 'lightgreen'), 'Run')
        self._plot = self.addAction(qta.icon('mdi.chart-box', color = 'lightpink'), 'Plot')
        self._opts = self.addAction(qta.icon('mdi.language-python', color = 'orange'), 'Opt')
        self.addSeparator()

        self._undo  = self.addAction(qta.icon('mdi.undo', color = 'yellow'), 'Undo')
        self._redo  = self.addAction(qta.icon('mdi.redo', color = 'yellow'), 'Redo')
        self._clone = self.addAction(qta.icon('fa5.clone', color = 'green'), 'Clone')
        self._paste = self.addAction(qta.icon('ph.clipboard-fill', color = 'lightblue'), 'Paste')
        self.addSeparator()

        self._reset = self.addAction(qta.icon('mdi.refresh', color = 'red'), 'Reset')
        self._templ = self.addAction(qta.icon('mdi.library', color = 'lightcyan'), 'Templates')
        self.addWidget(self._wide)

        self._conf = self.addAction(qta.icon('mdi.cog', color = 'black'), 'Settings')
        self._help = self.addAction(qta.icon('mdi.help-circle', color = 'lightgray'), 'Help')

        # If available, connect the callback function to this toolbar's signal:
        if  kwargs.get('callback'):
            self.sig_action_triggered.connect(kwargs['callback'])