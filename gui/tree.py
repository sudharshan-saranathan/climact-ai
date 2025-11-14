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
        self.setIndentation(23)
        self.setColumnCount(2)
        self.setColumnWidth(0, 300)

    # Reload method:
    def reload(self, canvas: Canvas):

        # Clear the tree:
        self.clear()

        # Create top-level items:
        vertex_root = QtWidgets.QTreeWidgetItem(self)
        vector_root = QtWidgets.QTreeWidgetItem(self)
        vertex_root.setText(0, 'Vertices')
        vector_root.setText(0, 'Connectors')
        vertex_root.setIcon(0, qta.icon('ph.git-commit-fill', color='#ffcb00'))
        vector_root.setIcon(0, qta.icon('ph.flow-arrow-fill', color='#ffcb00'))

        # Fetch all canvas items:
        vertex_list = canvas.fetch_items(Vertex)
        vector_list = canvas.fetch_items(Vector)

        for vertex in vertex_list:
            vertex_item = QtWidgets.QTreeWidgetItem(vertex_root)
            vertex_item.setText(0, vertex.property('label'))
            self.setItemWidget(vertex_item, 1, TreeItemToolBar(self))

        for vector in vector_list:
            vector_item = QtWidgets.QTreeWidgetItem(vector_root)
            vector_item.setText(0, vector.property('label'))
            self.setItemWidget(vector_item, 1, QtWidgets.QPushButton('Configure'))

        # Expand-all:
        self.expandItem(vertex_root)
        self.expandItem(vector_root)