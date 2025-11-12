# Encoding: utf-8
# Module name: handle
# Description: Connection end points for vertices.

# Import(s):
# Standard module(s):
import enum
import types

# PySide6:
from PySide6.QtCore import (
    Qt,
    QRectF,
    QPointF,
    QSize,
    Property,
    QEasingCurve,
    QPropertyAnimation,
    Signal
)

from PySide6.QtGui import QPen, QColor, QBrush
from PySide6.QtWidgets import QGraphicsObject

# Climact-ai sub-modules:
from opts import GlobalConfig
from obj  import Icon

# Default configuration for handles:
HandleOpts = {
    'frame': QRectF(-1.5, -1.5, 3, 3),
    'color': 0xb4f7d2,
}

class HandleRole(enum.Enum):
    INP = enum.auto()
    OUT = enum.auto()

# Class Handle:
class Handle(QGraphicsObject):

    # Signals:
    sig_handle_clicked = Signal(QGraphicsObject)

    # ------------------------------------------------------------------------------------------------------------------
    # Section       : Initialization and subcomponent setup.
    # Description   : This section contains the class constructor and methods for initializing subcomponents such as
    #                 icons, menus, and animations.
    # ------------------------------------------------------------------------------------------------------------------

    # Class constructor:
    def __init__(
            self,
            role: HandleRole,
            position: QPointF,
            parent: QGraphicsObject | None = None,
            **kwargs
    ):
        # Call the constructor of the base class:
        super().__init__(parent)

        # Set attribute(s):
        self.setProperty('frame', kwargs.get('frame', HandleOpts['frame']))
        self.setProperty('color', kwargs.get('color', HandleOpts['color']))
        self.setProperty('xpos' , position.x())
        self.setProperty('role' , role)

        # Sub-component initialization:
        self._icon = self._init_icon()
        self._anim = self._init_animation()
        self._stat = types.SimpleNamespace(
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
        super().setPos(position)

    # Initialize the animation for the handle:
    def _init_animation(self) -> QPropertyAnimation:

        # Create the animation and set attribute(s):
        animation = QPropertyAnimation(self, b"radius")
        animation.setEasingCurve(QEasingCurve.Type.OutQuad)
        animation.setDuration(240)

        # Return the animation:
        return animation

    # Initialize the icon for the handle:
    def _init_icon(self) -> Icon:

        # Default-icon path:
        file  = GlobalConfig['root']
        file += "/rss/icons/default.svg"

        # Create the icon:
        icon = Icon(
            file,
            parent = self,
            size = QSize(8, 8)
        )

        # Set position according to the handle's role:
        icon.setPos(
            QPointF(-8, 0)
            if      self.property('role') == HandleRole.OUT
            else    QPointF(8, 0)
        )

        # Return the icon:
        return icon

    # ------------------------------------------------------------------------------------------------------------------
    # Section       : Re-implementations of virtual methods.
    # Description   : This section contains re-implementations of the base-class's (QGraphicsObject) virtual methods.
    #                 They are automatically invoked by the Qt framework when certain events occur. Do not change the
    #                 method signatures or the re-implementations will not work as intended.
    # ------------------------------------------------------------------------------------------------------------------

    # Reimplementation of QGraphicsObject.boundingRect():
    def boundingRect(self, /):  return self.property('frame').adjusted(-6, -6, 6, 6)

    # Reimplementation of QGraphicsObject.paint():
    def paint(self, painter, option, widget = ...):

        painter.setPen(QPen(QColor(Qt.GlobalColor.black), 0.50))
        painter.setBrush(QBrush(QColor(self.property('color'))))
        painter.drawEllipse(self.property('frame'))

        if  self.isUnderMouse():
            painter.setBrush(QBrush(QColor(Qt.GlobalColor.black)))
            painter.drawEllipse(HandleOpts['frame'].adjusted(0.75, 0.75, -0.75, -0.75))

    # Reimplementation of QGraphicsObject.itemChange():
    def itemChange(self, change, value, /):

        if  change == QGraphicsObject.GraphicsItemChange.ItemScenePositionHasChanged:
            if  self._stat.connected:
                self._stat.connector.on_path_updated()

        return super().itemChange(change, value)

    # Reimplementation of QGraphicsObject.hoverEnterEvent():
    def hoverEnterEvent(self, event, /):

        super().hoverEnterEvent(event)
        super().setCursor(Qt.CursorShape.ArrowCursor)

        # Start animation:
        self._anim.setStartValue(HandleOpts['frame'].width() / 2)
        self._anim.setEndValue(HandleOpts['frame'].width() / 2 + 0.5)
        self._anim.start()

    # Reimplementation of QGraphicsObject.hoverLeaveEvent():
    def hoverLeaveEvent(self, event, /):

        super().hoverLeaveEvent(event)
        super().unsetCursor()

        # Start animation:
        self._anim.setStartValue(HandleOpts['frame'].width() / 2 + 0.5)
        self._anim.setEndValue(HandleOpts['frame'].width() / 2)
        self._anim.start()

    # Reimplementation of QGraphicsObject.mousePressEvent():
    def mousePressEvent(self, event, /):

        # Clear the scene's selection:
        if  self.scene():
            self.scene().clearSelection()

        if  not self._stat.connected:
            self.sig_handle_clicked.emit(self)

        else:
            event.accept()
            super().setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsMovable)
            super().mousePressEvent(event)

    # Reimplementation of QGraphicsObject.mouseReleaseEvent():
    def mouseReleaseEvent(self, event, /):

        # Ensure that the handle's x-position is locked:
        super().setX(self.property('xpos'))
        super().setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsMovable, False)
        super().mouseReleaseEvent(event)

    # ------------------------------------------------------------------------------------------------------------------
    # Section       : High-level callback functions.
    # Description   : This section contains methods that serve as high-level callbacks for user-driven events.
    # ------------------------------------------------------------------------------------------------------------------

    # When the user connects this handle to another:
    def pair(self, connector: QGraphicsObject, conjugate: 'Handle') -> None:

        self._stat.connected = True
        self._stat.connector = connector
        self._stat.conjugate = conjugate

    # When the user disconnects this handle from another:
    def free(self) -> None:

        self._stat.connected = False
        self._stat.connector = None
        self._stat.conjugate = None

    # ------------------------------------------------------------------------------------------------------------------
    # Section       : Property accessors, mutators, and declarations.
    # Description   : This section contains property accessors, mutators, and declarations for the Handle class. They
    #                 provide controlled access to the class's properties.
    # ------------------------------------------------------------------------------------------------------------------

    # Declare the `radius` property using the `@Property` decorator to register with Qt's metaobject system:
    @Property(float)
    def radius(self) -> float:
        return float(self.property("frame").width() / 2)

    # Setter for the `radius` property:
    @radius.setter
    def radius(self, value: float) -> None:
        self.setProperty("frame", QRectF(-value, -value, value * 2, value * 2))
        self.update()