# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: config
# Description: Configuration utility for different QGraphicsObject-subclasses.
# ----------------------------------------------------------------------------------------------------------------------

# Import(s):
# PySide6:
from PySide6 import QtCore, QtGui, QtWidgets
import qtawesome as qta

# Climact submodule(s):
import util
from apps.stream.base import FlowBases
from apps.stream.derived import DerivedStreams
from obj.entity import EntityClass

# Page indices for the QStackedWidget:
PAGE_GENERAL = 0
PAGE_STREAMS = 1
PAGE_PARAMS = 2
PAGE_EQUATIONS = 3

class VertexConfig(QtWidgets.QDialog):
    """
    A configuration dialog for a Vertex object. It allows users to manage
    the vertex's label, streams (inputs/outputs), parameters, and equations.
    """
    # Default constructor:
    def __init__(self,
                 vertex: QtWidgets.QGraphicsObject,
                 parent: QtWidgets.QWidget | None = None):

        # Base-class initialization:
        super().__init__(parent)
        super().setProperty('vertex', vertex)
        super().setWindowTitle(f"Configure: {vertex.property('label')}")
        super().setMinimumSize(960, 640)

        # --- Widgets ---
        self._nav_tree = self._init_nav_tree()
        self._content_stack = QtWidgets.QStackedWidget(self)

        # --- Pages for Stacked Widget ---
        self._general_page = self._create_general_page()
        self._streams_page = self._create_streams_page()
        self._params_page = self._create_params_page()
        self._equations_page = self._create_equations_page()

        # Add pages to the stacked widget
        self._content_stack.addWidget(self._general_page)
        self._content_stack.addWidget(self._streams_page)
        self._content_stack.addWidget(self._params_page)
        self._content_stack.addWidget(self._equations_page)

        # --- Layout ---
        splitter = QtWidgets.QSplitter(QtCore.Qt.Orientation.Horizontal, self)
        splitter.addWidget(self._nav_tree)
        splitter.addWidget(self._content_stack)
        splitter.setContentsMargins(0, 0, 0, 0)
        splitter.setSizes([240, 720]) # Initial size ratio

        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(splitter)

        # --- Connections ---
        self._nav_tree.currentItemChanged.connect(self._on_nav_changed)
        self._nav_tree.setCurrentItem(self._nav_tree.topLevelItem(0)) # Select "General" by default

    def _init_nav_tree(self) -> QtWidgets.QTreeWidget:
        """Initializes the navigation tree on the left."""
        tree = QtWidgets.QTreeWidget()
        tree.setHeaderHidden(True)
        tree.setIndentation(10)

        # Add root items with icons
        general_item = QtWidgets.QTreeWidgetItem(tree, ["General"])
        general_item.setIcon(0, qta.icon('mdi.tune', color='#efefef'))
        general_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, PAGE_GENERAL)

        streams_item = QtWidgets.QTreeWidgetItem(tree, ["Streams"])
        streams_item.setIcon(0, qta.icon('mdi.water', color='#efefef'))
        streams_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, PAGE_STREAMS)

        params_item = QtWidgets.QTreeWidgetItem(tree, ["Parameters"])
        params_item.setIcon(0, qta.icon('mdi.variable', color='#efefef'))
        params_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, PAGE_PARAMS)

        equations_item = QtWidgets.QTreeWidgetItem(tree, ["Equations"])
        equations_item.setIcon(0, qta.icon('mdi.function-variant', color='#efefef'))
        equations_item.setData(0, QtCore.Qt.ItemDataRole.UserRole, PAGE_EQUATIONS)

        return tree

    def _create_general_page(self) -> QtWidgets.QWidget:
        """Creates the 'General' configuration page."""
        vertex = self.property('vertex')
        page = QtWidgets.QWidget()
        form_layout = QtWidgets.QFormLayout(page)
        form_layout.setContentsMargins(16, 16, 16, 16)
        form_layout.setSpacing(10)

        form_layout.addRow('Vertex Label:', QtWidgets.QLineEdit(vertex.property('label')))
        form_layout.addRow('Group:', QtWidgets.QLabel(vertex.property('group') or 'N/A'))

        return page

    def _create_streams_page(self) -> QtWidgets.QWidget:
        """Creates the 'Streams' configuration page with tables for inputs and outputs."""
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(8)

        # Input Streams Table
        inp_group = QtWidgets.QGroupBox("Input Streams")
        inp_layout = QtWidgets.QVBoxLayout(inp_group)
        self._inp_table = self._create_stream_table()
        inp_layout.addWidget(self._inp_table)
        layout.addWidget(inp_group)

        # Output Streams Table
        out_group = QtWidgets.QGroupBox("Output Streams")
        out_layout = QtWidgets.QVBoxLayout(out_group)
        self._out_table = self._create_stream_table()
        out_layout.addWidget(self._out_table)
        layout.addWidget(out_group)

        return page

    def _create_stream_table(self) -> QtWidgets.QTableWidget:
        """Creates a boilerplate QTableWidget for streams."""
        table = QtWidgets.QTableWidget()
        headers = ["Label", "Type", "Value", "Units", "Time Function"]
        table.setColumnCount(len(headers))
        table.setHorizontalHeaderLabels(headers)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.ResizeMode.Stretch)
        table.horizontalHeader().setStretchLastSection(True)
        return table

    def _create_params_page(self) -> QtWidgets.QWidget:
        """Creates the 'Parameters' configuration page."""
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        # This can be a QTableWidget similar to streams or a different interface
        label = QtWidgets.QLabel("Parameter configuration will be implemented here.")
        label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(label)
        return page

    def _create_equations_page(self) -> QtWidgets.QWidget:
        """Creates the 'Equations' configuration page with a text editor."""
        page = QtWidgets.QWidget()
        layout = QtWidgets.QVBoxLayout(page)
        layout.setContentsMargins(0, 0, 0, 0)

        # A simple text editor for now. This can be replaced with a syntax-highlighting editor.
        editor = QtWidgets.QTextEdit()
        editor.setPlaceholderText("Define equations relating inputs, outputs, and parameters.\nExample: out1 = inp1 * param1")
        layout.addWidget(editor)
        return page

    def _populate_streams_page(self):
        """Populates the input and output tables with data from the vertex."""
        vertex = self.property('vertex')
        if inp_handles := vertex[EntityClass.INP]:
            self._populate_table(self._inp_table, inp_handles)

        if out_handles := vertex[EntityClass.OUT]:
            self._populate_table(self._out_table, out_handles)

    def _populate_table(self, table: QtWidgets.QTableWidget, handles: dict):
        """Helper method to fill a stream table with handle data."""
        table.setRowCount(len(handles))
        stream_types = [
            (qta.icon(cls.ICON, color=cls.COLOR), cls.LABEL) for cls in (FlowBases | DerivedStreams).values()
        ]

        for row, handle in enumerate(handles.keys()):
            # Column 0: Label
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(handle.property('label')))

            # Column 1: Type (ComboBox)
            combo = util.combobox(self)

            # TODO: Set the current stream type if available on the handle
            table.setCellWidget(row, 1, combo)

            # Columns 2-4: Value, Units, Time Function (LineEdits)
            table.setCellWidget(row, 2, QtWidgets.QLineEdit())
            table.setCellWidget(row, 3, QtWidgets.QLineEdit())
            table.setCellWidget(row, 4, QtWidgets.QLineEdit())

    def _on_nav_changed(self, current: QtWidgets.QTreeWidgetItem, previous: QtWidgets.QTreeWidgetItem):
        """Slot to switch pages in the QStackedWidget."""
        if not current: return

        page_index = current.data(0, QtCore.Qt.ItemDataRole.UserRole)
        self._content_stack.setCurrentIndex(page_index)

    def exec(self):
        """Overrides exec to populate data before showing the dialog."""
        self._populate_streams_page()
        # TODO: Add calls to populate other pages (parameters, equations)
        super().exec()