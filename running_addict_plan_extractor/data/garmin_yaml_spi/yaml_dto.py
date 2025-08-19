from dataclasses import dataclass
from datetime import date

from running_addict_plan_extractor.data.garmin_yaml_spi.enum import StepType


@dataclass
class SettingsYamlDTO:
    delete_same_name_workout: bool


@dataclass
class StepYamlDTO:
    type: str
    value: str | list["StepYamlDTO"]


@dataclass
class WorkoutYamlDTO:
    name: str
    steps: list[StepYamlDTO]


@dataclass
class SchedulePlanYamlDTO:
    start_from: str
    workouts: list[str]


@dataclass
class TrainingPlanYamlDTO:
    settings: SettingsYamlDTO
    definitions: dict[str, str]
    workouts: list[WorkoutYamlDTO]
    schedule_plan: SchedulePlanYamlDTO
