# Encoding: utf-8
# Module name: vertex
# Description: A QGraphicsObject-based vertex for the Climact application that represents a generic node in a schematic.
import types

# Imports:
# Standard module(s):
import enum

# PySide6
from PySide6.QtCore import Qt, QRectF, Signal, QPointF, QSize
from PySide6.QtGui import QBrush, QColor, QPen, QFont
from PySide6.QtWidgets import QGraphicsObject

from apps.schema.anchor import Anchor
from apps.schema.handle import Handle
from conf import GlobalConfig
from obj import *
from obj.button import Button


# Enumeration for resource types:
class EntityRole(enum.Enum):
    INP = enum.auto()
    OUT = enum.auto()
    PAR = enum.auto()

# Default vertex options:
VertexOpts = {
    'round' : 4,
    'frame' : QRectF(-32, -40, 64, 68),
    'board' : {
        'round' : 4,
        'frame' : QRectF(-32, -28, 64, 56),
        'brush' : QBrush(QColor(0xffffff)),
    },
    'style' : {
        'pen'   : {
            'normal': QPen(QColor(0x364958)),
            'select': QPen(QColor(0xf3a738))
        },
        'brush' : {
            'normal': QBrush(QColor(0x364958)),
            'select': QBrush(QColor(0xf3a738))
        }
    },
}

# Class Resizing handle:
class ResizeHandle(QGraphicsObject):

    # Signal(s):
    sig_resize_handle_moved = Signal()

    # Default constructor:
    def __init__(self, **kwargs):

        # Base-class initialization:
        super().__init__(kwargs.get('parent', None))
        super().setAcceptHoverEvents(True)
        super().setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsMovable)
        super().setFlag(QGraphicsObject.GraphicsItemFlag.ItemSendsScenePositionChanges)

        # Set class-level attribute(s):
        self.setProperty('frame', kwargs.get('frame' , QRectF(-32, -2, 64, 4)))
        self.sig_resize_handle_moved.connect(kwargs.get('callback', None))

    # Reimplementation of QGraphicsObject.boundingRect():
    def boundingRect(self) -> QRectF:       return self.property('frame')

    # Reimplementation of QGraphicsObject.paint():
    def paint(self, painter, option, /, widget = ...):

        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(self.boundingRect(), 2, 2)

    # Reimplementation of QGraphicsObject.itemChange():
    def itemChange(self, change, value, /):

        # Emit a signal when the resize-handle is moved:
        if  change == QGraphicsObject.GraphicsItemChange.ItemPositionHasChanged:
            self.sig_resize_handle_moved.emit()

        return value

    # Reimplementation of QGraphicsObject.hoverEnterEvent():
    def hoverEnterEvent(self, event, /):
        super().setCursor(Qt.CursorShape.SizeVerCursor)
        super().hoverEnterEvent(event)

    # Reimplementation of QGraphicsObject.hoverLeaveEvent():
    def hoverLeaveEvent(self, event, /):
        super().unsetCursor()
        super().hoverLeaveEvent(event)

