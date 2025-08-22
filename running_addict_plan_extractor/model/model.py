from dataclasses import dataclass

from running_addict_plan_extractor.model.enum import Day, PaceType


@dataclass
class BaseStep:
    description: str


@dataclass
class ConstantStep(BaseStep):
    duration_minutes: float
    pace: PaceType


@dataclass
class IntervalStep(BaseStep):
    repeat_count: int
    workout: BaseStep
    rest: BaseStep


@dataclass
class ProgressiveStep(BaseStep):
    duration_minutes: float
    start_pace: PaceType
    end_pace: PaceType


@dataclass
class Workout:
    title: str
    description: str
    steps: list[BaseStep]


@dataclass
class TrainingPlan:
    title: str
    description: str
    workouts: list[Workout]
    days: list[Day]


@dataclass
class Pace:
    minutes: int
    seconds: int

    def __lt__(self, other: "Pace") -> bool:
        return (self.minutes, self.seconds) < (other.minutes, other.seconds)

    def __le__(self, other: "Pace") -> bool:
        return (self.minutes, self.seconds) <= (other.minutes, other.seconds)

    def __gt__(self, other: "Pace") -> bool:
        return (self.minutes, self.seconds) > (other.minutes, other.seconds)

    def __ge__(self, other: "Pace") -> bool:
        return (self.minutes, self.seconds) >= (other.minutes, other.seconds)
