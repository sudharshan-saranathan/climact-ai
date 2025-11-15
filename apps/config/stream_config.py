# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: stream_config
# Description: Configuration utility for resources.
# ----------------------------------------------------------------------------------------------------------------------

from typing import List, Type, Dict, Any

# Import(s):
# PySide6:
from PySide6 import QtCore, QtGui
from PySide6 import QtWidgets

# Qtawesome
import qtawesome as qta

# Class StreamConfigWidget: A tree widget for managing resource types.
class StreamConfigWidget(QtWidgets.QTreeWidget):

    # Default constructor:
    def __init__(self, parent: QtWidgets.QWidget | None = None):

        # Base-class initialization:
        super().__init__(parent)

        # Set properties:
        self.setColumnCount(2)
        self.setIndentation(8)
        self.setHeaderHidden(True)
        self.setColumnWidth(0, 150)

        # Create top-level items:
        self._phy_root = QtWidgets.QTreeWidgetItem(self); self._phy_root.setText(0, 'Physical')
        self._raw_root = QtWidgets.QTreeWidgetItem(self); self._raw_root.setText(0, 'Material')
        self._fue_root = QtWidgets.QTreeWidgetItem(self); self._fue_root.setText(0, 'Fuel')
        self._eco_root = QtWidgets.QTreeWidgetItem(self); self._eco_root.setText(0, 'Economic')
        self._ghg_root = QtWidgets.QTreeWidgetItem(self); self._ghg_root.setText(0, 'Emission')
        self._new_root = QtWidgets.QTreeWidgetItem(self); self._new_root.setText(0, 'Custom')

        # Attach button to `new_root`:
        self._attach_add_button(self._new_root)
        self._attach_add_button(self._fue_root)
        self._attach_add_button(self._raw_root)
        self._populate_default_streams()

    # Attach button to the `custom` branch:
    def _attach_add_button(self, parent_item: QtWidgets.QTreeWidgetItem) -> None:

        # Initialize expander:
        expander = QtWidgets.QFrame(self)
        expander.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        toolbar = QtWidgets.QToolBar()
        toolbar.addWidget(expander)
        toolbar.setIconSize(QtCore.QSize(20, 20))
        toolbar.setStyleSheet('QToolBar {padding: 2px;} QToolBar QToolButton { margin: 0px; padding: 0px; }')

        if  parent_item is self._raw_root:
            toolbar.addAction(
                qta.icon('mdi.plus', color='#ffcb00'), 'Add',
                self._define_raw_material
            )

        if  parent_item is self._fue_root:
            toolbar.addAction(
                qta.icon('mdi.plus', color='#ffcb00'), 'Add',
                self._define_fuel_type
            )

        if  parent_item is self._new_root:
            toolbar.addAction(
                qta.icon('mdi.plus', color='#ffcb00'), 'Add',
                self._define_raw_material if parent_item == self._raw_root else self._define_new_resource
            )

        # Place the widget into column 1 of the specified item
        self.setItemWidget(parent_item, 1, toolbar)

    def _populate_default_streams(self) -> None:
        """Create tree items for the default streams using their metadata."""
        from apps.stream import default as streams

        physical_keys = {"mass", "flow", "energy", "electricity"}
        economic_keys = {"opex", "capex" , "revenue"}
        emission_keys = {"GHG"  , "SOx", "NOx", "pm2.5", "pm10"}

        for cls in streams.DEFAULT_STREAMS.values():
            meta = cls.metadata()
            key = meta["key"]
            label = meta.get("label", key.title())
            unit = meta.get("unit", "")
            icon_name = meta.get("icon", "")
            color = meta.get("color", "")

            # decide parent
            if  key in physical_keys:
                parent = self._phy_root
            elif key in economic_keys:
                parent = self._eco_root
            elif key in emission_keys:
                parent = self._ghg_root
            else:
                parent = self._new_root

            item = QtWidgets.QTreeWidgetItem(parent)
            item.setText(0, label)
            item.setText(1, unit)
            item.setIcon(0, qta.icon(icon_name, color=color))

    # Method to compose a new stream selection item:
    def _define_new_resource(self):

        # Import default streams:
        from apps.stream import default as streams

        # Create a child under the "Custom" root
        item = QtWidgets.QTreeWidgetItem(self._new_root)
        item.setText(0, "New Resource")
        item.setIcon(0, qta.icon('mdi.cube', color='#ffcb00'))
        item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)

        # Create toolbar widget to hold icon actions
        toolbar = QtWidgets.QToolBar(self)
        toolbar.setIconSize(QtCore.QSize(18, 18))
        toolbar.setStyleSheet('QToolBar {padding: 2px;} QToolBar QToolButton { margin: 0px; padding: 0px; }')

        # Add one checkable action per default stream, store the stream key in action.data()
        for cls in streams.DEFAULT_STREAMS.values():

            meta = cls.metadata()
            key  = meta.get("key")
            name = meta.get("label", key.title())
            icon = meta.get("icon", "")
            color = meta.get("color", "")
            action = toolbar.addAction(qta.icon(icon, color=color), name)

            action.setToolTip(name)
            action.setCheckable(True)
            action.setData(key)

        # Place the toolbar widget into column 1 of the newly created item
        toolbar.addAction(qta.icon('mdi.close-circle', color='red'), 'Delete', )
        self.setItemWidget(item, 1, toolbar)
        self.editItem(item, 0)
        self._new_root.setExpanded(True)

    # Method to define a new fuel type:
    def _define_fuel_type(self):

        # Create a child under the "Fuel" root
        item = QtWidgets.QTreeWidgetItem(self._fue_root)
        item.setText(0, "New Fuel")
        item.setIcon(0, qta.icon('mdi.fuel', color='#ffcb00'))
        item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)

        # Create toolbar widget to hold icon actions
        toolbar = QtWidgets.QToolBar(self)
        toolbar.setIconSize(QtCore.QSize(18, 18))
        toolbar.setStyleSheet('QToolBar {padding: 2px;} QToolBar QToolButton { margin: 0px; padding: 0px; }')

        # Place the toolbar widget into column 1 of the newly created item
        toolbar.addAction(qta.icon('mdi.close-circle', color='red'), 'Delete', )
        self.setItemWidget(item, 1, toolbar)
        self.editItem(item, 0)
        self._fue_root.setExpanded(True)

    # Method to define a new raw material:
    def _define_raw_material(self):

        # Create a child under the "Custom" root
        item = QtWidgets.QTreeWidgetItem(self._raw_root)
        item.setText(0, "New Resource")
        item.setIcon(0, qta.icon('mdi.cube', color='#ffcb00'))
        item.setFlags(item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)

        # Create toolbar widget to hold icon actions
        toolbar = QtWidgets.QToolBar(self)
        toolbar.setIconSize(QtCore.QSize(18, 18))
        toolbar.setStyleSheet('QToolBar {padding: 2px;} QToolBar QToolButton { margin: 0px; padding: 0px; }')

        # Place the toolbar widget into column 1 of the newly created item
        toolbar.addAction(qta.icon('mdi.close-circle', color='red'), 'Delete', )
        self.setItemWidget(item, 1, toolbar)
        self.editItem(item, 0)
        self._raw_root.setExpanded(True)