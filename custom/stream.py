from PyQt6.QtCore   import Qt
from PyQt6.QtGui    import QPen, QIcon, QColor

from PyQt6.QtWidgets import (
    QWidgetAction,
    QWidget,
    QHBoxLayout,
    QLabel,
)

from PyQt6.QtGui  import QPainter, QPixmap
from PyQt6.QtCore import pyqtSignal

# Class Stream:
class Stream:

    # Constructor:
    def __init__(self,
                 strid: str,
                 color: QColor,
                 icon: QIcon = QIcon(),
                 **kwargs):

        # Store attributes:
        self._strid = strid
        self._color = color
        self._icon  = icon

        self._constant_attr = {key: value for key, value in kwargs.items()}
        self._variable_attr = {}

    # Set a custom attribute:
    def set_attr(self, key: str, value: str | int | float | bool):
        self._variable_attr[key] = value

    # Properties:
    @property # FlowStream-ID (datatype = str): A unique identifier
    def strid(self) -> str: return self._strid

    @property # Color (datatype = QColor): Color of the stream
    def color(self) -> QColor: return QColor(self._color)

    @property # Icon (datatype = QPixmap): Icon of the stream
    def icon(self) -> QIcon: return self._icon

    @property
    def constant_attr(self) -> dict: return self._constant_attr

    @property
    def variable_attr(self) -> dict: return self._variable_attr

    @strid.setter # String-ID setter
    def strid(self, strid): self._strid = strid

    @color.setter # Color setter
    def color(self, color): self._color = color

class StreamActionLabel(QLabel):

    # Signals:
    sig_label_hovered = pyqtSignal()

    # Initializer:
    def __init__(self,
                 label: str,
                 select: bool,
                 parent: QWidget | None
                 ):
        """
        Initialize a category label.
        """

        # If selected, make the label bold:
        label = f"<b>{label}</b>" if select else label

        # Initialize base-class:
        super().__init__(label, parent)

        # Customize:
        self.setIndent(4)
        self.setStyleSheet("QLabel {border-radius: 6px; color: black;}")

    # Handles enterEvent:
    def enterEvent(self, _event):   self.setStyleSheet("QLabel {background: #e0e0e0; color: #187795;}")

    # Handles leaveEvent:
    def leaveEvent(self, _event):   self.setStyleSheet("QLabel {background: transparent; color: black;}")