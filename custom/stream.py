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

    # Instance initializer:
    def __init__(self, strid: str, color: QColor | Qt.GlobalColor, units: str | None = None, icon: QIcon | None = None):

        # Store stream-ID and color:
        self._strid = strid
        self._color = color
        self._units = units
        self._icon  = icon      # Placeholder for an icon, if needed

        # Additional user-defined properties:
        self._attr = {
            "strid" : self._strid,  # FlowStream-ID
            "color" : self._color,  # Color of the stream
            "units" : self._units,  # Units of the stream
        }

    # Properties:
    @property # FlowStream-ID (datatype = str): A unique identifier
    def strid(self) -> str: return self._strid

    @property # Color (datatype = QColor): Color of the stream
    def color(self) -> QColor: return QColor(self._color)

    @property # Units (datatype = str): Units of the stream
    def units(self) -> str | None:  return self._units

    @property # Icon (datatype = QPixmap): Icon of the stream
    def icon(self) -> QIcon | None: return self._icon

    @property
    def attr(self) -> dict: return self._attr

    @strid.setter # String-ID setter
    def strid(self, strid): self._strid = strid

    @color.setter # Color setter
    def color(self, color): self._color = color

    @units.setter # Units setter
    def units(self, units: str | None): self._units = units

    @icon.setter # Icon setter
    def icon(self, icon: QIcon | None): self._icon = icon

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

class StreamMenuAction(QWidgetAction):

    # Initializer:
    def __init__(self,
                 stream: Stream,
                 select: bool
                 ):

        # Initialize base-class:
        super().__init__(None)

        # Colored indicator:
        size = 16
        pixmap = QPixmap(size, size)      # Empty pixmap
        pixmap.fill(QColor(0, 0, 0, 0))   # Fill with a transparent background

        # Draw colored circle:
        painter = QPainter(pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(stream.color)
        painter.setPen(QPen(Qt.GlobalColor.black, 0.5))
        painter.drawEllipse(2, 2, size-4, size-4)
        painter.end()

        # Containers:
        self._icon_label = QLabel()
        self._icon_label.setPixmap(pixmap)
        self._icon_label.setFixedWidth(16)
        self._icon_label.setObjectName("Color-indicator")

        # Widget:
        widget = QWidget()
        widget.setFixedHeight(24)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        # Set text-label:
        self._text_label = StreamActionLabel(stream.strid, select, None)

        # Layout items:
        layout.addWidget(self._icon_label)
        layout.addWidget(self._text_label)

        # Add widget to action:
        self.setCheckable(True)
        self.setChecked(select)
        self.setDefaultWidget(widget)

    @property
    def label(self):    return self._text_label.text()
