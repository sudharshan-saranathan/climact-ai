# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: vertex
# Description: A QGraphicsObject-based vertex for the Climact application that represents a processing unit in a
#              schematic. The vertex can be resized vertically using a handle at its bottom edge, and it contains
#              input and output anchors for connecting to other vertices via handles.
# ----------------------------------------------------------------------------------------------------------------------

# Import(s):
# Standard:
import json
import types

# Dependency: PySide6
from PySide6.QtCore import Qt, QRectF, Signal, QPointF
from PySide6.QtGui import QBrush, QColor, QPen
from PySide6.QtWidgets import QGraphicsObject

# Climact-ai sub-module(s):
from apps.schema.anchor import Anchor
from apps.schema.handle import Handle, HandleRole
from conf import GlobalIcons
from obj.label import Label
from obj.svgicon import SvgIcon

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
        'normal': QColor(0x4a6d7c),
        'select': QColor(0xf3a738)
    },
    'anchor-position': {
        'INP' : -32,
        'OUT' :  32
    }
}

# Class Resizing handle:
class ResizeHandle(QGraphicsObject):

    # Signal(s):
    sig_handle_moved = Signal()

    # Default constructor:
    def __init__(self, **kwargs):

        # Base-class initialization:
        super().__init__(kwargs.get('parent', None))

        # Set attribute(s):
        self.setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsMovable,True)
        self.setFlag(QGraphicsObject.GraphicsItemFlag.ItemSendsScenePositionChanges,True)
        self.setAcceptHoverEvents(True)

        # Set class-level attribute(s):
        self.setProperty('shape',QRectF(-32, -2, 64, 4))
        self.sig_handle_moved.connect(kwargs.get('callback', lambda: None))

    # Reimplementation of QGraphicsObject.boundingRect():
    def boundingRect(self) -> QRectF:       return self.property('shape')

    # Reimplementation of QGraphicsObject.paint():
    def paint(self, painter, option, /, widget = ...):

        # The resize-handle must be invisible:
        painter.setPen(QPen(Qt.PenStyle.NoPen))
        painter.setBrush(Qt.BrushStyle.NoBrush)
        painter.drawRoundedRect(self.boundingRect(), 2, 2)

    # Reimplementation of QGraphicsObject.itemChange():
    def itemChange(self, change, value, /):

        # Emit the `sig_handle_moved` signal if the position has changed. This signal can be captured by the parent to
        # trigger a resizing-operation.
        if  change == QGraphicsObject.GraphicsItemChange.ItemPositionHasChanged:
            self.sig_handle_moved.emit()

        # Invoke the base-class implementation:
        return super().itemChange(change, value)

    # Reimplementation of QGraphicsObject.hoverEnterEvent():
    def hoverEnterEvent(self, event, /):
        super().setCursor(Qt.CursorShape.SizeVerCursor)
        super().hoverEnterEvent(event)

    # Reimplementation of QGraphicsObject.hoverLeaveEvent():
    def hoverLeaveEvent(self, event, /):
        super().unsetCursor()
        super().hoverLeaveEvent(event)

