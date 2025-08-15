from dataclasses import dataclass


@dataclass
class StepDTO:
    description: str


@dataclass
class WorkoutRunningAddictDTO:
    day: str
    duration: str
    effort_level: int
    steps: list[StepDTO]
    coach_advice: str


@dataclass
class WeekRunningAddictDTO:
    week: str
    workouts: list[WorkoutRunningAddictDTO]


@dataclass
class TrainingPlanRunningAddictDTO:
    title: str
    weeks: list[WeekRunningAddictDTO]