# Class Vertex:
class  Vertex(QGraphicsObject):

    # Signal(s):
    sig_handle_clicked  = Signal(Handle)
    sig_handle_moved    = Signal()

    # Default constructor:
    def __init__(self, parent: QGraphicsObject | None = None, **kwargs):

        # Base-class initialization:
        super().__init__(parent)
        super().setAcceptHoverEvents(True)
        super().setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsMovable)
        super().setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsSelectable)

        # Set class-level attributes:
        self.setProperty('limit', kwargs.get('limit', VertexOpts['frame'].bottom()))
        self.setProperty('frame', kwargs.get('frame', VertexOpts['frame']))
        self.setProperty('round', kwargs.get('round', VertexOpts['round']))
        self.setProperty('board', kwargs.get('board', VertexOpts['board']))
        self.setProperty('style', kwargs.get('style', VertexOpts['style']))
        self.setProperty('label', kwargs.get('label', 'Process'))
        self.setProperty('icon' , kwargs.get('icon' , GlobalConfig['root'] + '/rss/icons/pack-two/process.svg'))

        # Add anchor(s):
        self._inp_anchor = Anchor(EntityRole.INP.value, parent = self, cpos = QPointF(-31.5, 0), callback = self.on_anchor_clicked)
        self._out_anchor = Anchor(EntityRole.OUT.value, parent = self, cpos = QPointF( 31.5, 0), callback = self.on_anchor_clicked)

        # Add a resize-handle at the bottom:
        self._resize_handle = ResizeHandle(parent = self, callback = self.on_resize_handle_moved)
        self._resize_handle.moveBy(0, self.property('frame').bottom())

        # Label and icon:
        self._image = SvgIcon(parent = self, file  = self.property('icon'))
        self._label = Label  (parent = self, label = self.property('label'), color = QColor(0xffffff), width=self.property('frame').width() - 4)
        self._label.sig_text_changed.connect(self.on_text_changed)

        self._label.setX(self.property('frame').left() + 2)
        self._label.setY(self.property('frame').top() - 2)

        # Handle database:
        self._connections = types.SimpleNamespace(
            inp = dict(),
            out = dict()
        )

    # Reimplementation of QGraphicsObject.boundingRect():
    def boundingRect(self) -> QRectF:       return self.property('frame')

    # Reimplementation of QGraphicsObject.paint():
    def paint(self, painter, option, /, widget = ...):

        # Customize painter:
        painter.setPen  (self.property('style')['pen']   ['select' if self.isSelected() else 'normal'])
        painter.setBrush(self.property('style')['brush'] ['select' if self.isSelected() else 'normal'])
        painter.drawRoundedRect(self.boundingRect(), self.property('round'), self.property('round'))

        # Draw the white board:
        painter.setBrush(self.property('board')['brush'])
        painter.drawRoundedRect(
            self.property('frame').adjusted(1, 16, -1, -1),
            self.property('board')['round'],
            self.property('board')['round']
        )

        # Repaint the canvas:
        if  self.scene():
            self.scene().update(self.scene().visible_region())

    # Reimplementation of QGraphicsObject.itemChange():
    def itemChange(self, change, value, /):

        if (
            change == QGraphicsObject.GraphicsItemChange.ItemSceneHasChanged and
            self.scene()
        ):
            self.sig_handle_clicked.connect(self.scene().begin_transient)

        # Invoke the base-class implementation:
        return super().itemChange(change, value)

    # ------------------------------------------------------------------------------------------------------------------
    # Event handler(s):
    # Reimplementation of QGraphicsObject.hoverEnterEvent():
    def hoverEnterEvent(self, event) -> None:
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event, /):
        self.unsetCursor()
        super().hoverLeaveEvent(event)

    # ------------------------------------------------------------------------------------------------------------------
    # Callback functions for user-driven events:

    # When the vertex's resize-handle is moved:
    def on_resize_handle_moved(self):

        # Get the current limit and frame:
        limit = self.property('limit')
        frame = self.property('frame')

        # Update the frame's bottom based on the handle's position:
        frame.setBottom(max(self._resize_handle.y(), limit))
        self .setProperty('frame', frame)

        # Reposition the resize-handle:
        self._resize_handle.setX(0)
        self._resize_handle.setY(frame.bottom())

        # Resize the anchors:
        self._inp_anchor.resize(frame.bottom() - 6)
        self._out_anchor.resize(frame.bottom() - 6)

    # When an anchor is clicked:
    def on_anchor_clicked(self, cpos: QPointF):

        anchor = self.sender()              # The anchor that sent the signal
        coords = anchor.mapToParent(cpos)   # Get the coordinates in the vertex's reference frame
        offset = 8 if anchor is self._inp_anchor else -8

        # Create a new handle at the clicked position:
        handle = Handle(
            self,
            cpos = coords,
            offset = offset,
            callback = self.sig_handle_clicked
        )

        # Add the handle to the database:
        self.sig_handle_clicked.emit(handle)
        self._connections.inp[handle] = anchor

    # When the label text is changed:
    def on_text_changed(self, text: str):   self.setProperty('label', text)

    # ------------------------------------------------------------------------------------------------------------------
    # Special functions:

    # Clone this vertex:
    def clone(self) -> 'Vertex':

        # Create a new vertex with the same properties:
        vertex = Vertex(
            limit = self.property('limit'),
            frame = self.property('frame'),
            round = self.property('round'),
            board = self.property('board'),
            style = self.property('style'),
            label = self.property('label'),
            icon  = self.property('icon')
        )

        # Return the new vertex:
        return vertex
