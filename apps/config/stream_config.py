# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: stream_config
# Description: Configuration utility for resources.
# ----------------------------------------------------------------------------------------------------------------------

# Import(s):
# PySide6:
from PySide6 import QtCore
from PySide6 import QtWidgets

# Qtawesome
import qtawesome as qta

PhysicalStreams = {
    'Mass'       :  {
        'unit' : 'kg',
        'icon' : 'mdi.weight-gram',
        'color': 'lightblue'
    },

    'Flow'       :  {
        'unit' : 'kg/s',
        'icon' : 'mdi.speedometer',
        'color': '#00aced'
    },

    'Energy'     :  {
        'unit' : 'kJ',
        'icon' : 'mdi.thermometer',
        'color': '#ffcb00'
    },

    'Electricity':  {
        'unit' : 'kW',
        'icon' : 'mdi.flash',
        'color': '#8c2b76'
    },
}

EmissionStreams = {
    'Carbon'     :  {
        'unit' : 'kg CO2-eq/kg',
        'icon' : 'mdi.alpha-c',
        'color': '#efefef'
    },

    'Sulphur'    :  {
        'unit' : 'kg SO2-eq/kg',
        'icon' : 'mdi.alpha-s',
        'color': '#efefef'
    },

    'Nitrogen'   :  {
        'unit' : 'kg NOx-eq/kg',
        'icon' : 'mdi.alpha-n',
        'color': '#efefef'
    },

    'PM 2.5'     :  {
        'unit' : 'kg PM2.5/kg',
        'icon' : 'mdi.circle-small',
        'color': '#efefef'
    },

    'PM 10'      :  {
        'unit' : 'kg PM10/kg',
        'icon' : 'mdi.circle-medium',
        'color': '#efefef'
    },
}

EconomicStreams = {

    'CapEx'     : {
        'unit' : 'INR/year',
        'icon' : 'mdi.cash',
        'color': 'lightgreen'
    },

    'OprEx'     :  {
        'unit' : 'INR/year',
        'icon' : 'mdi.account-cog',
        'color': 'red'
    },

    'Labour'    : {
        'unit' : '#',
        'icon' : 'mdi.account-multiple',
        'color': '#ffcb00'
    },

    'Land'     : {
        'unit' : 'sq.m',
        'icon' : 'mdi.island',
        'color': 'brown'
    }
}

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
        phy_root = QtWidgets.QTreeWidgetItem(self); phy_root.setText(0, 'Physical')
        eco_root = QtWidgets.QTreeWidgetItem(self); eco_root.setText(0, 'Economics')
        ghg_root = QtWidgets.QTreeWidgetItem(self); ghg_root.setText(0, 'Emissions')
        new_root = QtWidgets.QTreeWidgetItem(self); new_root.setText(0, 'Custom')

        for key, value in PhysicalStreams.items():
            item = QtWidgets.QTreeWidgetItem(phy_root, [key, ''])
            item.setText(0, key)
            item.setText(1, value['unit'])
            item.setIcon(0, qta.icon(value['icon'], color=value['color']))

        for key, value in EmissionStreams.items():
            item = QtWidgets.QTreeWidgetItem(ghg_root, [key, ''])
            item.setText(0, key)
            item.setText(1, value['unit'])
            item.setIcon(0, qta.icon(value['icon'], color=value['color']))

        for key, value in EconomicStreams.items():
            item = QtWidgets.QTreeWidgetItem(eco_root, [key, ''])
            item.setText(0, key)
            item.setText(1, value['unit'])
            item.setIcon(0, qta.icon(value['icon'], color=value['color']))

        # attach add button to root
        self._attach_add_button(new_root)

    # Attach button to the `custom` branch:
    def _attach_add_button(self, parent_item: QtWidgets.QTreeWidgetItem) -> None:

        # Initialize expander:
        expander = QtWidgets.QFrame(self)
        expander.setSizePolicy(QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Expanding)

        toolbar = QtWidgets.QToolBar()
        toolbar.addWidget(expander)
        toolbar.setIconSize(QtCore.QSize(20, 20))
        toolbar.setStyleSheet('QToolBar {padding: 2px;} QToolBar QToolButton { margin: 0px; padding: 0px; }')
        toolbar.addAction(qta.icon('mdi.plus', color='#ffcb00'), 'Add', lambda: self.define_new_composite(parent_item))

        # Place the widget into column 1 of the specified item
        self.setItemWidget(parent_item, 1, toolbar)

    # Add a new custom item:
    def define_new_composite(self, parent_item: QtWidgets.QTreeWidgetItem) -> None:

        # Expand the `custom` branch so the new item is visible:
        parent_item.setExpanded(True)

        # Create the new composite item and allow editing of its label:
        new_item = QtWidgets.QTreeWidgetItem(parent_item, ["New Resource", ""])
        new_item.setIcon(0, qta.icon('mdi.cube-outline', color='#ffcb00'))
        new_item.setFlags(new_item.flags() | QtCore.Qt.ItemFlag.ItemIsEditable)

        # Build a small toolbar with checkable actions for each non-composite resource
        toolbar = QtWidgets.QToolBar(self)
        toolbar.setIconSize(QtCore.QSize(18, 18))
        toolbar.setStyleSheet('QToolBar {padding: 2px;} QToolBar QToolButton { margin: 0px; padding: 2px; }')

        m_tool = toolbar.addAction(qta.icon('mdi.weight-gram', color='lightblue'), 'Mass')
        f_tool = toolbar.addAction(qta.icon('mdi.speedometer', color='#00aced'), 'Flow')
        e_tool = toolbar.addAction(qta.icon('mdi.thermometer', color='#ffcb00'), 'Energy')
        p_tool = toolbar.addAction(qta.icon('mdi.flash', color='#8c2b76'), 'Electricity')
        c_tool = toolbar.addAction(qta.icon('mdi.alpha-c', color='#efefef'), 'Carbon')
        s_tool = toolbar.addAction(qta.icon('mdi.alpha-s', color='#efefef'), 'Sulphur')
        n_tool = toolbar.addAction(qta.icon('mdi.alpha-n', color='#efefef'), 'Nitrogen')
        pms_tool = toolbar.addAction(qta.icon('mdi.circle-small', color='#efefef'), 'PM 2.5')
        pmm_tool = toolbar.addAction(qta.icon('mdi.circle-medium', color='#efefef'), 'PM 10')
        capex_tool = toolbar.addAction(qta.icon('mdi.cash', color='lightgreen'), 'CapEx')
        oprex_tool = toolbar.addAction(qta.icon('mdi.account-cog' , color='red'), 'OprEx')

        m_tool.setCheckable(True)
        f_tool.setCheckable(True)
        e_tool.setCheckable(True)
        p_tool.setCheckable(True)
        c_tool.setCheckable(True)
        s_tool.setCheckable(True)
        n_tool.setCheckable(True)
        pms_tool.setCheckable(True)
        pmm_tool.setCheckable(True)
        capex_tool.setCheckable(True)
        oprex_tool.setCheckable(True)

        self.setItemWidget(new_item, 1, toolbar)
        self.editItem(new_item, 0)