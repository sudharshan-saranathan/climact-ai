# Encoding: utf-8
# Module name: anchor
# Description: Transparent rails on which input and output handles to a vertex can be anchored.

# PySide6:
from PySide6.QtCore import (
    Qt,
    QRectF,
    QPointF,
    Signal
)
from PySide6.QtGui import (
    QPen,
    QBrush,
    QColor
)
from PySide6.QtWidgets import QGraphicsObject, QGraphicsEllipseItem

# Default config:
AnchorOpts = {
    'frame': QRectF(-2.0, -15, 4, 35),
    'curve': 0,
    'style': {
        'color': QPen  (Qt.GlobalColor.transparent),
        'brush': QBrush(Qt.GlobalColor.transparent),
    }
}

# Class Anchor:
class Anchor(QGraphicsObject):

    # Signals:
    sig_anchor_clicked = Signal(QPointF)

    # Class constructor:
    def __init__(self, parent: QGraphicsObject | None = None, **kwargs):

        # Base-class initialization:
        super().__init__(parent)
        super().setAcceptHoverEvents(True)

        # Set attribute(s):
        self.setProperty('cpos', kwargs.get('cpos', QPointF(0, 0)))
        self.setProperty('frame', kwargs.get('frame', AnchorOpts['frame']))
        self.setProperty('curve', kwargs.get('curve', AnchorOpts['curve']))
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
        return self.property('frame')

    # Reimplementation of QGraphicsObject.paint(...):
    def paint(self, painter, option, widget = ...):

        # Customize painter:
        painter.setPen(self.property('style')['color'])
        painter.setBrush(self.property('style')['brush'])
        painter.drawRoundedRect(
            self.boundingRect().adjusted(0.5, 0, -0.5, 0),
            self.property('curve'),
            self.property('curve')
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