#-----------------------------------------------------------------------------------------------------------------------
# Author    : Sudharshan Saranathan
# GitHub    : https://github.com/sudharshan-saranathan/climact
# Module(s) : PyQt6 (version 6.8.1), Google-AI (Gemini)
#-----------------------------------------------------------------------------------------------------------------------

from PyQt6.QtGui     import QIcon, QActionGroup, QAction
from PyQt6.QtCore    import Qt, QSize, pyqtSignal
from PyQt6.QtWidgets import QWidget, QToolBar, QApplication

import qtawesome as qta
import logging

class NavBar(QToolBar):

    # Signals:
    sig_open_schema = pyqtSignal()      # Emitted when the user clicks the "Open" action
    sig_save_schema = pyqtSignal()      # Emitted when the user clicks the "Save" action
    sig_show_widget = pyqtSignal(str)   # Emitted when the user clicks one of the icons in the navbar

    # Initializer:
    def __init__(self, parent: QWidget | None):

        # Initialize base-class:
        super().__init__(parent)

        # Adjust width:
        self.setMovable(False)
        self.setIconSize(QSize(20, 20))
        self.setOrientation(Qt.Orientation.Vertical)
        self.setStyleSheet("QToolBar QToolButton {margin: 2px 4px 4px 4px;}")

        self._open = self.addAction(qta.icon('ph.folder-simple-fill', color = '#ffcb00'), 'Open')
        self._save = self.addAction(qta.icon('ph.floppy-disk-fill', color = 'lightblue'), 'Save')
        self._site = self.addAction(qta.icon('mdi.sitemap', color = 'red'), 'Canvas')
        self._data = self.addAction(qta.icon('mdi.microsoft-excel', color = 'lightgreen'), 'Sheets')
        self._plot = self.addAction(qta.icon('ph.chart-pie-fill', color = '#f07167'), 'Charts')
        self._opts = self.addAction(qta.icon('mdi.function', color = '#efefef'), 'Script')
        self._play = self.addAction(qta.icon('ph.play-fill', color = '#588157'), 'Optima')
        self._chat = self.addAction(qta.icon('mdi.robot-excited', color='#efefef'), 'Assistant')

        # Save actions in a list for easy access:
        self._actions = [
            self._site,
            self._data,
            self._play,
        ]

        # Make canvas, sheets, script, and config checkable:
        self._site.setCheckable(True)
        self._data.setCheckable(True)
        self._play.setCheckable(True)
        self._chat.setCheckable(True)
        self._site.setChecked(True)

        # Create an action group and toggle exclusivity:
        _action_group = QActionGroup(self)
        _action_group.addAction(self._site)
        _action_group.addAction(self._data)
        _action_group.addAction(self._play)
        _action_group.setExclusive(True)

        # Connect action-signals:
        self._open.triggered.connect(lambda: self.sig_open_schema.emit())
        self._save.triggered.connect(lambda: self.sig_save_schema.emit())
        self._site.triggered.connect(lambda: self.sig_show_widget.emit(self._site.text()))
        self._data.triggered.connect(lambda: self.sig_show_widget.emit(self._data.text()))
        self._play.triggered.connect(lambda: self.sig_show_widget.emit(self._play.text()))
        self._chat.triggered.connect(lambda: self.sig_show_widget.emit(self._chat.text()))

    # Activate a specific action by name:
    def select_action(self, action_name: str):
        """
        Activates a specific action by its name.
        """
        for action in self._actions:
            if action.text() == action_name:
                action.trigger()
                return

        logging.warning(f"Action '{action_name}' not found in the navigation bar.")