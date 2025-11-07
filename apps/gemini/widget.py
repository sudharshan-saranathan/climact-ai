# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: widget
# Description: GUI widget for interacting with the Gemini AI assistant.
# ----------------------------------------------------------------------------------------------------------------------

# Dependency(s): PySide6, Gemini API, Threading:
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QShortcut, QKeySequence
from PySide6.QtWidgets import (
    QFrame,
    QTextEdit,
    QVBoxLayout,
    QSizePolicy,
    QWidget, QLabel
)

# Class
class Assistant(QWidget):

    # Signal(s):
    sig_get_response = Signal(str)

    # Constructor:
    def __init__(self, parent: QWidget | None = None):

        # Initialize base-class:
        super().__init__(parent)

        # Read-only text script that displays the AI's response:
        self._window = QTextEdit(self)
        self._window.setReadOnly(True)

        # Text-script for querying:
        self._prompt = QTextEdit()
        self._prompt.setFixedHeight(160)
        self._prompt.setPlaceholderText("Type your message or instruction here.")

        # Install a shortcut on the prompt:
        shortcut = QShortcut(QKeySequence("Ctrl+Return"), self._prompt, self._submit_message)
        shortcut.setContext(Qt.ShortcutContext.WidgetWithChildrenShortcut)

        # Layout to arrange child-widgets:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)

        # Add editors to the layout:
        layout.addWidget(self._window)
        layout.addWidget(self._prompt)

    # Method to emit a signal:
    def _submit_message(self) -> None:
        """
        Emit a signal to request a response from the AI assistant.
        :return: None
        """

        if  message := self._prompt.toPlainText():
            self.sig_get_response.emit(message)
            self._prompt.clear()
