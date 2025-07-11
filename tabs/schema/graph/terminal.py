import numpy as np
import logging

from PyQt6.QtCore import (
    Qt, 
    QRectF, 
    QPointF, 
    pyqtSlot,
    pyqtSignal
)

from PyQt6.QtGui import (
    QPen, 
    QBrush,
    QPainter
)

from PyQt6.QtWidgets import (
    QGraphicsObject, 
    QGraphicsItem, 
    QMenu
)

from custom  import *
from util    import *
from .handle import Handle

class StreamTerminal(QGraphicsObject):

    # Signals:
    sig_item_clicked = pyqtSignal() # Emitted when the terminal's handle is clicked
    sig_item_updated = pyqtSignal() # Emitted when the terminal is updated
    sig_item_removed = pyqtSignal() # Emitted when the terminal is removed

    # Constants:
    class Constants:
        COUNT = 4
        ICON_WIDTH  = 32 # Width of the icon
        ICON_OFFSET = 4  # Offset of the icon from the terminal's left/right edge

    # Default Attrib:
    class Attr:
        def __init__(self):
            self.rect = QRectF(-StreamTerminal.Constants.ICON_WIDTH / 2,
                               -StreamTerminal.Constants.ICON_WIDTH / 2,
                                StreamTerminal.Constants.ICON_WIDTH,
                                StreamTerminal.Constants.ICON_WIDTH)

    # Initializer:
    def __init__(self,
                 eclass : EntityClass,
                 parent : QGraphicsObject | None):

        # Initialize base-class:
        super().__init__(parent)

        # Initialize attribute(s):
        self._tuid   = random_id(length=4, prefix='T')
        self._attr   = self.Attr()
        self._eclass = eclass

        # Load icon according to `eclass`:
        if  eclass == EntityClass.OUT:
            icon = load_svg("rss/icons/plus.svg", self.Constants.ICON_WIDTH)
            icon.moveBy(-self._attr.rect.width() / 2.0, -self._attr.rect.height() / 2.0)
            icon.setParentItem(self)

        elif eclass == EntityClass.INP:
            icon = load_svg("rss/icons/minus.svg", self.Constants.ICON_WIDTH)
            icon.moveBy(-self._attr.rect.width() / 2.0, -self._attr.rect.height() / 2.0)
            icon.setParentItem(self)

        # Customize behavior:
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)

        # Create four terminal-handles and position them:
        self.hlist = list()
        self.x_pos = self._attr.rect.right() + 4 if eclass == EntityClass.OUT else self._attr.rect.left() - 4
        self.y_pos = np.linspace(self._attr.rect.top() + 4, self._attr.rect.bottom() - 4, self.Constants.COUNT)

        for ind in range(self.Constants.COUNT):
            handle = Handle(eclass, QPointF(self.x_pos, self.y_pos[ind]), str(), terminal = True)
            handle.setParentItem(self)

            handle.sig_item_clicked.connect(self.sig_item_clicked.emit)
            handle.sig_item_updated.connect(self.on_handle_updated)
            self.hlist.append(handle)

        # Initialize context-menu:
        self._menu = QMenu()
        delete = self._menu.addAction("Delete")
        delete.triggered.connect(self.sig_item_removed.emit)

    # Re-implemented methods -------------------------------------------------------------------------------------------
    # Name                      Description
    # ------------------------------------------------------------------------------------------------------------------
    # 1. boundingRect           Returns the bounding rectangle of the terminal.
    # 2. paint                  Paints the terminal.
    # ------------------------------------------------------------------------------------------------------------------

    def boundingRect(self) -> QRectF:
        """
        Re-implementation of the `QGraphicsObject.boundingRect()` method.
        """
        return self._attr.rect

    # Paint:
    def paint(self, painter, option, widget = ...):
        """
        Re-implementation of the `QGraphicsObject.paint()` method.
        """
        rect = QRectF(
            self._attr.rect.right() if self._eclass == EntityClass.OUT else self._attr.rect.left() - 8,
            self._attr.rect.top(),
            8,
            self._attr.rect.height()
        )
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(0x50808e)
        painter.setBrush(0x50808e)
        painter.drawRoundedRect(rect, 4, 4)

    # Re-implementation
    def itemChange(self, change, value):
        """
        Reimplementation of QGraphicsObject.itemChange()
        """

        # Import CanvasState from canvas-module:
        from tabs.schema import CanvasState

        # If terminal was added to a scene:
        if change == QGraphicsItem.GraphicsItemChange.ItemSceneHasChanged and value:
            for handle in self.hlist:
                handle.sig_item_clicked.connect(value.begin_transient)
                handle.sig_item_updated.connect(lambda: value.sig_canvas_state.emit(CanvasState.HAS_UNSAVED_CHANGES))

            self.sig_item_removed.connect(value.on_item_removed)

        return value

    # Event-handlers ---------------------------------------------------------------------------------------------------
    # Name                      Description
    # ------------------------------------------------------------------------------------------------------------------
    # 1. contextMenuEvent       Displays the _node's context menu.
    # 2. hoverEnterEvent        Sets the cursor to an arrow when hovering over the terminal.
    # 3. hoverLeaveEvent        Unsets the cursor when leaving the terminal.
    # ------------------------------------------------------------------------------------------------------------------

    def contextMenuEvent(self, event):
        """
        Re-implementation of the `QGraphicsObject.contextMenuEvent()` method.
        """
        self._menu.exec(event.screenPos())

    def hoverEnterEvent(self, event):
        """
        Re-implementation of the `QGraphicsObject.hoverEnterEvent()` method.
        """
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        """
        Re-implementation of the `QGraphicsObject.hoverLeaveEvent()` method.
        """
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().hoverLeaveEvent(event)

    # Custom methods ---------------------------------------------------------------------------------------------------
    # Name                      Description
    # ------------------------------------------------------------------------------------------------------------------
    # 1. clone                  Duplicates the terminal.
    # ------------------------------------------------------------------------------------------------------------------

    def clone(self, **kwargs):
        """
        Duplicates the terminal.

        Parameters:
            kwargs (dict): Set of keyword arguments

        Returns: 
            StreamTerminal: A new terminal with the same properties as the original terminal.
        """

        terminal = StreamTerminal(self.eclass, None)
        terminal.setPos(self.scenePos() + QPointF(25, 25))
        terminal.setSelected(True)

        # Create a hash-map entry:
        Handle.cmap[self.handle] = terminal.handle

        # Copy attribute(s):
        for ind, handle in enumerate(self.hlist):
            self.hlist[ind].clone_into(terminal.hlist[ind])

        self.setSelected(False)

        # Emit the handle's signal to propagate it to the terminal:
        terminal.handle.set_stream(Stream(self.handle.strid, self.handle.color))

        # Return reference:
        return terminal

    @pyqtSlot(Handle)
    def on_handle_updated(self, _handle):
        """
        Event handler for when the handle is updated.
        """
        for handle in self.hlist:
            if  handle is not _handle:
                handle.blockSignals(True)      # Block signals to prevent infinite recursion
                handle.set_stream(Stream(handle.strid, handle.color))
                handle.blockSignals(False)

    # Properties -------------------------------------------------------------------------------------------------------
    # Name                      Description
    # ------------------------------------------------------------------------------------------------------------------
    # 1. uid                    The terminal's unique identifier.
    # 2. eclass                 The terminal's entity class.
    # ------------------------------------------------------------------------------------------------------------------

    @property
    def uid(self) -> str: return self._tuid

    @property
    def eclass(self): return self._eclass

    @property
    def title(self): return self.handle.label