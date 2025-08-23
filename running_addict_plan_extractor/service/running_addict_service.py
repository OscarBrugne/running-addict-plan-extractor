from running_addict_plan_extractor.config import TrainingPlanType
from running_addict_plan_extractor.data import running_addict_api
from running_addict_plan_extractor.model.model import BaseStep, TrainingPlan


def get_training_plan(plan_type: TrainingPlanType) -> TrainingPlan:
    training_plan: TrainingPlan = running_addict_api.get_half_marathon_plan(plan_type)
    return training_plan


def pretty_format_training_plan(
    training_plan: TrainingPlan,
) -> str:
    """
    Format the training plan into a human-readable string.

    Args:
        training_plan (TrainingPlan): The training plan to format.

    Returns:
        str: The formatted training plan.
    """
    formatted_training_plan: str = f"Training Plan: {training_plan.title}\n"
    formatted_training_plan += f"  Description: {training_plan.description}\n"
    formatted_training_plan += "Workout days: "
    for day in training_plan.days:
        formatted_training_plan += f"{day.name}, "
    formatted_training_plan = formatted_training_plan.rstrip(", ")
    formatted_training_plan += "\n"
    for workout in training_plan.workouts:
        formatted_training_plan += f"Workout: {workout.title}\n"
        formatted_training_plan += f"  Description: {workout.description}\n"
        for step in workout.steps:
            formatted_training_plan += f"    - {step.description}\n"
    return formatted_training_plan
