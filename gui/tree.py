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

import qtawesome as qta

class TreeItemToolBar(QtWidgets.QToolBar):

    # Default constructor:
    def __init__(self, parent = None):

        # Base-class initialization:
        super().__init__(parent)

        # Expander:
        self._wide = QtWidgets.QWidget(self)
        self._wide.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
        self._wide.setStyleSheet("background: transparent;")
        self.addWidget(self._wide)

        self.setIconSize(QtCore.QSize(16, 16))
        self.addAction(qta.icon('ph.wrench-fill', color='#efefef'), 'Configure')
        self.addAction(qta.icon('ph.play-fill', color='#efefef'), 'Run')

class Tree(QtWidgets.QTreeWidget):

    # Default constructor:
    def __init__(self, parent: QtWidgets.QWidget | None = None):

        # Base-class initialization:
        super().__init__(parent)

        # Set properties:
        self.setHeaderHidden(True)
        self.setIndentation(28)
        self.setColumnCount(2)
        self.setColumnWidth(0, 200)

    # Method to create a vertex-QTreeWidgetItem:
    def create_vertex_item(self, vertex):

        vertex_item = QtWidgets.QTreeWidgetItem()
        vertex_item.setText(0, vertex.property('label'))
        vertex_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, vertex)

        return vertex_item

    # Method to create a stream-QTreeWidgetItem:
    def create_stream_item(self, stream):

        stream_item = QtWidgets.QTreeWidgetItem()
        stream_item.setText(0, stream.property('label'))
        stream_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, stream)
        self.setItemWidget(stream_item, 1, TreeItemToolBar(self))

        return stream_item

    # Method to create a vector-QTreeWidgetItem:
    def create_vector_item(self, vector):

        vector_item = QtWidgets.QTreeWidgetItem()
        vector_item.setText(0, vector.property('label'))
        vector_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, vector)
        self.setItemWidget(vector_item, 1, TreeItemToolBar(self))

        return vector_item

    # Reload method:
    def reload(self, canvas: Canvas):

        # Clear the tree:
        self.clear()

        # Create top-level items:
        vertex_root = QtWidgets.QTreeWidgetItem(self)
        stream_root = QtWidgets.QTreeWidgetItem(self)
        vector_root = QtWidgets.QTreeWidgetItem(self)

        vertex_root.setText(0, 'Vertices')
        stream_root.setText(0, 'Streams')
        vector_root.setText(0, 'Connectors')
        vertex_root.setIcon(0, qta.icon('ph.git-commit-fill', color='pink'))
        stream_root.setIcon(0, qta.icon('ph.flow-arrow-fill', color='cyan'))
        vector_root.setIcon(0, qta.icon('ph.path-fill', color='#ffcb00'))

        # Fetch all canvas items:
        vertex_list = canvas.fetch_items(Vertex)
        vector_list = canvas.fetch_items(Vector)

        for vertex in vertex_list:
            vertex_item = self.create_vertex_item(vertex)
            vertex_root.addChild(vertex_item)
            self.setItemWidget(vertex_item, 1, TreeItemToolBar(self))

        for vector in vector_list:
            vector_item = self.create_vector_item(vector)
            vector_root.addChild(vector_item)
            self.setItemWidget(vector_item, 1, TreeItemToolBar(self))

        # Expand-all:
        self.expandItem(vertex_root)
        self.expandItem(vector_root)