# ----------------------------------------------------------------------------------------------------------------------
# Encoding: UTF-8
# Module name: params
# Description: Resource stream parameter definitions.
# ----------------------------------------------------------------------------------------------------------------------

from typing import Dict, Type

class Parameter:
    """
    Lightweight declarative parameter descriptor used as a base for derived parameters.

    Subclasses should override:
      - KEY  : unique key used to identify the parameter (string)
      - ICON : mdi icon name (string) usable with qtawesome: qta.icon(ICON, ...)
      - COLOR: suggested color for UIs
      - UNITS: human-readable UNITS for values
    """

    KEY     : str = "parameter"
    ICON    : str = "mdi.pound"
    COLOR   : str = "darkred"
    LABEL   : str = "Parameter"
    UNITS   : str = ""
    DEFAULT : str = None

    @classmethod
    def metadata(cls) -> Dict[str, str]:
        return {
            "key"   : cls.KEY,
            "icon"  : cls.ICON,
            "units" : cls.UNITS,
            "color" : cls.COLOR,
            "label" : cls.LABEL if hasattr(cls, 'LABEL') else cls.KEY.title()
        }

# ----------------------------------------------------------------------------------------------------------------------
# Conversion factors:
# Expense:
class Expense(Parameter):
    KEY     = "expense"
    ICON    = "mdi.cash-minus"
    COLOR   = 'lightgreen'
    LABEL   = "Expense"
    UNITS   = ["INR/count", "INR/kg", "INR/tonne", "INR/MJ", "INR/GJ", "INR/kWh", "INR/MWh"]
    DEFAULT = UNITS[0]

# Revenue:
class Revenue(Parameter):
    KEY     = "revenue"
    ICON    = "mdi.cash-plus"
    COLOR   = 'lightgreen'
    LABEL   = "Revenue"
    UNITS   = ["INR/count", "INR/kg", "INR/tonne", "INR/MJ", "INR/GJ", "INR/kWh", "INR/MWh"]
    DEFAULT = UNITS[0]

# Specific Energy:
class SpecificEnergy(Parameter):
    KEY     = "specific_energy"
    ICON    = 'mdi.thermometer'
    COLOR   = '#ffcb00'
    UNITS   = ["kJ/kg", "MJ/kg", "GJ/tonne"]
    LABEL   = "Specific Energy"
    DEFAULT = UNITS[0]

class EmissionFactor(Parameter):
    KEY     = "emission_factor"
    ICON    = 'mdi.percent'
    COLOR   = 'darkgray'
    UNITS   = ["kg/kg", "kg/tonne", "kg/kWh", "kg/MWh"]
    LABEL   = "Emission Factor"
    DEFAULT = UNITS[0]

__all__ = [
    "Parameter",
    "Expense",
    "Revenue",
    "SpecificEnergy",
    "EmissionFactor",
    "ParamBases"
]

ParamBases: Dict[str, Type[Parameter]] = {
    cls.KEY: cls for cls in [
        Expense,
        Revenue,
        SpecificEnergy,
        EmissionFactor
    ]
}