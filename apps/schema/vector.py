# Encoding: utf-8
# Module name: vector
# Description: A QGraphicsObject-based stream/connector that represents a directional connection between two handles.

# Import(s):
# Standard module(s):
import numpy as np

# PySide6
from PySide6.QtGui import QPen, QPainterPath, QPainter, QPainterPathStroker, QFont, QColor
from PySide6.QtCore import Qt, QRectF, QPointF, QSizeF, QSize
from PySide6.QtWidgets import QGraphicsObject, QGraphicsSceneHoverEvent

# Climact submodule:
from conf import GlobalConfig
from obj.icon import Icon

VectorOpts = {
    "frame" : QRectF(-2.5, -2.5, 5, 5),     # Default bounding rectangle.
    "offset": QPointF(16, 0),               # Default offset for the connector's starting and ending points.
    "radius": 4.0,                          # Radius for the rounded corners.
    "stroke": {
        "style": Qt.PenStyle.SolidLine,
        "color": QColor(0xababab),
        'width': 1.5,
    },
}

class Vector(QGraphicsObject):

    # Constructor:
    def __init__(self, parent: QGraphicsObject | None = None, **kwargs):

        # Initialize the base class:
        super().__init__(parent)
        super().setAcceptHoverEvents(True)

        # Set properties:
        self.setProperty("stroke", kwargs.get("stroke", VectorOpts["stroke"]))

        self._route = QPainterPath()
        self._arrow = Icon(
            GlobalConfig["root"] + "/rss/icons/arrow.svg",
            self,
            size = QSize(16, 16),
        )

        # Store reference(s):
        self.origin = kwargs.get("origin", None)
        self.target = kwargs.get("target", None)
        self.setZValue(-1)

        # If origin and target handles are provided, connect them:
        if  self.origin and self.target:

            self.origin.pair(self, self.target)
            self.target.pair(self, self.origin)
            self.on_path_updated()

    # Reimplementation of QGraphicsObject.boundingRect():
    def boundingRect(self) -> QRectF:   return self._route.boundingRect()

    # Reimplementation of QGraphicsObject.paint():
    def paint(self, painter: QPainter, option, widget=None):

        # Customize the painter and draw the path:
        pen = QPen(
            self.property("stroke")['color'],
            self.property("stroke")['width'],
            self.property("stroke")['style'],
        )
        painter.setPen(pen)
        painter.drawPath(self._route)

        # Add label if an origin handle is available:
        if self.origin:

            path = QPainterPath()
            path.addText(
                self.origin.scenePos() + QPointF(4, 2),
                QFont("Trebuchet MS", 7),
                'Handle'
            )

            pen.setWidthF(3.0)
            pen.setColor(Qt.GlobalColor.white)
            painter.setPen(pen)
            painter.drawPath(path)

            pen.setWidthF(0.25)
            pen.setColor(self.property('stroke')['color'])

            painter.setPen(pen)
            painter.setBrush(self.property('stroke')['color'])
            painter.drawPath(path)


    # Reimplementation of QGraphicsObject.shape():
    def shape(self):

        stroker = QPainterPathStroker()
        stroker.setWidth(self.property("stroke")['width'])

        return stroker.createStroke(self._route)

    # Reimplementation of QGraphicsObject.hoverEnterEvent():
    def hoverEnterEvent(self, event: QGraphicsSceneHoverEvent):
        super().hoverEnterEvent(event)
        self.setCursor(Qt.CursorShape.SizeAllCursor)

    # Reimplementation of QGraphicsObject.hoverEnterEvent():
    def hoverLeaveEvent(self, event, /):
        super().hoverLeaveEvent(event)
        self.unsetCursor()

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

        if  opos.x() <= tpos.x() - 2 * VectorOpts['offset'].x():
            self._route = self.segment(opos, tpos)
            self._arrow.setRotation(np.degrees(np.arctan(self._route.slopeAtPercent(0.5))))

        else:
            self._route = self.loopback(opos, tpos)
            self._arrow.setRotation(180)

        # Reposition the label and arrow:
        self._arrow.setPos(self._route.pointAtPercent(0.5))

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

        opos += VectorOpts['offset']
        tpos -= VectorOpts['offset']

        if  tpos.y() != opos.y():   angle = 0.75 * np.arctan(np.abs(tpos.x() - opos.x()) / np.abs(tpos.y() - opos.y()))
        else:                       angle = np.pi / 2.0

        theta = angle if tpos.y() > opos.y() else np.pi - angle
        xm  = 0.50 * (opos.x() + tpos.x())
        xd  = np.tan(theta) * (tpos.y() - opos.y()) / 2.0
        rad = min(0.50 * np.abs(tpos.y() - opos.y()), VectorOpts['radius'])

        # If the origin is to the left of the target, draw the path accordingly:
        path = QPainterPath()
        path.moveTo(opos - VectorOpts['offset'])
        path.lineTo(opos)

        path.lineTo(xm - xd - rad, opos.y())
        path.quadTo(xm - xd, opos.y(), xm - xd + rad * np.sin(theta), opos.y() + rad * np.cos(theta))
        path.lineTo(xm + xd - rad * np.sin(theta), tpos.y() - rad * np.cos(theta))
        path.quadTo(xm + xd, tpos.y(), xm + xd + rad, tpos.y())

        path.lineTo(tpos)
        path.lineTo(tpos + VectorOpts['offset'])

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

        opos += VectorOpts['offset']
        tpos -= VectorOpts['offset']
        diff  = tpos - opos

        path = QPainterPath()
        mid  = QPointF(0.5 * opos.x(), 0.5 * opos.y()) + QPointF(0.5 * tpos.x(), 0.5 * tpos.y())
        rad  = min(0.50 * np.abs(diff.y()), VectorOpts['radius'])

        path.moveTo(opos - VectorOpts['offset'])
        path.lineTo(opos - QPointF(rad, 0))

        if  tpos.y() > opos.y():
            path.arcTo(QRectF(opos - QPointF(2 * rad, 0), QSizeF(2 * rad, 2 * rad)), 90, -90)
            path.lineTo(opos.x(), mid.y() - rad)
            path.arcTo(QRectF(opos.x() - 2*rad, mid.y() - 2*rad, 2 * rad, 2 * rad), 0, -90)
            path.lineTo(tpos.x() + rad, mid.y())
            path.arcTo(QRectF(tpos.x(), mid.y(), 2 * rad, 2 * rad), 90, 90)
            path.lineTo(tpos.x(), tpos.y() - 2 * rad)
            path.arcTo(QRectF(tpos.x(), tpos.y() - 2 * rad, 2 * rad, 2 * rad), 180, 90)
            path.lineTo(tpos + VectorOpts['offset'])

        else:
            path.arcTo(QRectF(opos - QPointF(2 * rad, 2 * rad), QSizeF(2 * rad, 2 * rad)), 270, 90)
            path.lineTo(opos.x(), mid.y() + rad)
            path.arcTo(QRectF(opos.x() - 2 * rad, mid.y(), 2 * rad, 2 * rad), 0, 90)
            path.lineTo(tpos.x() + rad, mid.y())
            path.arcTo(QRectF(tpos.x(), mid.y() - 2 * rad, 2 * rad, 2 * rad), 270, -90)
            path.lineTo(tpos.x(), tpos.y() + 2 * rad)
            path.arcTo(QRectF(tpos.x(), tpos.y(), 2 * rad, 2 * rad), 180, -90)
            path.lineTo(tpos + VectorOpts['offset'])

        return path

    # Reset the path and hide the item:
    def clear(self):

        rect = self.boundingRect()
        self._route.clear()
        self._arrow.setPos(QPointF())
        self.scene().update(rect)