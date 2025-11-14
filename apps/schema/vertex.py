# Encoding: utf-8
# Module name: vertex
# Description: A QGraphicsObject-based vertex for the Climact application that represents a generic node in a schematic.
import types

# Imports:
# Standard module(s):
import enum

# PySide6
from PySide6.QtCore import Qt, QRectF, Signal, QPointF, QSize
from PySide6.QtGui import QBrush, QColor, QPen, QTextCursor
from PySide6.QtWidgets import QGraphicsObject, QGraphicsItem

from apps.schema.anchor import Anchor
from apps.schema.config import Configurator
from apps.schema.handle import Handle, HandleRole
from opts import GlobalConfig
from obj import *

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
            'normal': QPen(QColor(0x6e2b46), 2.0),
            'select': QPen(QColor(0xffcb00), 2.0)
        },
        'brush' : {
            'normal': QBrush(QColor(0x6e2b46)),
            'select': QBrush(QColor(0xffcb00))
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
class Vertex(QGraphicsObject):

    # Signal(s):
    sig_vertex_renamed = Signal(str)
    sig_handle_clicked = Signal(Handle)
    sig_handle_moved   = Signal()

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

        # Add anchor(s):
        self._inp_anchor = Anchor(HandleRole.INP.value, parent = self, cpos = QPointF(self.property('frame').left() , 0), callback = self.on_anchor_clicked)
        self._out_anchor = Anchor(HandleRole.OUT.value, parent = self, cpos = QPointF(self.property('frame').right(), 0), callback = self.on_anchor_clicked)

        # Add a resize-handle at the bottom:
        self._resize_handle = ResizeHandle(parent = self, callback = self.on_resize_handle_moved)
        self._resize_handle.moveBy(0, self.property('frame').bottom())

        # Label and icon:
        self._image = Icon (parent = self, file = GlobalConfig['root'] + '/rss/icons/pack-two/process.svg', size = QSize(32, 32))
        self._label = Label(parent = self, label = self.property('label'), color = QColor(0xffffff), width = self.property('frame').width() - 4)
        self._label.sig_text_changed.connect(self.on_text_changed)

        self._label.setX(self.property('frame').left() + 2)
        self._label.setY(self.property('frame').top() - 2)

        # Handle database:
        self._connections = types.SimpleNamespace(
            inp = dict(),
            out = dict()
        )

    # Reimplementation of QGraphicsObject.boundingRect():
    def boundingRect(self) -> QRectF:       return self.property('frame').adjusted(-16, -16, 16, 16)

    # Reimplementation of QGraphicsObject.paint():
    def paint(self, painter, option, /, widget = ...):

        # Customize painter:
        painter.setPen  (self.property('style')['pen']   ['select' if self.isSelected() else 'normal'])
        painter.setBrush(self.property('style')['brush'] ['select' if self.isSelected() else 'normal'])
        painter.drawRoundedRect(self.property('frame'), self.property('round'), self.property('round'))

        # Draw the white board:
        painter.setBrush(self.property('board')['brush'])
        painter.drawRoundedRect(
            self.property('frame').adjusted(0, 16, -0, -0),
            self.property('board')['round'],
            self.property('board')['round']
        )

    # Reimplementation of QGraphicsObject.itemChange():
    def itemChange(self, change, value, /):

        # Flag alias:
        cflag = QGraphicsObject.GraphicsItemChange.ItemSceneHasChanged
        sflag = QGraphicsObject.GraphicsItemChange.ItemSelectedChange

        # Connect to the canvas's begin_transient() method when added to a scene:
        if  change == cflag and hasattr(value, 'begin_transient'):
            self.sig_handle_clicked.connect(value.begin_transient)

        if  change == sflag and value == False:
            self.toggle_focus(False)

        # Invoke the base-class implementation:
        return super().itemChange(change, value)

    # ------------------------------------------------------------------------------------------------------------------
    # Event handler(s):
    # Reimplementation of QGraphicsObject.hoverEnterEvent():
    def hoverEnterEvent(self, event) -> None:
        super().setCursor(Qt.CursorShape.ArrowCursor)
        super().hoverEnterEvent(event)

    # Reimplementation of QGraphicsObject.hoverLeaveEvent():
    def hoverLeaveEvent(self, event, /):
        super().unsetCursor()
        super().hoverLeaveEvent(event)

    # ------------------------------------------------------------------------------------------------------------------
    # Callback function(s) for user-driven events like resizing, handle-creation, etc.

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

        anchor = self.sender()                      # The anchor that sent the signal
        coords = self.mapFromItem(anchor, cpos)     # Map the clicked coordinates to the vertex's coordinate system

        # Create a new handle at the clicked position:
        handle = Handle(
            HandleRole.INP if anchor is self._inp_anchor else HandleRole.OUT,
            coords,
            self,
            callback = self.sig_handle_clicked
        )

        # Add the handle to the database:
        self.sig_handle_clicked.emit(handle)        # This allows users to create the handle and begin a transient with a single click
        self._connections.inp[handle] = anchor      # Add the handle to the database

    # When the label text is changed:
    def on_text_changed(self, text: str):

        # Update the label property:
        self.setProperty('label', text)

        # Emit signal:
        if  hasattr(self.scene(), 'sig_canvas_updated'):
            self.scene().sig_canvas_updated.emit(self)

    # ------------------------------------------------------------------------------------------------------------------
    # Functions that allow programmatic state change. These may return complex objects, and therefore cannot be directly
    # used with LLMs' function-calling frameworks.

    # Create a new handle at the specified position:
    def create_handle(self, role: HandleRole, cpos: QPointF) -> Handle:

        # Create the handle:
        handle = Handle(
            role,                               # Role of the handle.
            cpos,                               # Cursor position.
            self,                               # The vertex is the parent.
            callback = self.sig_handle_clicked  # Callback function when the handle is clicked.
        )

        # Add the handle to the database:
        if role == HandleRole.INP:  self._connections.inp[handle] = self._inp_anchor
        else:                       self._connections.out[handle] = self._out_anchor

        # Return the new handle:
        return handle

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

    # Toggle focus on the vertex's label:
    def toggle_focus(self, focus = True):

        if  focus:
            self._label.setFocus(Qt.FocusReason.MouseFocusReason)

        else:
            self._label.clearFocus()

    # Open a configuration widget for this vertex:
    def configure(self):

        dialog = Configurator(self, None)
        dialog.exec()

    # Open a configuration widget for this vertex:
    def validate(self):

        print(f"Validating {self.property('label')}")