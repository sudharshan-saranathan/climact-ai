# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: search
# Description: A generic search utility for the Climact application
# ----------------------------------------------------------------------------------------------------------------------
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLineEdit, QWidget, QProxyStyle, QStyle, QTextEdit

import qtawesome as qta

class ThickCursorStyle(QProxyStyle):

    # Override the pixelMetric method to customize cursor width:
    def pixelMetric(self, metric, option=None, widget=None):

        return (
            8 if metric == QStyle.PixelMetric.PM_TextCursorWidth
            else super().pixelMetric(metric, option, widget)
        )

class Search(QTextEdit):

    # Default constructor:
    def __init__(self, parent: QWidget | None = None, **kwargs):

        # Base-class initialization:
        super().__init__(parent)
        super().setCursor(Qt.CursorShape.BlankCursor)

        # Set placeholder text:
        self.setPlaceholderText(kwargs.get('placeholder', 'Type to search'))
        self.setStyle(ThickCursorStyle())
        self.setMaximumHeight(240)

        # Set search icon at the leading position:
        # self.addAction(
        #     qta.icon(
        #         'mdi.magnify',
        #         color='black'
        #     ),
        #     QLineEdit.ActionPosition.LeadingPosition
        # )

        # Connect the returnPressed signal to the callback:
        # if  kwargs.get('callback', None):   self.returnPressed.connect(kwargs['callback'])
