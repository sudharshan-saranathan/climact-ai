from enum import Enum, auto

# Enumeration for different classes of entities:
class EntityClass(Enum):
    INP = auto()
    OUT = auto()
    VAR = auto()
    PAR = auto()
    EQN = auto()

class EntityState(Enum):
    HIDDEN = auto()
    ACTIVE = auto()