# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: handle
# Description: A QGraphicsObject-based handle for the Climact application that represents an input or output connection
#              point on a vertex, similar to the pins on a physical integrated circuit (IC) chip.
# ----------------------------------------------------------------------------------------------------------------------

import enum

# Dependency: PySide6
from PySide6.QtCore import (
    Qt,
    QRectF,
    QPointF,
    Property,
    QEasingCurve,
    QPropertyAnimation,
    Signal
)
from PySide6.QtGui import (
    QPen,
    QColor,
    QBrush
)
from PySide6.QtWidgets import QGraphicsObject, QMenu

# Enum:
class HandleRole(enum.Enum):
    INP = enum.auto(),
    OUT = enum.auto()

# Default handle attribute(s):
HandleOpts = {

    'shape': {
        'bounding-rectangle': QRectF(-1.5, -1.5, 3, 3),     # The bounding rectangle of the handle.
        'hovering-proximity': 4,                            # The proximity distance for hovering detection.
    },

    'style': {
        'border': QPen(Qt.GlobalColor.black, 0.50),
        'colour': QBrush(QColor(0xb4f7d2))
    },

    'animation': {
        'duration': 240,
        'easing-curve': QEasingCurve.Type.OutQuad,
        'start-radius': 1.5,
        'final-radius': 2.0,
    }
}

