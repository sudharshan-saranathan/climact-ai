# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: chat
# Description: A widget to type queries and fetch responses from Gemini AI models.
# ----------------------------------------------------------------------------------------------------------------------

# Import(s):
# PySide6
from PySide6 import QtWidgets, QtCore

import qtawesome as qta

class Chat(QtWidgets.QWidget):

    # Default constructor:
    def __init__(self, parent: QtWidgets.QWidget | None = None):

        # Base-class initialization:
        super().__init__(parent)

        # Response display:
        self._display = QtWidgets.QTextEdit(self)
        self._display.setReadOnly(True)
        self._display.setPlaceholderText("Hello! I'm an AI assistant. How can I help you today?")
        self._display.setStyleSheet('QTextEdit { '
                                    'background: #3a4043;'
                                    '}')

        # Input field:
        self._message = QtWidgets.QTextEdit(self)
        self._message.setPlaceholderText("Type query, press <Ctrl+Enter> to send.")
        self._message.setFixedHeight(240)


        # Spacer widget:
        self._spacers = QtWidgets.QWidget(self)
        self._spacers.setStyleSheet('QWidget { background: transparent; }')
        self._spacers.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        # AI-model selector:
        self._models = QtWidgets.QComboBox(self)
        self._models.addItems(['Gemini-2.5-Flash', 'Gemini-2.5-Pro'])
        self._models.setCurrentIndex(0)
        self._models.setFixedWidth(160)

        # Options-bar:
        self._options = QtWidgets.QToolBar(self)
        self._options.setIconSize(QtCore.QSize(18, 18))
        self._options.setStyleSheet('QToolBar { background: transparent; padding: 0px;}')
        self._options.addWidget(self._models)
        self._options.addWidget(self._spacers)

        self._history = self._options.addAction(qta.icon('ph.clock-counter-clockwise', color='#efefef'), "Chat History")
        self._speak   = self._options.addAction(qta.icon('ph.microphone', color='#efefef'), "Speak Message")
        self._attach  = self._options.addAction(qta.icon('ph.paperclip', color='#efefef'), "Attach File")
        self._send    = self._options.addAction(qta.icon('ph.paper-plane-right-fill', color='#ffcb00'), "Send Message")

        # Layout:
        self._layout = QtWidgets.QVBoxLayout(self)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.setSpacing(1)
        self._layout.addWidget(self._display)
        self._layout.addWidget(self._message)
        self._layout.addWidget(self._options)
