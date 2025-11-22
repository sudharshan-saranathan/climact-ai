# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: stream_config
# Description: Configuration utility for resources.
# ----------------------------------------------------------------------------------------------------------------------

from typing import List, Type, Dict, Any

# Import(s):
# PySide6:
from PySide6 import QtCore
from PySide6 import QtWidgets

# Qtawesome
import qtawesome as qta

from apps.stream.params import ParamBases


# Helper to create an expander widget:
def _expander() -> QtWidgets.QWidget:
    expander = QtWidgets.QFrame()
    expander.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)
    return expander

# Dialog widget for new streams:
class CustomStreamDialog(QtWidgets.QDialog):

    # Default constructor:
    def __init__(self, parent: QtWidgets.QWidget | None = None):

        from apps.stream.base    import FlowBases
        from apps.stream.derived import DerivedStreams

        # Base-class initialization:
        super().__init__(parent)

        # Set properties:
        self.setWindowTitle('Define Custom Stream')

        # Toolbar factory:
        def _new_toolbar(icons: dict):

            toolbar = QtWidgets.QToolBar(self)
            toolbar.setIconSize(QtCore.QSize(20, 20))
            for key, cls in icons.items():
                icon  = getattr(cls, 'ICON', None)
                color = getattr(cls, 'COLOR', None)

                action = toolbar.addAction(qta.icon(icon, color=color), cls.metadata().get('label', key.title()))
                action.setCheckable(True)

            return toolbar

        form = QtWidgets.QFormLayout(self)
        form.setSpacing(4)
        form.setContentsMargins(8, 12, 8, 12)
        form.setLabelAlignment(QtCore.Qt.AlignmentFlag.AlignRight)

        form.addRow('Name:'    , QtWidgets.QLineEdit(self))
        form.addRow('Color:'   , QtWidgets.QLineEdit(self))
        form.addRow(''         , _new_toolbar(FlowBases))
        form.addRow('Category:', _new_toolbar(ParamBases))
        form.addRow(''         , _new_toolbar(DerivedStreams))

# Class StreamConfigWidget: A tree widget for managing resource types.
class StreamConfigWidget(QtWidgets.QTreeWidget):

    # Default constructor:
    def __init__(self, parent: QtWidgets.QWidget | None = None):

        # Base-class initialization:
        super().__init__(parent)

        # Set properties:
        self.setColumnCount(3)
        self.setIndentation(16)
        self.setMinimumWidth(360)
        self.setHeaderHidden(True)
        self.setColumnWidth(0, 180)
        self.setColumnWidth(1, 140)
        self.setColumnWidth(2, 40)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeMode.Fixed)
        self.header().setSectionResizeMode(1, QtWidgets.QHeaderView.ResizeMode.Stretch)

        # Create top-level items:
        self._flow_root = QtWidgets.QTreeWidgetItem(self); self._flow_root.setText(0, 'Flow Rates')
        self._pars_root = QtWidgets.QTreeWidgetItem(self); self._pars_root.setText(0, 'Parameters')
        self._derv_root = QtWidgets.QTreeWidgetItem(self); self._derv_root.setText(0, 'Derived')
        self._new_root  = QtWidgets.QTreeWidgetItem(self); self._new_root.setText (0, 'Custom')

        # Attach button to `new_root`:
        self._attach_add_button(self._new_root)
        self._init_basic()
        self.expandAll()

    # Attach button to the `custom` branch:
    def _attach_add_button(self, parent: QtWidgets.QTreeWidgetItem) -> None:

        # Initialize expander:
        expander = QtWidgets.QFrame(self)
        expander.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        toolbar = QtWidgets.QToolBar()
        toolbar.addWidget(expander)
        toolbar.setIconSize(QtCore.QSize(24, 24))
        toolbar.setProperty('parent', parent)

        if  parent is self._new_root:
            toolbar.addAction(qta.icon('mdi.plus', color='#ffcb00'), 'Add', lambda: self._define_new_stream(self._new_root))

        # Place the widget into column 1 of the specified item
        self.setItemWidget(parent, 2, toolbar)

    # Method to initialize primary streams:
    def _init_basic(self) -> None:

        # Import default streams:
        from apps.stream.base    import FlowBases
        from apps.stream.params  import ParamBases
        from apps.stream.derived import DerivedStreams

        # Define basic stream categories:
        flow_bases = [cls.metadata().get("key") for cls in FlowBases.values()]
        parameters = [cls.metadata().get("key") for cls in ParamBases.values()]

        # Add all flow and parameter classes to the tree:
        for name, cls in (FlowBases | ParamBases | DerivedStreams).items():

            key   = cls.metadata().get("key"  , name)
            icon  = cls.metadata().get("icon" , "")
            color = cls.metadata().get("color", "")
            label = cls.metadata().get("label", key.title())

            item = QtWidgets.QTreeWidgetItem(
                self._flow_root if key in flow_bases else (
                    self._pars_root if key in parameters else
                    self._derv_root
                )
            )

            item.setText(0, label)
            item.setIcon(0, qta.icon(icon, color=color))

            if  key in flow_bases + parameters:
                self.setItemWidget(item, 1, units := QtWidgets.QComboBox(self))
                units.addItems(cls.UNITS)
                units.setCurrentText(cls.DEFAULT or cls.UNITS[0])

            else:
                toolbar = QtWidgets.QToolBar(self)
                toolbar.setIconSize(QtCore.QSize(20, 20))
                for base in cls.__bases__:
                    icon  = getattr(base, 'ICON', None)
                    color = getattr(base, 'COLOR', None)
                    toolbar.addAction(qta.icon(icon, color=color), '')

                self.setItemWidget(item, 1, toolbar)

    # Method to compose a new stream selection item:
    def _define_new_stream(self, root: QtWidgets.QTreeWidgetItem):

        # Show dialog:
        dialog = CustomStreamDialog(self)
        dialog.exec()