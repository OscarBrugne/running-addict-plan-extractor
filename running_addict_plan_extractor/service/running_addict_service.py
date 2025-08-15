from running_addict_plan_extractor.data import running_addict_api


def get_training_plan_title() -> str:
    title: str = running_addict_api.get_half_marathon_plan_title()
    return title


def get_training_plan_str() -> str:
    training_plan: running_addict_api.TrainingPlanRunningAddictDTO = (
        running_addict_api.get_half_marathon_plan()
    )
    training_plan_str: str = pretty_format_training_plan(training_plan)
    return training_plan_str


def pretty_format_training_plan(
    training_plan: running_addict_api.TrainingPlanRunningAddictDTO,
) -> str:
    """
    Format the training plan into a human-readable string.

    Args:
        training_plan (TrainingPlanRunningAddictDTO): The training plan to format.

    Returns:
        str: The formatted training plan.
    """
    formatted_training_plan: str = f"Training Plan: {training_plan.title}\n"
    for week in training_plan.weeks:
        formatted_training_plan += f"Week {week.week}:\n"
        for workout in week.workouts:
            formatted_training_plan += (
                f"  - {workout.day} ({workout.duration} - {workout.effort_level})\n"
            )
            for step in workout.steps:
                formatted_training_plan += f"    - {step.description}\n"
            formatted_training_plan += f"    Coach's Advice: {workout.coach_advice}\n"
    return formatted_training_plan
