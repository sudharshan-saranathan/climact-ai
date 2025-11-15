# ----------------------------------------------------------------------------------------------------------------------
# Encoding: utf-8
# Module name: default
# Description: Default resource stream definitions.
# ----------------------------------------------------------------------------------------------------------------------

# Import(s):
from typing import Dict, Type, Any, List

# Base-stream class:
class Stream:
    """Lightweight declarative stream descriptor used as mixin/base for resources.

    Subclasses should override:
      - KEY: unique key used to identify the stream (string)
      - UNIT: human-readable unit for values
      - ICON: mdi icon name (string) usable with qtawesome: qta.icon(ICON, ...)
      - COLOR: suggested color for UIs
    """

    KEY: str = "stream"
    UNIT: str = ""
    ICON: str = ""
    COLOR: str = ""

    @classmethod
    def metadata(cls) -> Dict[str, Any]:
        return {
            "key": cls.KEY,
            "unit": cls.UNIT,
            "icon": cls.ICON,
            "color": cls.COLOR,
            "label": getattr(cls, "LABEL", cls.KEY.title()),
        }

    def __repr__(self) -> str:  # pragma: no cover - trivial
        return f"<Stream {self.KEY}>"

# ----------------------------------------------------------------------------------------------------------------------
# Basic stream subclasses:

# Mass:
class Mass(Stream):
    KEY = "mass"
    UNIT = "kg"
    ICON = "mdi.weight-gram"
    COLOR = "lightblue"
    LABEL = "Mass"

# Flow:
class Flow(Stream):
    KEY = "flow"
    UNIT = "kg/s"
    ICON = "mdi.speedometer"
    COLOR = "lightblue"
    LABEL = "flow"

# Energy:
class Energy(Stream):
    KEY = "energy"
    UNIT = "kJ"
    ICON = "mdi.thermometer"
    COLOR = "#ffcb00"
    LABEL = "Energy"

# Electricity:
class Electricity(Stream):
    KEY = "electricity"
    UNIT = "kW"
    ICON = "mdi.flash"
    COLOR = "#8c2b76"
    LABEL = "Electricity"

# Expenses / Costs:
class CapEx(Stream):
    """Generic cost stream (alias/aggregate)."""
    KEY = "capex"
    UNIT = "INR"
    ICON = "mdi.cash"
    COLOR = "#9ad3bc"
    LABEL = "capex"

# Expenses / Costs:
class OpEx(Stream):
    """Generic cost stream (alias/aggregate)."""
    KEY = "opex"
    UNIT = "INR"
    ICON = "mdi.account-cog"
    COLOR = "red"
    LABEL = "opex"

# Revenue:
class Revenue(Stream):
    """Generic cost stream (alias/aggregate)."""
    KEY = "revenue"
    UNIT = "INR"
    ICON = "mdi.currency-inr"
    COLOR = "#9ad3bc"
    LABEL = "revenue"

# GHG:
class GHG(Stream):
    KEY = "GHG"
    UNIT = "kg CO2-eq"
    ICON = "mdi.alpha-c"
    COLOR = "#efefef"
    LABEL = "GHG"

# Sulphur oxides:
class SOx(Stream):
    KEY = "SOx"
    UNIT = "kg"
    ICON = "mdi.alpha-s"
    COLOR = "#efefef"
    LABEL = "SOx"

# Nitrogen oxides:
class NOx(Stream):
    KEY = "NOx"
    UNIT = "kg"
    ICON = "mdi.alpha-n"
    COLOR = "#efefef"
    LABEL = "NOx"

# Particulate Matter 2.5:
class PM25(Stream):
    KEY = "pm2.5"
    UNIT = "kg"
    ICON = "mdi.circle-small"
    COLOR = "#efefef"
    LABEL = "PM 2.5"

# Particulate Matter 10:
class PM10(Stream):
    KEY = "pm10"
    UNIT = "kg"
    ICON = "mdi.circle-medium"
    COLOR = "#efefef"
    LABEL = "PM 10"

# Registry to look up a stream's class by its string key:
DEFAULT_STREAMS: Dict[str, Type[Stream]] = {
    className.KEY: className
    for className in (
        Mass,
        Flow,
        Energy,
        Electricity,
        CapEx,
        OpEx,
        Revenue,
        GHG,
        SOx,
        NOx,
        PM25,
        PM10,
    )
}

# Helper functions:
def get_stream_class(key: str) -> Type[Stream] | None:
    """Return the Stream subclass for the given key or None if not found."""
    return DEFAULT_STREAMS.get(key)

# Helper function to list available stream keys:
def list_stream_keys() -> List[str]:
    """Return available default stream keys in insertion order."""
    return list(DEFAULT_STREAMS.keys())

__all__ = [
    "Stream",
    "Mass",
    "Flow",
    "Energy",
    "Electricity",
    "CapEx",
    "OpEx",
    "Revenue",
    "GHG",
    "SOx",
    "NOx",
    "PM25",
    "PM10",
    "DEFAULT_STREAMS",
    "get_stream_class",
    "list_stream_keys",
]
