# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: vector
# Description: A QGraphicsObject-based stream for the Climact application that represents a connection between two
#              handles in a schematic. The stream is drawn as a curved path with an arrow indicating the direction
#              of flow from the origin handle to the target handle.
# ----------------------------------------------------------------------------------------------------------------------

# Numpy for trigonometric functions:
import numpy as np

# Dependency: PySide6
from PySide6.QtGui import QPen, QPainterPath, QPainter, QPainterPathStroker, QBrush, QColor, QFont
from PySide6.QtCore import Qt, QRectF, QPointF, QSizeF, QSize, Property, QEasingCurve, QPropertyAnimation
from PySide6.QtWidgets import QGraphicsObject, QGraphicsSceneHoverEvent

# Climact-ai sub-module(s):
from conf import GlobalConfig
from obj.svgicon import SvgIcon

# Default vector options:
VectorOpts = {

    "shape" : {
        'boundary-rectangle': QRectF(-2, -2, 4, 4)
    },

    "stroke" : {
        'color': {
            'normal': Qt.GlobalColor.darkGray,
            'select': QColor(0xf3a738)
        },
        'width': 1.5,
        'style': Qt.PenStyle.SolidLine,
    },

    "offset": 32,
    "radius": 4
}

# Class Vector: A graphical stream connecting two handles in a schematic.
class Vector(QGraphicsObject):

    # Constructor:
    def __init__(self, parent: QGraphicsObject | None = None, **kwargs):

        # Initialize the base class:
        super().__init__(parent)
        super().setAcceptHoverEvents(True)
        super().setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsSelectable)

        # Set properties:
        self.setProperty('stroke', VectorOpts['stroke'])

        # Initialize class-level attributes:
        self._route = QPainterPath()
        self._arrow = SvgIcon(GlobalConfig["root"] + "/rss/icons/arrow.svg", self, size = QSize(16, 16))

        # Animation:
        self._animation = QPropertyAnimation(self, b"thickness")
        self._animation.setEasingCurve(QEasingCurve.Type.OutCubic)
        self._animation.setDuration(360)

        # Store reference(s) to the origin and target handles:
        self.origin = kwargs.get("origin", None)
        self.target = kwargs.get("target", None)
        self.setZValue(-1)

        # If origin and target handles are provided, connect them:
        if  self.origin and self.target:

            self.origin.paired = True, self, self.target
            self.target.paired = True, self, self.origin
            self.on_path_updated()

    # Reimplementation of QGraphicsObject.boundingRect():
    def boundingRect(self) -> QRectF:   return self._route.boundingRect().adjusted(-4, -4, 4, 4)

    # Reimplementation of QGraphicsObject.paint():
    def paint(self, painter: QPainter, option, widget=None):
        """
        Paints the connector's path onto the canvas.
        :param painter:
        :param option:
        :param widget:
        :return:
        """

        color = self.property('stroke')['color']['select'] if self.isSelected() else self.property('stroke')['color']['normal']
        width = self.property('stroke')['width']
        style = self.property('stroke')['style']

        painter.setPen(QPen(color, width, style))
        painter.drawPath(self._route)

        # Draw the origin's label:
        if  self.origin:

            path = QPainterPath(self.origin.scenePos() + QPointF(6, 2.0))
            path.addText(path.currentPosition(), QFont('Fira Sans', 7), self.origin.property('label'))

            painter.setPen(QPen(Qt.GlobalColor.white, 4.0))
            painter.drawPath(path)

            painter.setPen(QPen(color, 0.25))
            painter.drawPath(path)
            painter.fillPath(path, QBrush(color))

    # Reimplementation of QGraphicsObject.shape():
    def shape(self):

        stroker = QPainterPathStroker()
        stroker.setWidth(8.0)
        return stroker.createStroke(self._route)

    # Reimplementation of QGraphicsObject.hoverEnterEvent():
    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent):
        super().hoverEnterEvent(event)
        super().setCursor(Qt.CursorShape.ArrowCursor)

        # Animate:
        self._animation.setStartValue(VectorOpts['stroke']['width'])
        self._animation.setEndValue(VectorOpts['stroke']['width'] + 1.0)
        self._animation.start()

    # Reimplementation of QGraphicsObject.hoverEnterEvent():
    def hoverLeaveEvent(self, event, /):
        super().hoverLeaveEvent(event)
        super().unsetCursor()

        # Animate:
        self._animation.setStartValue(VectorOpts['stroke']['width'] + 1.0)
        self._animation.setEndValue(VectorOpts['stroke']['width'])
        self._animation.start()

    # ------------------------------------------------------------------------------------------------------------------
    # Callback function(s) for user-driven events

    # Update the path when the origin or target handle is moved:
    def on_path_updated(self, opos: QPointF = QPointF(), tpos: QPointF = QPointF()):
        """
        Redraws the connection between the origin and target coordinates.
        :param opos: The coordinate of the origin-handle (default: None)
        :param tpos: The coordinate of the target-handle (default: None)
        """

        opos = opos or self.origin.scenePos()
        tpos = tpos or self.target.scenePos()

        # Next, construct the path:
        if  opos.x() <= tpos.x() - 2 * VectorOpts['offset']:
            self._route = self.segment(opos, tpos)
            self._arrow.setPos(self._route.pointAtPercent(0.5))
            self._arrow.setRotation(np.degrees(np.arctan(self._route.slopeAtPercent(0.5))))

        else:
            self._route = self.loopback(opos, tpos)
            self._arrow.setPos(self._route.pointAtPercent(0.5))
            self._arrow.setRotation(180)

        # Update the canvas:
        if  self.scene():
            self.scene().update(self.scene().visible_region())

    # Constructs the stream path from origin to target:
    @staticmethod
    def segment(opos: QPointF, tpos: QPointF):
        """
        Constructs the stream path from origin to target.
        :param opos: Origin point of the stream.
        :param tpos: Target point of the stream.
        :return: QPainterPath: The constructed path from origin to target.
        """

        opos += QPointF(VectorOpts['offset'], 0)
        tpos -= QPointF(VectorOpts['offset'], 0)

        if  tpos.y() != opos.y():   angle = 0.75 * np.arctan(np.abs(tpos.x() - opos.x()) / np.abs(tpos.y() - opos.y()))
        else:                       angle = np.pi / 2.0

        theta = angle if tpos.y() > opos.y() else np.pi - angle
        xm  = 0.50 * (opos.x() + tpos.x())
        xd  = np.tan(theta) * (tpos.y() - opos.y()) / 2.0
        rad = min(0.50 * np.abs(tpos.y() - opos.y()), VectorOpts['radius'])

        # If the origin is to the left of the target, draw the path accordingly:
        path = QPainterPath()
        path.moveTo(opos - QPointF(VectorOpts['offset'], 0))
        path.lineTo(opos)

        path.lineTo(xm - xd - rad, opos.y())
        path.quadTo(xm - xd, opos.y(), xm - xd + rad * np.sin(theta), opos.y() + rad * np.cos(theta))
        path.lineTo(xm + xd - rad * np.sin(theta), tpos.y() - rad * np.cos(theta))
        path.quadTo(xm + xd, tpos.y(), xm + xd + rad, tpos.y())

        path.lineTo(tpos)
        path.lineTo(tpos + QPointF(VectorOpts['offset'], 0))

        return path

    # Loop-back path:
    @staticmethod
    def loopback(opos: QPointF, tpos: QPointF):
        """
        Constructs a loop-back path from origin to target.
        :param opos:
        :param tpos:
        :return:
        """

        opos += QPointF(VectorOpts['offset'], 0)
        tpos -= QPointF(VectorOpts['offset'], 0)
        diff  = tpos - opos

        path = QPainterPath()
        mid  = QPointF(0.5 * opos.x(), 0.5 * opos.y()) + QPointF(0.5 * tpos.x(), 0.5 * tpos.y())
        rad  = min(0.50 * np.abs(diff.y()), VectorOpts['radius'])

        path.moveTo(opos - QPointF(VectorOpts['offset'], 0))
        path.lineTo(opos - QPointF(rad, 0))

        if  tpos.y() > opos.y():

            path.arcTo(QRectF(opos - QPointF(2 * rad, 0), QSizeF(2 * rad, 2 * rad)), 90, -90)
            path.lineTo(opos.x(), mid.y() - rad)
            path.arcTo(QRectF(opos.x() - 2*rad, mid.y() - 2*rad, 2 * rad, 2 * rad), 0, -90)
            path.lineTo(tpos.x() + rad, mid.y())
            path.arcTo(QRectF(tpos.x(), mid.y(), 2 * rad, 2 * rad), 90, 90)
            path.lineTo(tpos.x(), tpos.y() - 2 * rad)
            path.arcTo(QRectF(tpos.x(), tpos.y() - 2 * rad, 2 * rad, 2 * rad), 180, 90)
            path.lineTo(tpos + QPointF(VectorOpts['offset'], 0))

        else:
            path.arcTo(QRectF(opos - QPointF(2 * rad, 2 * rad), QSizeF(2 * rad, 2 * rad)), 270, 90)
            path.lineTo(opos.x(), mid.y() + rad)
            path.arcTo(QRectF(opos.x() - 2 * rad, mid.y(), 2 * rad, 2 * rad), 0, 90)
            path.lineTo(tpos.x() + rad, mid.y())
            path.arcTo(QRectF(tpos.x(), mid.y() - 2 * rad, 2 * rad, 2 * rad), 270, -90)
            path.lineTo(tpos.x(), tpos.y() + 2 * rad)
            path.arcTo(QRectF(tpos.x(), tpos.y(), 2 * rad, 2 * rad), 180, -90)
            path.lineTo(tpos + QPointF(VectorOpts['offset'], 0))

        return path

    # Reset the path and hide the item:
    def clear(self):

        self._route.clear()
        self._arrow.setPos(QPointF())

        # Update the scene to prevent visual artifacts:
        if  self.scene(): self.scene().update(self.scene().visible_region())

    # ------------------------------------------------------------------------------------------------------------------
    # Property accessors and mutators:

    def get_thickness(self) -> float:   return self.property('stroke')['width']

    def set_thickness(self, value: float) -> None:

        stroke = self.property('stroke')
        stroke['width'] = value

        self.setProperty('stroke', stroke)
        self.update()

    # Declare thickness as a property:
    thickness = Property(float, get_thickness, set_thickness)