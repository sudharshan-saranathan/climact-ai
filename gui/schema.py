# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: tree
# Description: A tree view widget for displaying hierarchical items in a schematic.
# ----------------------------------------------------------------------------------------------------------------------
from typing import Any

# PySide6:
from PySide6 import QtCore, QtGui
from PySide6 import QtWidgets
from pyqtgraph.parametertree.parameterTypes import action

from apps.schema.canvas import Canvas
from apps.schema.vector import Vector
from apps.schema.vertex import Vertex

# QtAwesome:
import qtawesome as qta

from obj.combo import ComboBox


# Creates a toolbar for a tree item:
def _tree_item_toolbar(
        widgets: list[QtWidgets.QWidget] | None = None,
        actions: list[QtGui.QAction] | None = None
):

    _expander = QtWidgets.QFrame()
    _expander.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

    _toolbar = QtWidgets.QToolBar()
    _toolbar.setIconSize(QtCore.QSize(16, 16))
    _toolbar.setContentsMargins(0, 0, 0, 0)
    _toolbar.addWidget(_expander)

    for _widget in widgets or []:
        _toolbar.addWidget(_widget)

    for _action in actions or []:
        _toolbar.addAction(_action)

    return _toolbar

# Tree widget showing the complete schematic, including vertices, streams, and vectors:
class Schema(QtWidgets.QTreeWidget):

    # Default constructor:
    def __init__(self, parent: QtWidgets.QWidget | None = None):

        # Base-class initialization:
        super().__init__(parent)

        # Set properties:
        self.setColumnCount(2)
        self.setIndentation(20)
        self.setHeaderHidden(True)
        self.setColumnWidth(1, 240)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)

        # Create root-level items:
        self._vertex_root = QtWidgets.QTreeWidgetItem(self); self._vertex_root.setIcon(0, qta.icon('ph.git-commit-fill', color='pink'))
        self._stream_root = QtWidgets.QTreeWidgetItem(self); self._stream_root.setIcon(0, qta.icon('ph.flow-arrow-fill', color='cyan'))
        self._vector_root = QtWidgets.QTreeWidgetItem(self); self._vector_root.setIcon(0, qta.icon('ph.path-fill', color='#ffcb00'))

        self._vertex_root.setText(0, 'Vertices')
        self._stream_root.setText(0, 'Streams')
        self._vector_root.setText(0, 'Vectors')

        # Connect signals:
        self.itemSelectionChanged.connect(self.on_item_selected)
        self.itemChanged.connect(self.on_item_changed)

    # Reload method:
    def reload(self, canvas: Canvas):

        from apps.stream.base    import FlowBases
        from apps.stream.derived import DerivedStreams

        actions = [
            (cls.ICON, cls.COLOR, cls.LABEL)
            for cls in (FlowBases | DerivedStreams).values()
        ]

        # Fetch all canvas items:
        objects = canvas.fetch_items((Vertex, Vector))

        # Clear roots:
        self._vertex_root.takeChildren()
        self._vector_root.takeChildren()

        # Add vertices to the tree:
        for _object in objects:

            item = QtWidgets.QTreeWidgetItem()
            item.setIcon(0, _object.icon() if hasattr(_object, 'icon') else QtGui.QIcon())
            item.setData(0, QtCore.Qt.ItemDataRole.UserRole, _object)
            item.setText(0, _object.property('label'))

            if  isinstance(_object, Vertex):

                tool = _tree_item_toolbar()
                tool.addAction(qta.icon('mdi.delete', color='red'), 'Delete')

                self._vertex_root.addChild(item)
                self.setItemWidget(item, 1, tool)

            elif isinstance(_object, Vector):

                tool = _tree_item_toolbar([cbox := ComboBox(actions = actions)])
                tool.addAction(qta.icon('mdi.delete', color='red'), 'Delete')

                item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)
                cbox.setCurrentText(_object.category())

                self._vector_root.addChild(item)
                self.setItemWidget(item, 1, tool)

        # Expand-all:
        self.expandItem(self._vertex_root)
        self.expandItem(self._vector_root)

    # Callback when an item is selected:
    def on_item_selected(self):

        # Fetch the associated schema item:
        item = self.currentItem()
        objs = item.data(0, QtCore.Qt.ItemDataRole.UserRole)
        if  hasattr(objs, 'highlight'):
            objs.highlight()

    # Callback when a connection is renamed:
    @staticmethod
    def on_item_changed(item: QtWidgets.QTreeWidgetItem, column: int):

        # Fetch the associated schema object:
        _object = item.data(0, QtCore.Qt.ItemDataRole.UserRole)

        # Update the connection's name:
        if  not column and isinstance(_object, Vector):
            _object.setProperty('label', item.text(0))
            _object.update()