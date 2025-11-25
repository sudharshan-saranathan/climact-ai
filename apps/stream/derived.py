# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: derived
# Description: Derived resource stream definitions.
# ----------------------------------------------------------------------------------------------------------------------

from typing import Dict, Type
from apps.stream.base   import *
from apps.stream.params import *

# Derived stream: Fuel
class Fuel(MassFlow, SpecificEnergy, EmissionFactor, Expense):
    KEY     = "fuel"
    ICON    = "mdi.fuel"
    COLOR   = "#bd8b9c"
    LABEL   = "Fuel"

# Derived stream: Material
class Material(MassFlow, Expense):
    KEY     = "material"
    ICON    = "mdi.gold"
    COLOR   = "#f63c6b"
    LABEL   = "Material"

# Derived stream: Electricity
class Electricity(EnergyFlow, Expense):
    KEY    = "electricity"
    ICON   = "mdi.flash"
    COLOR  = "#8491a3"
    LABEL  = "Electricity"

# Derived stream: Product
class Product(MassFlow, Revenue):
    KEY     = "product"
    ICON    = "mdi.package-variant"
    COLOR   = "#b5ca8d"
    LABEL   = "Product"

DerivedStreams: Dict[str, Type[Stream]] = {
    Fuel.KEY        : Fuel,
    Material.KEY    : Material,
    Electricity.KEY : Electricity,
    Product.KEY     : Product
}

__all__ = [
    "Fuel",
    "Material",
    "Electricity",
    "Product",
    DerivedStreams
]