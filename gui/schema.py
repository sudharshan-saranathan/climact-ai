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

# Creates a toolbar for a tree item:
def _tree_item_toolbar():

    _expander = QtWidgets.QFrame()
    _expander.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

    _toolbar = QtWidgets.QToolBar()
    _toolbar.setIconSize(QtCore.QSize(16, 16))
    _toolbar.setContentsMargins(0, 0, 0, 0)
    _toolbar.addWidget(_expander)

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

        categories = [cls.LABEL for cls in (FlowBases | DerivedStreams).values()]

        # Fetch all canvas items:
        vertex_list = canvas.fetch_items(Vertex)
        vector_list = canvas.fetch_items(Vector)

        # Clear roots:
        self._vertex_root.takeChildren()
        self._vector_root.takeChildren()

        # QTreeWidgetItem generator:
        def _tree_item(
                _parent: QtWidgets.QTreeWidgetItem,
                _vertex: Vertex | None = None
        ):
            _item = QtWidgets.QTreeWidgetItem(_parent)
            _item.setData(0, QtCore.Qt.ItemDataRole.UserRole, _vertex)
            _item.setText(0, _vertex.property('label'))
            _item.setIcon(0, _vertex.icon())
            return _item

        for vertex in vertex_list:

            item = _tree_item(self._vertex_root, vertex)
            tool = _tree_item_toolbar()
            item.setExpanded(True)

            tool.addAction(qta.icon('mdi.plus', color='#efefef'), 'Add', vertex.create_parameter)
            tool.addAction(qta.icon('mdi.delete', color='red'), 'Delete', vertex.delete)

            for param in vertex.connections.par.keys():
                _item = QtWidgets.QTreeWidgetItem(item)
                _item.setText(0, param)
                _item.setData(0, QtCore.Qt.ItemDataRole.UserRole, param)

            # Install the toolbar:
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

        # Update the connection's name:
        if  isinstance(
                vector := item.data(0, QtCore.Qt.ItemDataRole.UserRole),
                Vector
        ):
            vector.setProperty('label', item.text(0))
            vector.update()