# Encoding: utf-8
# Module name: canvas
# Description: A QGraphicsScene-based canvas for the Climact application

# Import(s):
# Standard module(s):
import types
import weakref

# PySide6:
from PySide6.QtCore import QRectF, Qt, QPointF, QObject, Signal
from PySide6.QtGui import QBrush, QColor, QKeySequence
from PySide6.QtWidgets import QGraphicsScene, QMenu, QGraphicsObject

# QtAwesome:
import qtawesome as qta

from apps.schema.anchor import Anchor
from apps.schema.handle import Handle
from apps.schema.vector import Vector

# Climact submodule:
from apps.schema.vertex import Vertex

# Class Canvas: A QGraphicsScene-subclass for the Climact application
class Canvas(QGraphicsScene):

    # Global signals:
    sig_canvas_updated = Signal(QGraphicsObject)

    # Global clipboard:
    clipboard = list()

    # ------------------------------------------------------------------------------------------------------------------
    # Section       : High-level callback functions.
    # Description   : This section contains methods that serve as high-level callbacks for user-driven events.
    # ------------------------------------------------------------------------------------------------------------------

    # Default constructor:
    def __init__(self, parent: QObject | None = None, **kwargs):

        # Base-class initialization:
        super().__init__(parent)

        # Set class-level attribute(s):
        self.setBackgroundBrush(QBrush(QColor(0xefefef), Qt.BrushStyle.DiagCrossPattern))
        self.setSceneRect(kwargs.get('rect', QRectF(0, 0, 10000, 10000)))

        # Transient connection:
        self._transient = types.SimpleNamespace(
            active = False,
            origin = None,
            target = None,
            vector = __import__("apps.schema.vector", fromlist=["Vector"]).Vector()
        )

        self.addItem(self._transient.vector)

        # Initialize context-menu:
        self._cpos = QPointF()
        self._menu = self.init_menu()

    # Context-menu initializer:
    def init_menu(self):

        _menu = QMenu()
        _subm = _menu.addMenu("Add")

        _vertex = _subm.addAction(qta.icon('ph.git-commit-fill', color='#efefef'), 'Vertex', QKeySequence("Ctrl + ["), lambda: self.create_item('Vertex'))
        _stream = _subm.addAction(qta.icon('ph.flow-arrow-fill', color='#efefef'), 'Stream', QKeySequence("Ctrl + ]"), )
        _menu.addSeparator()

        # Project management:
        _open = _menu.addAction(qta.icon('mdi.file', color='#ffcb00'), 'Import', QKeySequence.StandardKey.Open)
        _save = _menu.addAction(qta.icon('mdi.content-save', color='green'), 'Export', QKeySequence.StandardKey.Save)
        _wipe = _menu.addAction(qta.icon('mdi.eraser', color='pink'), 'Clear', QKeySequence("Ctrl + Delete"))
        _menu.addSeparator()

        # Schematic management:
        _copy = _menu.addAction(qta.icon('mdi.content-copy', color='lightgreen'), 'Copy', QKeySequence.StandardKey.Copy)
        _past = _menu.addAction(qta.icon('mdi.content-paste', color='lightblue'), 'Paste', QKeySequence.StandardKey.Paste)
        _undo = _menu.addAction(qta.icon('mdi.undo', color='lavender'), 'Undo', QKeySequence.StandardKey.Undo)
        _redo = _menu.addAction(qta.icon('mdi.redo', color='lavender'), 'Redo', QKeySequence.StandardKey.Redo)
        _menu.addSeparator()

        # Set icon and shortcut visibility in menu and context menu:
        _open.setIconVisibleInMenu(True);   _open.setShortcutVisibleInContextMenu(True)
        _save.setIconVisibleInMenu(True);   _save.setShortcutVisibleInContextMenu(True)
        _wipe.setIconVisibleInMenu(True);   _wipe.setShortcutVisibleInContextMenu(True)
        _copy.setIconVisibleInMenu(True);   _copy.setShortcutVisibleInContextMenu(True)
        _past.setIconVisibleInMenu(True);   _past.setShortcutVisibleInContextMenu(True)
        _undo.setIconVisibleInMenu(True);   _undo.setShortcutVisibleInContextMenu(True)
        _redo.setIconVisibleInMenu(True);   _redo.setShortcutVisibleInContextMenu(True)

        _vertex.setIconVisibleInMenu(True); _vertex.setShortcutVisibleInContextMenu(True)
        _stream.setIconVisibleInMenu(True); _stream.setShortcutVisibleInContextMenu(True)

        # Return the menu instance:
        return _menu

    # Returns the region of the canvas that's visible in the viewport:
    def visible_region(self):

        # If viewers exist:
        if  viewers := self.views():
            rect = viewers[0].viewport().rect()
            return viewers[0].mapToScene(rect).boundingRect()

        return QRectF()

    # ------------------------------------------------------------------------------------------------------------------
    # Event handler(s):
    # Context-menu event handler:
    def contextMenuEvent(self, event, /):

        # Show the context menu:
        self._cpos = event.scenePos()
        self._menu.exec(event.screenPos())

    # Mouse press event handler:
    def mouseMoveEvent(self, event, /):

        # If the transient connection is active, update the vector:
        if  self._transient.active:
            self._transient.vector.on_path_updated(
                self._transient.origin().scenePos(),
                event.scenePos()
            )

        # Invoke the base-class implementation:
        super().mouseMoveEvent(event)

    # Mouse-release event handler:
    def mouseReleaseEvent(self, event, /):

        # If a transient connection isn't being drawn, return:
        if  not self._transient.active:
            super().mouseReleaseEvent(event)
            return

            # Get item under cursor:
        item = self.itemAt(event.scenePos(), self.views()[0].transform())
        if isinstance(item, Anchor):

            cpos = item.mapFromScene(event.scenePos())
            item.sig_anchor_clicked.emit(QPointF(0, cpos.y()))

        # Get the item under the cursor (this should now be a handle):
        item = self.itemAt(event.scenePos(), self.views()[0].transform())
        if (
            isinstance(item, Handle) and
            item is not self._transient.origin()
        ):
            self.addItem(Vector(origin=self._transient.origin(), target=item))

        # Base-class implementation:
        self.reset_transient()
        super().mouseReleaseEvent(event)

    # ------------------------------------------------------------------------------------------------------------------
    # Callback method(s) for user-driven events:

    # When the user clicks on a handle to begin drawing a connection:
    def begin_transient(self, handle: Handle):

        # Only initiate if the transient connection isn't already active:
        if  not self._transient.active:
            self._transient.active = True
            self._transient.origin = weakref.ref(handle)

    # Reset the transient connection:
    def reset_transient(self):

        # Reset the transient connection:
        self._transient.active = False
        self._transient.origin = None
        self._transient.target = None
        self._transient.vector.clear()

    # ------------------------------------------------------------------------------------------------------------------
    # Callback method(s) for actions from the context-menu:

    # When the user selects an item to create:
    def create_item(self, item_class: str, **kwargs):

        item_class = globals().get(item_class)

        if  item_class:
            item = item_class(**kwargs)
            item.setPos(self._cpos)

            self.addItem(item)
            self.sig_canvas_updated.emit(item)

    # When the user copies selected items:
    def clone_items(self):

        # Iterate over the items and copy them to the clipboard:
        for item in self.selectedItems():

            # Clone the item and add it to the clipboard:
            if  hasattr(item, 'clone'):
                clone = item.clone()
                clone.setPos(item.scenePos() + QPointF(20, 20))
                self.clipboard.append(clone)