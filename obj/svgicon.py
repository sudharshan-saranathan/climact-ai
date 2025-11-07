# Encoding: utf-8
# Module Name: svgicon
# Description: Animatable SVG-icon class for non-textual labeling.

from PySide6.QtCore import QSize, QRectF, Qt, Signal, QPropertyAnimation, QEasingCurve, Property
from PySide6.QtGui import QPixmap, QPainter
from PySide6.QtWidgets import QGraphicsObject, QGraphicsItem
from PySide6.QtSvg import QSvgRenderer

# Default options:
SvgIconOpts = {
    "size": QSize(28, 28),             # Size of the SVG icon.
    "anim": False                      # Whether to animate the icon on appearance.
}

# Class SvgIcon:
class SvgIcon(QGraphicsObject):

    # Signals:
    sig_item_moved = Signal()

    # Default constructor:
    def __init__(self, file: str, parent: QGraphicsObject | None = None, **kwargs):
        """
        Initializes the SvgIcon with a parent item and optional keyword arguments.
        """

        # Initialize base-class:
        super().__init__(parent)

        # Set properties:
        self.setProperty("file",file)
        self.setProperty("size",kwargs.get("size", SvgIconOpts["size"]))
        self.setProperty("anim",kwargs.get("anim", True))

        # Instantiate an SVG renderer:
        self.renderer = QSvgRenderer(self.property("file"), self)

        # If the `movable` is set:
        if  kwargs.get('movable', False):
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
            self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges)

    # Reimplementation of QGraphicsObject.boundingRect():
    def boundingRect(self) -> QRectF:

        return QRectF(-self.property("size").width()  / 2,
                      -self.property("size").height() / 2,
                       self.property("size").width(),
                       self.property("size").height())

    # Reimplementation of QGraphicsObject.paint():
    def paint(self, painter, option, widget=None):

        painter.save()
        self.renderer.render(painter, self.boundingRect())
        painter.restore()