# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: tree
# Description: A tree view widget for displaying hierarchical items in a schematic.
# ----------------------------------------------------------------------------------------------------------------------

from PySide6 import QtCore
from PySide6 import QtWidgets

from apps.schema.canvas import Canvas
from apps.schema.vector import Vector
from apps.schema.vertex import Vertex

# QtAwesome:
import qtawesome as qta

class TreeItemToolBar(QtWidgets.QToolBar):

    # Signal:
    sig_action_triggered = QtCore.Signal(str)

    # Default constructor:
    def __init__(self, item, parent = None):

        # Base-class initialization:
        super().__init__(parent)
        super().setStyleSheet("QToolBar QToolButton {margin: 2px; padding: 0px;}")

        # Expander:
        self._wide = QtWidgets.QWidget(self)
        self._wide.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self._wide.setStyleSheet("background: transparent;")
        self.addWidget(self._wide)

        self.setIconSize(QtCore.QSize(16, 16))
        self.addAction(qta.icon('mdi.tools' , color='#efefef'), 'Configure', item.configure)
        self.addAction(qta.icon('mdi.delete', color='#db5461'), 'Delete'   , )

class Tree(QtWidgets.QTreeWidget):

    # Default constructor:
    def __init__(self, parent: QtWidgets.QWidget | None = None):

        # Base-class initialization:
        super().__init__(parent)

        # Set properties:
        self.setColumnCount(2)
        self.setIndentation(32)
        self.setHeaderLabels(['Item', 'Actions'])
        self.header().setDefaultAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Stretch)

    # Method to create a vertex-QTreeWidgetItem:
    @staticmethod
    def create_vertex_item(vertex):

        vertex_item = QtWidgets.QTreeWidgetItem()
        vertex_item.setText(0, f"➤ {vertex.property('label')}")
        vertex_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, vertex)

        return vertex_item

    # Method to create a stream-QTreeWidgetItem:
    @staticmethod
    def create_stream_item(stream):

        stream_item = QtWidgets.QTreeWidgetItem()
        stream_item.setText(0, f"➤ {stream.property('label')}")
        stream_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, stream)

        return stream_item

    # Method to create a vector-QTreeWidgetItem:
    @staticmethod
    def create_vector_item(vector):

        vector_item = QtWidgets.QTreeWidgetItem()
        vector_item.setText(0, f"➤ {vector.property('label')}")
        vector_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, vector)

        return vector_item

    # Reload method:
    def reload(self, canvas: Canvas):

        # Clear the tree:
        self.clear()

        # Create top-level items:
        vertex_root = QtWidgets.QTreeWidgetItem(self)
        vertex_line = QtWidgets.QTreeWidgetItem(self)
        stream_root = QtWidgets.QTreeWidgetItem(self)
        stream_line = QtWidgets.QTreeWidgetItem(self)
        vector_root = QtWidgets.QTreeWidgetItem(self)

        vertex_root.setText(0, 'Vertices')
        stream_root.setText(0, 'Streams')
        vector_root.setText(0, 'Connectors')
        vertex_root.setIcon(0, qta.icon('ph.git-commit-fill', color='pink'))
        stream_root.setIcon(0, qta.icon('ph.flow-arrow-fill', color='cyan'))
        vector_root.setIcon(0, qta.icon('ph.path-fill', color='#ffcb00'))
        vertex_root.setFlags(vertex_root.flags() & ~QtCore.Qt.ItemFlag.ItemIsSelectable)
        stream_root.setFlags(stream_root.flags() & ~QtCore.Qt.ItemFlag.ItemIsSelectable)
        vector_root.setFlags(vector_root.flags() & ~QtCore.Qt.ItemFlag.ItemIsSelectable)
        vertex_line.setFlags(vertex_line.flags() & ~QtCore.Qt.ItemFlag.ItemIsSelectable)
        stream_line.setFlags(stream_line.flags() & ~QtCore.Qt.ItemFlag.ItemIsSelectable)

        # Fetch all canvas items:
        vertex_list = canvas.fetch_items(Vertex)
        vector_list = canvas.fetch_items(Vector)

        for vertex in vertex_list:
            vertex_item = self.create_vertex_item(vertex)
            vertex_root.addChild(vertex_item)

            self.setItemWidget(vertex_item, 1, TreeItemToolBar(vertex, self))

        for vector in vector_list:
            vector_item = self.create_vector_item(vector)
            vector_root.addChild(vector_item)
            self.setItemWidget(vector_item, 1, TreeItemToolBar(vector, self))

        # Expand-all:
        self.expandItem(vertex_root)
        self.expandItem(vector_root)