# ----------------------------------------------------------------------------------------------------------------------
class Vertex(QGraphicsObject):
    """
    This class is a custom QGraphicsObject that is painted onto a QGraphicsScene, it is part of the Climact-ai application.
    The class can be used to represent any process where input resources are transformed into output products (e.g. a
    turbine where electricity is produced from steam or any other working fluid). Modelers can define parameters and
    equations and store them in this instance.
    """

    # Signals:
    sig_handle_clicked = Signal(Handle)

    # Default constructor:
    def __init__(self, **kwargs):

        # Base-class initialization:
        super().__init__(kwargs.get('parent', None))
        super().setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsMovable,True)
        super().setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsSelectable,True)
        super().setAcceptHoverEvents(True)

        # Set class-level attributes:
        self.setProperty('name' , kwargs.get('name' , "Generic"))
        self.setProperty('image', kwargs.get('icon' , GlobalIcons['Vertex']['default']))
        self.setProperty('limit', kwargs.get('limit', VertexOpts['frame'].bottom()))
        self.setProperty('frame', kwargs.get('frame', VertexOpts['frame']))
        self.setProperty('round', kwargs.get('round', VertexOpts['round']))
        self.setProperty('board', kwargs.get('board', VertexOpts['board']))
        self.setProperty('style', kwargs.get('style', VertexOpts['style']))
        self.setProperty('group', kwargs.get('group', None))

        # Add a resize-handle at the bottom:
        self._resize_handle = ResizeHandle(parent = self, callback = self.on_resize_handle_moved)
        self._resize_handle.moveBy(0, self.property('frame').bottom())

        # Add anchor(s):
        self._inp_anchor = Anchor(parent = self, cpos = QPointF(VertexOpts['anchor-position']['INP'], 0), callback=self.on_anchor_clicked)
        self._out_anchor = Anchor(parent = self, cpos = QPointF(VertexOpts['anchor-position']['OUT'], 0), callback=self.on_anchor_clicked)

        # Add icon if provided:
        self._icon = SvgIcon(self.property('image'), parent = self)

        # The vertex's name:
        self._text = Label(self.property('name'), parent = self, color = QColor(0xffffff), width = 64)
        self._text.setY(self.property('frame').top() - 2)
        self._text.sig_text_changed.connect(lambda name: self.setProperty('name', name))

        # Handle-dictionaries:
        self._conn = types.SimpleNamespace(
            inp = dict(),
            out = dict()
        )

    # ------------------------------------------------------------------------------------------------------------------
    # Reimplementation of virtual function(s):

    # Reimplementation of QGraphicsObject.boundingRect():
    def boundingRect(self) -> QRectF:       return self.property('frame')

    # Reimplementation of QGraphicsObject.paint():
    def paint(self, painter, option, /, widget = ...):

        # Set a custom pen and brush:
        painter.setPen  (QPen  (self.property('style')['select' if self.isSelected() else 'normal'], 2.0))
        painter.setBrush(QBrush(self.property('style')['select' if self.isSelected() else 'normal']))
        painter.drawRoundedRect(self.boundingRect(), self.property('round'), self.property('round'))

        # Draw the white board:
        painter.setBrush(self.property('board')['brush'])
        painter.drawRoundedRect(
            self.property('frame').adjusted(0.25, 16, -0.25, -0.25),
            self.property('board')['round'],
            self.property('board')['round']
        )

    # Reimplementation of QGraphicsObject.itemChange():
    def itemChange(self, change, value, /):

        if  change == QGraphicsObject.GraphicsItemChange.ItemSceneHasChanged and self.scene():
            self.sig_handle_clicked.connect(self.scene().begin_transient)

        # Invoke the base-class implementation:
        return super().itemChange(change, value)

    # ------------------------------------------------------------------------------------------------------------------
    # Reimplementation of event-handler(s) for Qt events:

    # QGraphicsObject.hoverEnterEvent():
    def hoverEnterEvent(self, event) -> None:
        super().setCursor(Qt.CursorShape.ArrowCursor)
        super().hoverEnterEvent(event)

    # QGraphicsObject.hoverLeaveEvent():
    def hoverLeaveEvent(self, event, /):
        super().unsetCursor()
        super().hoverLeaveEvent(event)

    # ------------------------------------------------------------------------------------------------------------------
    # Callback method(s) for user-driven events:

    # Callback when the resize-handle is moved:
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
        if  hasattr(self, '_inp_anchor') and hasattr(self, '_out_anchor'):
            self._inp_anchor.resize(frame.bottom() - 4)
            self._out_anchor.resize(frame.bottom() - 4)

        # Update the scene to avoid visual artifacts:
        if  self.scene(): self.scene().update(self.scene().visible_region())

    # Callback when an anchor is clicked:
    def on_anchor_clicked(self, cpos: QPointF):

        # Define temporary variable(s):
        anchor = self.sender()
        coords = self.mapFromItem(anchor, cpos)
        handle = self.create_handle(
            HandleRole.INP if anchor is self._inp_anchor else HandleRole.OUT,
            coords
        )

        # Re-adjust the limit and emit the sig_handle_clicked signal:
        self.setProperty('limit', max(self.property('limit'), handle.y() + 8))
        self.sig_handle_clicked.emit(handle)

    # ------------------------------------------------------------------------------------------------------------------
    # Public method(s):

    # Method to create a new handle:
    def create_handle(self, role: HandleRole, cpos: QPointF = QPointF(), **kwargs) -> Handle | None:

        # If no coordinate has been provided, assume the y-coordinate is zero:
        cpos = cpos or QPointF(self.boundingRect().left() if role == HandleRole.INP else self.boundingRect().right(), 0)

        # Create the handle:
        handle = Handle(
            role,
            cpos,
            self,
            **kwargs
        )
        handle.sig_handle_clicked.connect(self.sig_handle_clicked.emit)

        # Create a new handle at the clicked position:
        if   cpos.x() >= 0:    self._conn.out[handle] = True
        elif cpos.x() <  0:    self._conn.inp[handle] = True

        # Return a reference to the created handle:
        return handle

    def to_json(self) -> str:

        json_dict = dict()
        json_dict['vertex-label'] = self._text.toPlainText()
        json_dict['vertex-group'] = self.property('group')
        json_dict['vertex-xpos']  = self.scenePos().x()
        json_dict['vertex-ypos']  = self.scenePos().y()
        json_dict['inp'] = {
            handle.property('label'): {
                'handle-xpos' : handle.pos().x(),
                'handle-ypos' : handle.pos().y(),
                'handle-value': 0.0
            }

            for handle in self._conn.inp.keys()
        }

        json_dict['out'] = {
            handle.property('label'): {
                'handle-xpos': handle.pos().x(),
                'handle-ypos': handle.pos().y(),
                'handle-value': 0.0
            }

            for handle in self._conn.out.keys()
        }

        encoder = json.JSONEncoder()
        return encoder.encode(json_dict)
