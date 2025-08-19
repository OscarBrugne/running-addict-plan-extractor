from typing import Any
import yaml

from running_addict_plan_extractor.data.garmin_yaml_spi.yaml_dto import (
    TrainingPlanYamlDTO,
    StepYamlDTO,
)


def write_training_plan_yaml(plan: TrainingPlanYamlDTO, file_path: str) -> None:
    plan_dict: dict[str, Any] = training_plan_to_yaml_dict(plan)
    with open(file_path, "w") as file:
        yaml.safe_dump(plan_dict, file, sort_keys=False)


def training_plan_to_yaml_dict(plan: TrainingPlanYamlDTO) -> dict[str, Any]:
    plan_dict: dict[str, Any] = {
        "settings": {"deleteSameNameWorkout": plan.settings.delete_same_name_workout},
        "definitions": plan.definitions,
        "workouts": {
            workout.name: [step_to_yaml_dict(step) for step in workout.steps]
            for workout in plan.workouts
        },
        "schedulePlan": {
            "start_from": plan.schedule_plan.start_from,
            "workouts": plan.schedule_plan.workouts,
        },
    }
    return plan_dict


def step_to_yaml_dict(step: StepYamlDTO) -> dict[str, Any]:
    if isinstance(step.value, list):
        return {step.type: [step_to_yaml_dict(s) for s in step.value]}
    if isinstance(step.value, str):
        return {step.type: step.value}

    raise ValueError(f"Unsupported step value type: {type(step.value)}")
