# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: library
# Description: A component library widget for the Climact application
# ----------------------------------------------------------------------------------------------------------------------

from PySide6.QtWidgets import QWidget, QListWidget, QListWidgetItem, QScrollArea, QGridLayout, QLabel, QTextEdit, QFrame

from apps.gemini.widget import Assistant
from obj.search import SearchBar

# Class Library:
class Dashboard(QWidget):

    # Default constructor:
    def __init__(self, parent: QWidget | None = None):

        # Base-class initialization:
        super().__init__(parent)

        # Sub-widgets:
        self._label  = QLabel("Components:", self)
        self._search = SearchBar(self)
        self._scroll = QListWidget(self)
        self._assist = Assistant(self)

        # Layout:
        layout = QGridLayout(self)
        layout.setSpacing(4)
        layout.setContentsMargins(2, 2, 2, 2)

        layout.addWidget(self._label , 0, 0)
        layout.addWidget(self._search, 0, 1)
        layout.addWidget(self._scroll, 1, 0, 1, 2)
        layout.addWidget(QLabel("AI Assistant:", self), 3, 0, 1, 2)
        layout.addWidget(self._assist, 4, 0, 1, 2)