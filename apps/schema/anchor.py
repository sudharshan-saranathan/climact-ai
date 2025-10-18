# Encoding: utf-8
# Module name: anchor
# Description: Transparent rails on which input and output handles to a vertex can be anchored.

# PySide6:
from PySide6.QtCore import (
    Qt,
    QRectF,
    QPointF,
    Signal, Property
)
from PySide6.QtGui import (
    QPen,
    QBrush,
    QColor
)
from PySide6.QtWidgets import QGraphicsObject, QGraphicsEllipseItem

# Default config:
AnchorOpts = {
    'frame': QRectF(-0.25, -15, 0.50, 35),
    'round': 0,
    'style': {
        'color': QPen  (Qt.GlobalColor.transparent),
        'brush': QBrush(Qt.GlobalColor.white),
    }
}

# Class Anchor:
class Anchor(QGraphicsObject):

    # Signals:
    sig_anchor_clicked = Signal(QPointF)

    # Class constructor:
    def __init__(self, role: int, parent: QGraphicsObject | None = None, **kwargs):

        # Base-class initialization:
        super().__init__(parent)
        super().setAcceptHoverEvents(True)

        # Set attribute(s):
        self.setProperty('role' , role)
        self.setProperty('cpos' , kwargs.get('cpos', QPointF(0, 0)))
        self.setProperty('frame', kwargs.get('frame', AnchorOpts['frame']))
        self.setProperty('round', kwargs.get('round', AnchorOpts['round']))
        self.setProperty('style', kwargs.get('style', AnchorOpts['style']))

        # Child item(s):
        self._hint = QGraphicsEllipseItem(QRectF(-1.5, -1.5, 3, 3), parent = self)
        self._hint.setPen(QPen(Qt.GlobalColor.black, 0.50))
        self._hint.setBrush(QBrush(QColor(0xb4f7d2)))
        self._hint.hide()

        # Position the anchor:
        self.setPos(self.property('cpos'))

        # Hook onto callbacks:
        if  kwargs.get('callback', None):
            self.sig_anchor_clicked.connect(kwargs.get('callback'), Qt.ConnectionType.UniqueConnection)

    # Reimplementation of QGraphicsObject.boundingRect(...):
    def boundingRect(self):
        return self.property('frame').adjusted(-2, 0, 2, 0)

    # Reimplementation of QGraphicsObject.paint(...):
    def paint(self, painter, option, widget = ...):

        # Customize painter:
        painter.setPen(self.property('style')['color'])
        painter.setBrush(self.property('style')['brush'])
        painter.drawRoundedRect(
            self.property('frame'),
            self.property('round'),
            self.property('round')
        )

    # Reimplementation of QGraphicsObject.hoverEnterEvent(...):
    def hoverEnterEvent(self, event, /):

        # Base-class implementation:
        super().hoverEnterEvent(event)

        # Show the handle-hint:
        self.setCursor(Qt.CursorShape.ArrowCursor)
        self._hint.setY(event.pos().y())
        self._hint.show()

    # Reimplementation of QGraphicsObject.hoverMoveEvent(...):
    def hoverMoveEvent(self, event, /):

        super().hoverMoveEvent(event)
        self._hint.setY(event.pos().y())

    # Reimplementation of QGraphicsObject.hoverEnterEvent(...):
    def hoverLeaveEvent(self, event, /):

        # Hide the handle-hint:
        self._hint.setY(event.pos().y())
        self._hint.hide()
        self.unsetCursor()

        # Base-class implementation:
        super().hoverLeaveEvent(event)

    # Reimplementation of QGraphicsObject.mousePressEvent(...):
    def mousePressEvent(self, event, /):
        self.sig_anchor_clicked.emit(QPointF(0, event.pos().y()))

    # ----------------
    # Utility methods:
    # ----------------

    # Resize the anchor:
    def resize(self, bottom: float, /):

        rect = self.property('frame')
        rect.setBottom(bottom)

        self.setProperty('frame', rect)

    # ------------------------------------------------------------------------------------------------------------------
    # Property getter(s) and setter(s):

    @Property(int)
    def role(self):
        return self.property('role')

    @role.setter
    def role(self, value):  pass