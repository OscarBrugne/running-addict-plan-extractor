from enum import Enum, auto


class Day(Enum):
    MONDAY = 0
    TUESDAY = 1
    WEDNESDAY = 2
    THURSDAY = 3
    FRIDAY = 4
    SATURDAY = 5
    SUNDAY = 6


class Pace(Enum):
    BASE = auto()
    FIVE_KM = auto()
    TEN_KM = auto()
    HALF_MARATHON = auto()
    MARATHON = auto()
    SLOW = auto()
    HILL = auto()
