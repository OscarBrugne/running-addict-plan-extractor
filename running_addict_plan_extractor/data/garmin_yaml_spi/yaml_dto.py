from dataclasses import dataclass


@dataclass
class SettingsYamlDTO:
    delete_same_name_workout: bool


@dataclass
class StepYamlDTO:
    step_type: str
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
