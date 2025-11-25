# Encoding: utf-8
# Module name: switcher
# Description: A tab-switching widget for the Climact application

# -------
# Imports
# PySide6:
from PySide6.QtCore import Qt, QSize, Signal
from PySide6.QtWidgets import QToolBar, QSizePolicy, QWidget, QLabel

import qtawesome as qta

# Navigation pane:
class Navigator(QToolBar):

    # Signal:
    sig_action_triggered = Signal(str)

    # Default constructor:
    def __init__(self, parent: QWidget | None = None, **kwargs):

        # Base-class initialization:
        super().__init__(parent)
        super().setMovable(False)
        super().setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonIconOnly)

        # Set the default icon size:
        self.setIconSize(QSize(23, 23))
        self.setStyleSheet("QToolBar QToolButton {margin: 3px 2px 8px 2px; padding: 1px;}")

        # Expander widget:
        self._wide = QWidget(self)
        self._wide.setStyleSheet("QWidget {background: transparent;}")
        self._wide.setSizePolicy(QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding))

        self._dock = self.addAction(qta.icon('ph.layout-fill', color='#efefef'), 'Dock', lambda: self.sig_action_triggered.emit('Dock'))
        self._dock.setCheckable(True)
        self._dock.setChecked(True)
        self.addSeparator()

        self._open = self.addAction(qta.icon('ph.folder-simple-fill', color = '#ffcb00'), 'Open')
        self._save = self.addAction(qta.icon('ph.floppy-disk-fill', color = 'lightblue'), 'Save')
        self._draw = self.addAction(qta.icon('mdi.hammer-wrench', color='#efefef'), 'Build')
        self._plot = self.addAction(qta.icon('ph.chart-pie-fill', color = '#f07167'), 'Plot')
        self._opts = self.addAction(qta.icon('mdi.function', color = '#efefef'), 'Setup')
        self._play = self.addAction(qta.icon('ph.play-fill', color = '#588157'), 'Run')
        self.addWidget(self._wide)

        # If available, connect the callback function to this toolbar's signal:
        if  kwargs.get('callback'):
            self.sig_action_triggered.connect(kwargs['callback'])