# QGraphicsObject subclass for the handle:
class Handle(QGraphicsObject):

    # Signals:
    sig_handle_clicked = Signal(QGraphicsObject)

    # Class constructor:
    def __init__(self, role: HandleRole, position: QPointF, parent: QGraphicsObject | None = None, **kwargs):

        # Base-class initialization:
        super().__init__(parent)

        # Set attribute(s):
        self.setProperty('label'    , kwargs.get('label', 'Handle'))
        self.setProperty('shape'    , kwargs.get('shape', HandleOpts['shape']))
        self.setProperty('style'    , kwargs.get('style', HandleOpts['style']))
        self.setProperty('animation', kwargs.get('animation', HandleOpts['animation']))
        self.setProperty('category' , kwargs.get('category', 'Generic'))
        self.setProperty('position' , position)
        self.setProperty('role'     , role)

        # Attribute(s) related to the connection-state of the handle:
        self.setProperty('connected', False)            # Whether the handle is currently connected to another handle.
        self.setProperty('connector', None)             # Reference to the connector (Vector) if connected, else None.
        self.setProperty('conjugate', None)             # Reference to the connected handle if connected, else None.

        # Connect the signal to the callback function, the default callback does nothing:
        self.sig_handle_clicked.connect(kwargs.get('callback', lambda: None))

        # Initialize context-menu:
        self._anim = self._init_animation()
        self._menu = self._init_context_menu()

        # Set flags and other attribute(s):
        self.setAcceptHoverEvents(True)
        self.setPos(position)
        self.setFlag(QGraphicsObject.GraphicsItemFlag.ItemSendsScenePositionChanges)

    # Method to initialize the context menu:
    @staticmethod
    def _init_context_menu():
        """
        This method initializes the context menu for the handle and returns it
        :return: QMenu
        """
        context_menu = QMenu()
        handle_type  = context_menu.addMenu("Set Category")

        return context_menu

    # Method to initialize the animation:
    def _init_animation(self):
        """
        This method initializes the animation for the radius property of the handle.
        :return: QPropertyAnimation
        """

        animator = QPropertyAnimation(self, b"radius")
        animator.setDuration(self.property('animation')['duration'])
        animator.setEasingCurve(self.property('animation')['easing-curve'])

        return animator

    # ------------------------------------------------------------------------------------------------------------------
    # Section:     CALLBACK FUNCTIONS
    # Description: This section contains re-implementations of event handlers for the base QGraphicsObject class. These
    #              methods are invoked by user-driven events such as hovering over the handle or clicking it. For more
    #              information on these methods and how they work, refer to PySide6 or Qt-documentation.
    # ------------------------------------------------------------------------------------------------------------------

    # Reimplementation of QGraphicsObject.boundingRect():
    def boundingRect(self, /):
        """
        Returns the bounding rectangle of the handle, adjusted for hovering proximity.
        :return: QRectF
        """

        return self.property('shape')['bounding-rectangle'].adjusted(
            -self.property('shape')['hovering-proximity'],
            -self.property('shape')['hovering-proximity'],
             self.property('shape')['hovering-proximity'],
             self.property('shape')['hovering-proximity']
        )

    # Reimplementation of QGraphicsObject.paint():
    def paint(self, painter, option, widget = ...):
        """
        Paints the handle onto the canvas.
        :param painter: QPainter instance managed by the Qt framework.
        :param option:  QStyleOptionGraphicsItem instance managed by the Qt framework.
        :param widget:  QWidget instance managed by the Qt framework.
        :return: None
        """

        painter.setPen(self.property('style')['border'])
        painter.setBrush(self.property('style')['colour'])
        painter.drawEllipse(self.property('shape')['bounding-rectangle'])

        # If the cursor is hovering over the handle, draw an additional black ellipse inside the handle:
        if  self.isUnderMouse():

            painter.setBrush(QBrush(QColor(Qt.GlobalColor.black)))
            painter.drawEllipse(HandleOpts['shape']['bounding-rectangle'].adjusted(0.75, 0.75, -0.75, -0.75))

    # Reimplementation of QGraphicsObject.itemChange():
    def itemChange(self, change: QGraphicsObject.GraphicsItemChange, value, /):

        # If the handle is moved and is connected, update the connector's path:
        if (
            change == QGraphicsObject.GraphicsItemChange.ItemScenePositionHasChanged and
            self.property('connected')
        ):

            connector = self.property('connector')
            conjugate = self.property('conjugate')

            if  connector and conjugate:
                connector.on_path_updated()

        return value

    # Reimplementation of QGraphicsObject.contextMenuEvent():
    def contextMenuEvent(self, event, /):

        self._menu.exec(event.screenPos())

    # Reimplementation of QGraphicsObject.hoverEnterEvent():
    def hoverEnterEvent(self, event, /):

        # Call the base-class implementation, set the correct cursor and show the hint:
        super().hoverEnterEvent(event)
        super().setCursor(Qt.CursorShape.ArrowCursor)

        # Start animation:
        self._anim.setStartValue(self.property('animation')['start-radius'])
        self._anim.setEndValue(self.property('animation')['final-radius'])
        self._anim.start()

    # Reimplementation of QGraphicsObject.hoverLeaveEvent():
    def hoverLeaveEvent(self, event, /):

        # Call the base-class implementation, set the correct cursor and show the hint:
        super().hoverLeaveEvent(event)
        super().unsetCursor()

        # Start animation:
        self._anim.setStartValue(self.property('animation')['final-radius'])
        self._anim.setEndValue(self.property('animation')['start-radius'])
        self._anim.start()

    # Reimplementation of QGraphicsObject.mousePressEvent():
    def mousePressEvent(self, event, /):

        # Clear scene selection:
        if  self.scene():   self.scene().clearSelection()

        # If connected, allow the handle to be moved, else emit the clicked-signal:
        if  self.property('connected'):
            super().setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsMovable)
            super().mousePressEvent(event)

        else:
            self.sig_handle_clicked.emit(self)

    # Reimplementation of QGraphicsObject.mouseReleaseEvent():
    def mouseReleaseEvent(self, event, /):

        super().mouseReleaseEvent(event)
        super().setX(self.property('position').x())

    # ------------------------------------------------------------------------------------------------------------------
    # Section:     PUBLIC METHODS
    # Description: This section contains public methods for the Handle class. These methods can be called from outside
    #              the class to perform various operations related to the handle's functionality.
    # ------------------------------------------------------------------------------------------------------------------

    def pair(self, connector: QGraphicsObject, conjugate: QGraphicsObject) -> None:

        self.setProperty('connected', True)
        self.setProperty('connector', connector)
        self.setProperty('conjugate', conjugate)

    # ------------------------------------------------------------------------------------------------------------------
    # Section:     PROPERTIES
    # Description: This section contains property definitions for the Handle class. Properties are special attributes
    #              that have getter and setter methods, allowing for controlled access and modification of the attributes.
    # ------------------------------------------------------------------------------------------------------------------

    # Get the radius of the handle:
    def get_radius(self) -> float:
        return float(self.property("shape")['bounding-rectangle'].width() / 2)

    # Set the radius of the handle:
    def set_radius(self, radius: float) -> None:

        shape = {
            'bounding-rectangle': QRectF(-radius, -radius, radius * 2, radius * 2),
            'hovering-proximity': self.property('shape')['hovering-proximity']
        }

        self.setProperty("shape", shape)
        self.update()

    # Get the paired state of the handle:
    def get_paired(self) -> bool:
        return self.property("connected")

    # Set the paired state of the handle:
    def set_paired(self, state: tuple) -> None:

        connected, connector, conjugate = state
        self.setProperty('connected', connected)
        self.setProperty('connector', connector)
        self.setProperty('conjugate', conjugate)

    # Declare radius as a property:
    radius = Property(float, get_radius, set_radius)
    paired = Property(bool , get_paired, set_paired)