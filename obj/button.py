# Encoding: utf-8
# Module Name: button
# Description: Custom SVG-based button class to include in a QGraphicsScene.

# Imports:
# PySide6:
from PySide6.QtCore import Signal, QSize, QRectF, Qt, QPointF
from PySide6.QtWidgets import QGraphicsObject
from PySide6.QtSvg import QSvgRenderer

# Custom button class for SVG icons in a QGraphicsScene
class Button(QGraphicsObject):

    # Signals:
    sig_clicked = Signal(int)

    # Constructor:
    def __init__(self, path, parent: QGraphicsObject | None = None, **kwargs):

        # Base-class initialization:
        super().__init__(parent)
        super().setAcceptHoverEvents(True)

        # Initialize properties:
        self.setProperty("size", kwargs.get("size", QSize(16, 16)))
        self.setProperty("cpos", kwargs.get("cpos", QPointF(0, 0)))
        self.setProperty('info', kwargs.get('info', ''))

        # Instantiate an SVG renderer:
        self.renderer = QSvgRenderer(path, self)

        # Connect signal to the callable, if provided:
        if  kwargs.get('callback', None):
            self.sig_clicked.connect(kwargs.get('callback'))

        # Set position:
        self.setPos(self.property("cpos"))
        self.setToolTip(kwargs.get('tooltip', ''))

    # Reimplementation of QGraphicsObject.boundingRect():
    def boundingRect(self) -> QRectF:
        """
        Returns the bounding rectangle of the button.
        :return: QRectF
        """

        return QRectF(-self.property("size").width()  / 2,     # X position of the top-left corner
                      -self.property("size").height() / 2,     # Y position of the top-left corner
                       self.property("size").width(),          # Width of the rectangle
                       self.property("size").height())         # Height of the rectangle

    # Reimplementation of QGraphicsObject.paint():
    def paint(self, painter, option, widget = ...):
        """
        Paints the button using the QSvgRenderer.
        :param painter: QPainter
        :param option: QStyleOptionGraphicsItem
        :param widget: QWidget
        """

        self.renderer.render(painter, self.boundingRect())

    # Reimplementation of QGraphicsObject.mousePressEvent():
    def mousePressEvent(self, event):
        """
        Handles mouse press events to emit the clicked signal.
        :param event: QGraphicsSceneMouseEvent
        """
        if  event.button() == Qt.MouseButton.LeftButton:
            self.sig_clicked.emit(self.property("args"))
            self.setScale(0.96)
            event.accept()

        else:
            event.ignore()

    # Reimplementation of QGraphics.mouseReleaseEvent():
    def mouseReleaseEvent(self, event, /):

        if  event.button() == Qt.MouseButton.LeftButton:
            self.setScale(1.00)
            event.accept()

        else:
            event.ignore()

    # Reimplementation of QGraphicsObject.hoverEnterEvent():
    def hoverEnterEvent(self, event):
        """
        Handles hover enter events to change the cursor shape.
        :param event: QGraphicsSceneHoverEvent
        """

        super().hoverEnterEvent(event)
        super().setOpacity(0.75)
        super().setCursor(Qt.CursorShape.PointingHandCursor)

    # Reimplementation of QGraphicsObject.hoverLeaveEvent():
    def hoverLeaveEvent(self, event):
        """
        Handles hover leave events to reset the cursor shape.
        :param event: QGraphicsSceneHoverEvent
        """

        super().hoverLeaveEvent(event)
        super().setOpacity(1.0)
        super().unsetCursor()