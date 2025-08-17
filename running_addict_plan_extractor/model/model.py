from dataclasses import dataclass

from running_addict_plan_extractor.model.enum import Day, Pace


@dataclass
class BaseStep:
    description: str


@dataclass
class ConstantStep(BaseStep):
    duration_minutes: int
    pace: Pace


@dataclass
class IntervalStep(BaseStep):
    repeat_count: int
    workout: BaseStep
    rest: BaseStep


@dataclass
class ProgressiveStep(BaseStep):
    duration_minutes: int
    start_pace: Pace
    end_pace: Pace


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
