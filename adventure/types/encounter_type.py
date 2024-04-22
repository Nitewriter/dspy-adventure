import random
from enum import StrEnum, auto


class EncounterType(StrEnum):
    """Text adventure encounter types"""

    EXPLORATION = auto()
    COMBAT = auto()
    SOCIAL = auto()
    PUZZLE = auto()
    TRAP = auto()
    TREASURE = auto()
    SHOP = auto()

    @classmethod
    def random(cls):
        return random.choice(list(cls))
