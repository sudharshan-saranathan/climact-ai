# -
# Encoding: utf-8
# Module name: map
# Description: A widget for displaying the schematic's contents.
# ----------------------------------------------------------------------------------------------------------------------

from PySide6 import QtCore
from PySide6 import QtWidgets

# Climact submodule:
from apps.schema.vertex import Vertex
from apps.schema.vector import Vector
from apps.stream.base import FlowBases
from apps.stream.derived import DerivedStreams
from obj.combo import ComboBox
from obj.list import List

# QtAwesome submodule:
import qtawesome as qta

# Schematic view widget:
class Schematic(QtWidgets.QToolBox):

    # Default constructor:
    def __init__(self, parent: QtWidgets.QWidget | None = None):

        # Base-class initialization:
        super().__init__(parent)

        # List widgets:
        self._vertex = List(self)
        self._stream = List(self)
        self._vector = List(self)

        # Add sections:
        self.addItem(self._vertex, qta.icon('ph.git-commit-fill', color='pink'), "Vertices")
        self.addItem(self._stream, qta.icon('ph.flow-arrow-fill', color='cyan'), "Streams")
        self.addItem(self._vector, qta.icon('ph.path-fill', color='#ffcb00'), "Vectors")

    # Method to reload canvas contents:
    def reload(self, canvas):

        vertex_list = canvas.fetch_items(Vertex)
        vector_list = canvas.fetch_items(Vector)

        # Clear the list and add items:
        self._vertex.load(
            vertex_list,
            actions = [
                ('mdi.cog', '#efefef', 'Configure'),
                ('mdi.delete', 'red', 'Delete')
            ]
        )

        self._vector.load(
            vector_list,
            actions = [
                ('mdi.delete', 'red', 'Delete')
            ]
        )
