# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: config
# Description: Configuration utility for different QGraphicsObject-subclasses.
# ----------------------------------------------------------------------------------------------------------------------

# Import(s):
# PySide6:
from PySide6 import QtCore, QtGui
from PySide6 import QtWidgets

import qtawesome as qta
import pyqtgraph as pg

import util
from apps.stream.base    import FlowBases
from apps.stream.derived import DerivedStreams

class VertexConfig(QtWidgets.QDialog):

    # Default constructor:
    def __init__(self,
                 vertex: QtWidgets.QGraphicsObject,
                 parent: QtWidgets.QWidget | None = None):

        # Base-class initialization:
        super().__init__(parent)
        super().setProperty('vertex', vertex)
        super().setFixedSize(1440, 900)

        # Define widgets:
        self._container = self._init_ctrl()

        # Tree-widget to list inputs, outputs, and params:
        self._tree = self._init_tree()
        self._form = self._init_form()
        self._form.addRow('Vertex:' , QtWidgets.QLabel(vertex.property('label')))
        self._form.addRow('Group:'  , QtWidgets.QLabel(vertex.property('group') or 'N/A'))
        self._form.addRow('Streams:', self._tree)

        # Initialize root-items:
        self._init_root()

        # Initialize layout:
        self._layout = QtWidgets.QGridLayout(self)
        self._layout.setSpacing(2)
        self._layout.setContentsMargins(0, 0, 0, 0)
        self._layout.addLayout(self._form, 0, 0)
        self._layout.addWidget(pg.PlotWidget(background = '#ffffff'), 0, 1, 2, 1)

        self._layout.setRowStretch(0, 5)
        self._layout.setColumnStretch(1, 5)

    # Initialize the control widget:
    @classmethod
    def _init_ctrl(cls):

        _frame = QtWidgets.QFrame()
        _frame.setLayout(_form := cls._init_form())

        _form.addRow('Start:', QtWidgets.QLineEdit())
        _form.addRow('Final:', QtWidgets.QLineEdit())

        return _frame

    @classmethod
    def _init_tree(cls):

        _tree = QtWidgets.QTreeWidget()
        _tree.setColumnCount(2)
        _tree.setIndentation(16)
        _tree.setHeaderHidden(True)
        _tree.setColumnWidth(0, 150)
        _tree.setMinimumWidth(320)

        return _tree

    @classmethod
    def _init_form(cls):

        # Form Layout for selecting the category of input and output streams:
        _form = QtWidgets.QFormLayout()
        _form.setVerticalSpacing(8)
        _form.setContentsMargins(4, 24, 4, 24)
        _form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        _form.setFieldGrowthPolicy(QtWidgets.QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow)

        return _form

    # Initialize root items:
    def _init_root(self):

        def _expander():
            widget = QtWidgets.QFrame(self)
            widget.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
            return widget

        def _toolbar():
            bar = QtWidgets.QToolBar("N/A", self)
            bar.setIconSize(QtCore.QSize(20, 20))
            bar.addWidget(_expander())
            bar.addAction(qta.icon('mdi.minus', color='#efefef'), 'Delete')
            bar.addAction(qta.icon('mdi.plus' , color='#ffcb00'), 'Add')
            return bar

        self._inp_root = QtWidgets.QTreeWidgetItem(self._tree, ['Input', '', ''])
        self._out_root = QtWidgets.QTreeWidgetItem(self._tree, ['Output', '', ''])
        self._par_root = QtWidgets.QTreeWidgetItem(self._tree, ['Parameters', '', ''])
        self._eqn_root = QtWidgets.QTreeWidgetItem(self._tree, ['Equations', '', ''])

        self._tree.setItemWidget(self._par_root, 1, _toolbar())
        self._tree.setItemWidget(self._eqn_root, 1, _toolbar())

    def _update_tree(self):

        # Clear the root:
        self._inp_root.takeChildren()
        self._out_root.takeChildren()
        self._par_root.takeChildren()

        # Method to populate a root item:
        def _populate(root: QtWidgets.QTreeWidgetItem, items: list[QtWidgets.QGraphicsObject]):

            # Add each handle as a child item:
            for handle in items:
                item = QtWidgets.QTreeWidgetItem(root)
                item.setText(0, handle.property('label'))
                item.setData(0, QtCore.Qt.ItemDataRole.UserRole, handle)
                item.setFlags(item.flags() |  QtCore.Qt.ItemFlag.ItemIsEditable)

                streams = util.combobox(
                    self,
                    actions = [(cls.ICON, cls.COLOR, cls.LABEL) for cls in (FlowBases | DerivedStreams).values()]
                )

                # Display stream-grid for input and output handles:
                self._tree.setItemWidget(item, 1, streams)

        # Populate the tree with inputs, outputs, and parameters:
        _populate(self._inp_root, self.property('vertex')._objects.inp)
        _populate(self._out_root, self.property('vertex')._objects.out)

        # Expand the tree:
        self._tree.expandAll()

    # Reimplementation of exec():
    def exec(self):

        # First, update the tree:
        self._update_tree()

        # Invoke the base-class implementation:
        super().exec()
