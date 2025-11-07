# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: search
# Description: A search widget for the Climact application
# ----------------------------------------------------------------------------------------------------------------------

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import QWidget, QLineEdit

from conf import GlobalIcons


class SearchBar(QLineEdit):
    """
    A search bar widget for the Climact application.
    """

    # Default constructor:
    def __init__(self, parent: QWidget | None = None, **kwargs):

        # Invoke base-class constructor:
        super().__init__(parent)
        super().setPlaceholderText(kwargs.get('placeholder', 'Search...'))

        # Set icon:
        self.addAction(
            QIcon(GlobalIcons['SearchBar']),
            QLineEdit.ActionPosition.LeadingPosition
        )