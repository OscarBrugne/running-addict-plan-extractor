from dataclasses import dataclass
from datetime import date

from running_addict_plan_extractor.data.garmin_yaml_spi.enum import StepType
from running_addict_plan_extractor.model.enum import Day


@dataclass
class StepGarmin:
    step_type: StepType
    duration_seconds: int
    intensity_target: str | None = None


@dataclass
class RepeatGarmin:
    count: int
    run_step: StepGarmin
    recovery_step: StepGarmin


@dataclass
class WorkoutGarmin:
    name: str
    steps: list[StepGarmin | RepeatGarmin]


@dataclass
class TrainingPlanGarmin:
    workouts: list[WorkoutGarmin]
    days: list[Day]
    start_date: date
    intensity_definitions: dict[str, str]
