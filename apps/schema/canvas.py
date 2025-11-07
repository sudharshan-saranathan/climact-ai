# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: canvas
# Description: A QGraphicsScene-based canvas for the Climact application
# ----------------------------------------------------------------------------------------------------------------------

# Imports:
import enum
import types

# PySide6
from PySide6.QtCore import QRectF, Qt, QPointF, QObject, Signal
from PySide6.QtGui import QBrush, QColor, QKeySequence, QTransform
from PySide6.QtWidgets import QGraphicsScene, QMenu, QWidget, QGraphicsItem, QGraphicsObject

# Qt-awesome:
import qtawesome as qta

# Apps:
from apps.schema.anchor import Anchor
from apps.schema.handle import Handle, HandleRole
from apps.schema.vector import Vector
from apps.schema.vertex import Vertex, VertexOpts
from conf import GlobalConfig

class SearchFilter(enum.Enum):
    NAME = enum.auto()
    SPOS = enum.auto()

# Canvas class: A QGraphicsScene-based canvas for the Climact application
class Canvas(QGraphicsScene):

    # Signals:
    sig_display_config = Signal(QWidget)

    # Default constructor:
    def __init__(self, parent: QObject | None = None, **kwargs):

        # Base-class initialization:
        super().__init__(parent)

        # Set class-level attribute(s):
        self.setBackgroundBrush(QBrush(QColor(0xefefef), Qt.BrushStyle.DiagCrossPattern))
        self.setSceneRect(QRectF(0, 0, 10000, 10000))

        # Transient connector:
        self._transient = types.SimpleNamespace(
            active = False,
            origin = None,
            target = None,
            vector = Vector(),
        )
        self.addItem(self._transient.vector)

        # Initialize context-menu:
        self._cpos = QPointF()
        self._menu = self._init_context_menu()

    # Initialize the context menu and add appropriate actions:
    def _init_context_menu(self):

        # Instantiate a menu:
        _menu = QMenu()

        # Add item sub-menu:
        _submenu = _menu.addMenu("Add")
        _vertex = _submenu.addAction(
            qta.icon("mdi.memory", color="teal"),
            "Vertex" , QKeySequence("Ctrl + Shift + V"),
            lambda: self.create_item(
                'Vertex',
                name = "Process",
                icon = GlobalConfig["root"] + "/rss/icons/pack-three/node.svg"
            )
        )

        _router = _submenu.addAction(
            qta.icon("mdi.call-split", color="darkred"),
            "Router", QKeySequence("Ctrl + Shift + |"),
            lambda: self.create_item(
                'Vertex',
                name = "Router",
                icon = GlobalConfig["root"] + "/rss/icons/pack-two/split.svg"
            )
        )

        _vertex.setIconVisibleInMenu(True); _vertex.setShortcutVisibleInContextMenu(True)
        _router.setIconVisibleInMenu(True); _router.setShortcutVisibleInContextMenu(True)

        # Schematic management:
        _menu.addSeparator()
        _open = _menu.addAction(qta.icon('mdi.file', color='orange'), 'Import', QKeySequence.StandardKey.Open)
        _save = _menu.addAction(qta.icon('mdi.content-save', color='green'), 'Export', QKeySequence.StandardKey.Save)
        _wipe = _menu.addAction(qta.icon('mdi.eraser', color='red'), 'Clear', QKeySequence("Ctrl + Delete"))
        _menu.addSeparator()

        # Schematic management:
        _copy = _menu.addAction(qta.icon('mdi.content-copy' , color='#62466b'), 'Copy', QKeySequence.StandardKey.Copy)
        _past = _menu.addAction(qta.icon('mdi.content-paste', color='blue') , 'Paste', QKeySequence.StandardKey.Paste)
        _undo = _menu.addAction(qta.icon('mdi.undo', color='purple'), 'Undo', QKeySequence.StandardKey.Undo)
        _redo = _menu.addAction(qta.icon('mdi.redo', color='purple'), 'Redo', QKeySequence.StandardKey.Redo)
        _menu.addSeparator()

        # Set icon and shortcut visibility in menu and context menu:
        _open.setIconVisibleInMenu(True); _open.setShortcutVisibleInContextMenu(True)
        _save.setIconVisibleInMenu(True); _save.setShortcutVisibleInContextMenu(True)
        _wipe.setIconVisibleInMenu(True); _wipe.setShortcutVisibleInContextMenu(True)
        _copy.setIconVisibleInMenu(True); _copy.setShortcutVisibleInContextMenu(True)
        _past.setIconVisibleInMenu(True); _past.setShortcutVisibleInContextMenu(True)
        _undo.setIconVisibleInMenu(True); _undo.setShortcutVisibleInContextMenu(True)
        _redo.setIconVisibleInMenu(True); _redo.setShortcutVisibleInContextMenu(True)

        # Return the menu instance:
        return _menu

    # ------------------------------------------------------------------------------------------------------------------
    # Reimplementation of virtual event-handler(s) of Canvas's base-class (QGraphicsScene):
    # Mouse-move event handler:
    def mouseMoveEvent(self, event, /):

        # Base-class implementation:
        super().mouseMoveEvent(event)

        # Update the transient connection (if active):
        if  self._transient.active and self._transient.origin:

            opos = self._transient.origin.scenePos()
            tpos = event.scenePos()

            self._transient.vector.on_path_updated(opos, tpos)
            self.update(self.visible_region())

    # Mouse-release event handler:
    def mouseReleaseEvent(self, event, /):

        # If a transient connection isn't being drawn, return:
        if  not self._transient.active:
            super().mouseReleaseEvent(event)
            return

        # Get item under cursor:
        item = self.itemAt(event.scenePos(), self.views()[0].transform())
        if  isinstance(item, Anchor):
            cpos = item.mapFromScene(event.scenePos())
            item.sig_anchor_clicked.emit(QPointF(0, cpos.y()))

        # Get the item under the cursor (this should now be a handle):
        if  isinstance(item := self.itemAt(event.scenePos(), QTransform()), Handle):

            # Create a new connection:
            self.create_connection(
                self._transient.origin,
                item
            )

        # Base-class implementation:
        super().mouseReleaseEvent(event)
        self.reset_transient()

    # Context-menu event handler:
    def contextMenuEvent(self, event, /):

        # Show the context menu:
        self._cpos = event.scenePos()
        self._menu.exec(event.screenPos())

    # ------------------------------------------------------------------------------------------------------------------

    # ------------------------------------------------------------------------------------------------------------------
    # Callback methods for user-driven events:

    # Begin drawing the transient connection from the clicked handle:
    def begin_transient(self, handle: Handle):

        if  not self._transient.active:
            self._transient.active = True
            self._transient.origin = handle

    # Reset the transient connection:
    def reset_transient(self):

        self._transient.active = False
        self._transient.origin = None
        self._transient.target = None
        self._transient.vector.clear()

    # Returns the visible portion of the scene:
    def visible_region(self):

        viewer = self.views()[0]
        bounds = viewer.viewport().rect()

        return viewer.mapToScene(bounds).boundingRect()

    # ------------------------------------------------------------------------------------------------------------------
    # These methods are used to manage items on the canvas, including creation, modification, and deletion. These are
    # exposed as 'tools' to LLMs and are therefore directly called by the LLM to manage the schematic independent of the
    # user.

    # Find an item using its object-name:
    def find(
            self,
            criterion: SearchFilter,        # SearchFilter.NAME or SearchFilter.SPOS
            argument: str | QPointF,        # The value to match: str or QPointF
            item_class = QGraphicsObject    # The class of the object
    ) -> QGraphicsObject | None:

        """
        This method searches for an item on the canvas using its 'name' property. If found, a reference to the item is
        returned; otherwise, None is returned. This method cannot be invoked through an LLM.

        :param criterion    : The name of the item to search for, identified through its 'name' property.
        :param argument     : The argument value to search for (name as str or spos as QPointF).
        :param item_class   : The class of the item to search for (Optional, default is QGraphicsObject).
        :return: item_class
        """

        # Define the search domain as those items with
        items = [
            item for item in self.items()
            if (
                    item.isVisible() and
                    isinstance(item, item_class) and
                    (
                        item.property('name') == argument if criterion == SearchFilter.NAME else
                        item.contains(argument)
                    )
            )
        ]

        # If multiple items match the criterion, return the first one:
        return items[0] if len(items) else None

    # Returns the names of vertices currently on the canvas:
    def vertex_labels(self):
        """
        This method returns the names of all vertices in the canvas. It can be used by an LLM to get an overview of the
        current schematic and determine the function of each vertex. For example, a vertex called 'Turbine' is likely
        to be a component in a power generation system.
        :return: List
        """

        return [
            item.property('name') for item in self.items()
            if isinstance(item, Vertex)
        ]

    # Create and add an item to the canvas:
    def create_item(self, item_class: str, **kwargs):
        """
        Create and add an item (a QGraphicsObject subclass) to this canvas (a QGraphicsScene subclass). The class of the
        item is required and must be a string that matches the name of a class in the global namespace. Additional
        keyword arguments such as 'xpos', 'ypos', 'name', and 'icon' are passed to the item's constructor to customize
        it.

        :param item_class: The class of the item to create (e.g., 'Vertex', 'Vector').
        :param kwargs: Additional parameters for item creation.
        :return: Reference to the created item.
        """

        # Unpack keyword arguments:
        xpos = float(kwargs.get("xpos", self._cpos.x()))
        ypos = float(kwargs.get("ypos", self._cpos.y()))
        name = kwargs.get("name", "Generic")
        icon = kwargs.get("icon", GlobalConfig["root"] + "/rss/icons/pack-three/node.svg")

        # Create the item and add it to the scene:
        item = globals().get(item_class)(icon = icon, name = name)
        item.setPos(QPointF(xpos, ypos))
        self.addItem(item)

        # Center the view on the created item:
        self.views()[0].centerOn(item)

        # Return a reference to the created item:
        return {
            "item"      : item.to_json() if hasattr(item, 'to_json') else str(),
            "status"    : f"success",
            "message"   : f"Successfully created a '{item_class}' named '{name}'.",
        }

    # Create a new input or output handle at the specified position:
    def create_handle(self, name: str, role: str, **kwargs):
        """
        This method creates a new input or output handle on the specified vertex at the given position. The vertex is
        first located using its name, and if found, the handle is created at the specified coordinates.

        :param name:    Name of the vertex where the handle should be created.
        :param role:    Role of the handle, either 'INP' or 'OUT'.
        :param kwargs:  Additional keyword arguments that are passed to the handle's constructor.
        :return: None
        """

        if  isinstance(vertex := self.find(name), Vertex):

            handle = vertex.create_handle(
                HandleRole.INP if role.lower() == 'inp' else HandleRole.OUT,
                QPointF(),
                **kwargs
            )

            return {
                "status"    : "success",
                "xpos"      : handle.pos().x(),
                "ypos"      : handle.pos().y(),
                "message"   : f"Successfully created a handle on vertex {vertex.property('name')}",
            }

        return {
            "status"    : "error",
            "message"   : f"Could not find a vertex named '{name}'.",
        }

    # Create a new connection between two handles:
    def create_connection(self, origin: Handle, target: Handle):
            """
            This method connects two handles with a vector. It ensures that the origin and target handles are valid,
            different, and have different roles (i.e., one is an input and the other is an output). If these
            conditions are met, a new vector is created to connect

            :param origin: Reference to the origin handle.
            :param target: Reference to the target handle.
            :return: None
            """

            # Check if the origin and target handles are valid and have different roles:
            if (
                origin and target and
                origin is not target and
                origin.property('role') != target.property('role')
            ):
                self.addItem(Vector(origin = origin, target = target))

            return {
                "status"    : "success",
                "message"   : f"Successfully created a connection between the specified handles.",
            }

    # List of functions that can be called by an LLM:
    def functions(self):

        return [
            self.create_item,
            self.create_handle,
            self.vertex_labels,
        ]