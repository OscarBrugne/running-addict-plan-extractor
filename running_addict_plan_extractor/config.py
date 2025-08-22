from enum import Enum, auto
from datetime import date

from running_addict_plan_extractor.model.model import Pace
from running_addict_plan_extractor.model.enum import Day, PaceType


class TrainingPlanType(Enum):
    HALF_MARATHON_3X12WEEKS = auto()
    HALF_MARATHON_4X12WEEKS = auto()
    HALF_MARATHON_1H30 = auto()


PACES: dict[PaceType, Pace] = {
    PaceType.BASE: Pace(6, 40),
    PaceType.FIVE_KM: Pace(4, 7),
    PaceType.TEN_KM: Pace(4, 18),
    PaceType.HALF_MARATHON: Pace(4, 30),
    PaceType.MARATHON: Pace(5, 22),
}

DAYS: list[Day] = [
    Day.TUESDAY,
    Day.THURSDAY,
    Day.SATURDAY,
    Day.SUNDAY,
]

START_DATE: date = date(2025, 8, 18)

SAVE_DIRECTORY: str = "output"
