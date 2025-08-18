from enum import Enum, auto


class Day(Enum):
    MONDAY = auto()
    TUESDAY = auto()
    WEDNESDAY = auto()
    THURSDAY = auto()
    FRIDAY = auto()
    SATURDAY = auto()
    SUNDAY = auto()


class Pace(Enum):
    BASE = auto()
    FIVE_KM = auto()
    TEN_KM = auto()
    HALF_MARATHON = auto()
    MARATHON = auto()
    SLOW = auto()
    HILL = auto()
