# Encoding: utf-8
# Module name: handle
# Description: Connection end points for vertices.

# Import(s):
# Standard module(s):
import types

# PySide6:
from PySide6.QtCore import Qt, QRectF, QPointF, QSize, Property, QEasingCurve, QPropertyAnimation, Signal
from PySide6.QtGui import QPen, QColor, QBrush
from PySide6.QtWidgets import QGraphicsObject

from conf import GlobalConfig
from obj import SvgIcon

# Default configuration for handles:
HandleConfig = {
    'frame': QRectF(-1.5, -1.5, 3, 3),
    'color': 0xb4f7d2,
}

# Class Handle:
class Handle(QGraphicsObject):

    # Signals:
    sig_handle_clicked = Signal(QGraphicsObject)

    # Class constructor:
    def __init__(self, parent: QGraphicsObject | None = None, **kwargs):

        # Base-class initialization:
        super().__init__(parent)

        # Set attribute(s):
        self.setProperty('frame', kwargs.get('frame', HandleConfig['frame']))
        self.setProperty('color', kwargs.get('color', HandleConfig['color']))
        self.setProperty('cpos' , kwargs.get('cpos', QPointF(0, 0)))
        self.setPos(self.property('cpos'))

        # Animation properties:
        self._hint = False
        self._anim = QPropertyAnimation(self, b"radius")
        self._anim.setEasingCurve(QEasingCurve.Type.OutQuad)
        self._anim.setDuration(360)

        # Handle's icon:
        self._icon = SvgIcon(GlobalConfig['root'] + "/rss/icons/default.svg", parent = self, size = QSize(8, 8))
        self._icon.setPos(QPointF(-8, 0) if self.property('cpos').x() >= 0 else QPointF(8, 0))

        # Instantiate connection state:
        self._state = types.SimpleNamespace(
            connected = False,
            connector = None,
            conjugate = None
        )

        # Hook onto the callback function (if provided):
        if  kwargs.get('callback', None):
            self.sig_handle_clicked.connect(kwargs.get('callback'))

        # Set flags and attribute(s):
        super().setAcceptHoverEvents(True)
        super().setFlag(QGraphicsObject.GraphicsItemFlag.ItemSendsScenePositionChanges)

    # Reimplementation of QGraphicsObject.boundingRect():
    def boundingRect(self, /):  return self.property('frame').adjusted(-6, -6, 6, 6)

    # Reimplementation of QGraphicsObject.paint():
    def paint(self, painter, option, widget = ...):

        painter.setPen(QPen(QColor(Qt.GlobalColor.black), 0.50))
        painter.setBrush(QBrush(QColor(self.property('color'))))
        painter.drawEllipse(self.property('frame'))

        if  self._hint:
            painter.setBrush(QBrush(QColor(Qt.GlobalColor.black)))
            painter.drawEllipse(HandleConfig['frame'].adjusted(0.75, 0.75, -0.75, -0.75))

    # Reimplementation of QGraphicsObject.itemChange():
    def itemChange(self, change, value, /):

        if  change == QGraphicsObject.GraphicsItemChange.ItemScenePositionHasChanged:
            if  self._state.connected:
                self._state.connector.on_path_updated()

        return super().itemChange(change, value)

    # ------------------------------------------------------------------------------------------------------------------
    # Reimplementation of QGraphicsObject event-handling methods for Qt events:

    # Reimplementation of QGraphicsObject.hoverEnterEvent():
    def hoverEnterEvent(self, event, /):

        super().hoverEnterEvent(event)
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self._anim.setStartValue(HandleConfig['frame'].width() / 2)
        self._anim.setEndValue(HandleConfig['frame'].width() / 2 + 0.5)
        self._anim.start()
        self._hint = True

    # Reimplementation of QGraphicsObject.hoverLeaveEvent():
    def hoverLeaveEvent(self, event, /):

        super().hoverLeaveEvent(event)
        self.unsetCursor()
        self._anim.setStartValue(HandleConfig['frame'].width() / 2 + 0.5)
        self._anim.setEndValue(HandleConfig['frame'].width() / 2)
        self._anim.start()
        self._hint = False

    # Reimplementation of QGraphicsObject.mousePressEvent():
    def mousePressEvent(self, event, /):

        # Clear the scene's selection:
        if  self.scene():
            self.scene().clearSelection()

        if  not self._state.connected:
            self.sig_handle_clicked.emit(self)

        else:
            event.accept()
            super().setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsMovable)
            super().mousePressEvent(event)

    # Reimplementation of QGraphicsObject.mouseReleaseEvent():
    def mouseReleaseEvent(self, event, /):

        # Ensure that the handle's x-position is locked:
        super().setX(self.property('cpos').x())
        super().setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsMovable, False)
        super().mouseReleaseEvent(event)

    # ------------------------------------------------------------------------------------------------------------------
    # Callback function(s) for user-driven events:

    # When the user connects this handle to another:
    def pair(self, connector: QGraphicsObject, conjugate: 'Handle') -> None:

        self._state.connected = True
        self._state.connector = connector
        self._state.conjugate = conjugate

    # When the user disconnects this handle from another:
    def unpair(self) -> None:

        self._state.connected = False
        self._state.connector = None
        self._state.conjugate = None

    # ------------------------------------------------------------------------------------------------------------------
    # Property accessors:

    # Get the radius of the handle:
    def get_radius(self) -> float:
        return float(self.property("frame").width() / 2)

    # Set the radius of the handle:
    def set_radius(self, radius: float) -> None:
        self.setProperty("frame", QRectF(-radius, -radius, radius * 2, radius * 2))
        self.update()

    # Declare radius as a property:
    radius = Property(float, get_radius, set_radius)