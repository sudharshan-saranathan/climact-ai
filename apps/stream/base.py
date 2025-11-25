# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: default
# Description: Default resource stream definitions.
# ----------------------------------------------------------------------------------------------------------------------

# Import(s):
from typing import Dict, List

# Pint: Library for physical quantities with units:
import pint
from typing import Dict
from typing import Type
from typing import Any

# Initialize unit-registry:
ureg = pint.UnitRegistry()

# Define custom units:
ureg.define('INR = [currency]')
ureg.define('USD = 85 * INR')
ureg.define('count = [item]')                       #

ureg.define('@alias ton = tonne')
ureg.define('tonne = 1000 * kg')
ureg.define('Mt = 1e6 * tonne')

ureg.define('CO2_eq = [greenhouse_gas]')
ureg.define('kg_CO2_eq = kg * CO2_eq')
ureg.define('tonne_CO2_eq = 1000 * kg_CO2_eq')
ureg.define('Mt_CO2_eq = 1e6 * tonne_CO2_eq')

# Base-stream class:
class Stream:

    KEY     : str   = "stream"  # Key used to identify the stream
    ICON    : str   = ""
    COLOR   : str   = ""
    LABEL   : str   = "Stream"  # Human-readable label
    UNITS   : list  = []        # Pint-compatible unit strings
    DEFAULT : str   = None      # Default unit for this stream

    @classmethod
    def metadata(cls) -> Dict[str, Any]:
        return {
            "key"   : cls.KEY,
            "icon"  : cls.ICON,
            "units" : cls.UNITS,
            "color" : cls.COLOR,
            "label" : cls.LABEL
        }

    # Class representation (trivial):
    def __repr__(self) -> str:  return f"<Stream {self.KEY}>"

# ----------------------------------------------------------------------------------------------------------------------
# Classes representing resource/emission flows:
# Item Flow:
class ItemFlow(Stream):
    KEY     = "item_flow"
    ICON    = "mdi.package-variant"
    COLOR   = "#222e50"
    LABEL   = "Item"
    UNITS   = ['count/year', 'count/month', 'count/day', 'count/hr', 'count/s']
    DEFAULT = UNITS[0]

    # Default constructor:
    def __init__(self, value: float = 0.0, unit: str = None):

        self.unit = unit or self.DEFAULT
        self.quantity = pint.Quantity(value, unit=self.unit)

# Mass Flow:
class MassFlow(Stream):
    KEY     = "mass_flow"
    ICON    = "mdi.weight-gram"
    COLOR   = "#0094c6"
    LABEL   = "Mass"
    UNITS   = ["kg/year", "kg/month", "kg/day", "kg/hr", "kg/s", "tonne/year", "tonne/month", "tonne/day", "tonne/hour", "tonne/s"]
    DEFAULT = UNITS[0]

# Energy Flow (Power):
class EnergyFlow(Stream):
    KEY     = "energy_flow"
    ICON    = "mdi.fire"
    COLOR   = "#ffcb00"
    LABEL   = "Energy"
    UNITS   = ["kW", "MW", "GW"]
    DEFAULT = UNITS[0]

# Cash Flow:
class CreditFlow(Stream):
    KEY     = "credit_flow"
    ICON    = "mdi.cash"
    COLOR   = "green"
    LABEL   = "Credit"
    UNITS   = ["INR/year", "INR/month", "INR/day", "INR/hour", "INR/s"]
    DEFAULT = UNITS[0]

__all__ = [
    "Stream",
    "ItemFlow",
    "MassFlow",
    "EnergyFlow",
    "CreditFlow",
    "FlowBases"
]

FlowBases: Dict[str, Type[Stream]] = {
    class_name.__name__: class_name
    for class_name in [
        ItemFlow,
        MassFlow,
        EnergyFlow,
        CreditFlow,
    ]
}