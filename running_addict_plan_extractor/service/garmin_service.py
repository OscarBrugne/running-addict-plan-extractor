from datetime import date
from math import e

from running_addict_plan_extractor.config import PACES
from running_addict_plan_extractor.model.model import (
    Pace,
    TrainingPlan,
    Workout,
    BaseStep,
    ConstantStep,
    IntervalStep,
    ProgressiveStep,
)
from running_addict_plan_extractor.model.enum import Day, PaceType
from running_addict_plan_extractor.data import garmin_yaml_spi


PACE_DEFINITIONS: dict[PaceType, str] = {
    PaceType.BASE: "EF",
    PaceType.FIVE_KM: "Pace5km",
    PaceType.TEN_KM: "Pace10km",
    PaceType.HALF_MARATHON: "Pace21km",
    PaceType.MARATHON: "Pace42km",
}


def create_yaml_garmin_training_plan(
    plan: TrainingPlan,
    file_path: str,
    start_date: date,
    days: list[Day] | None,
) -> None:
    plan_garmin: garmin_yaml_spi.TrainingPlanGarmin = map_training_plan_to_garmin(
        plan, start_date, days
    )
    garmin_yaml_spi.save_training_plan_to_yaml(plan_garmin, file_path)


def map_training_plan_to_garmin(
    plan: TrainingPlan,
    start_date: date,
    days: list[Day] | None,
) -> garmin_yaml_spi.TrainingPlanGarmin:
    workouts_garmin: list[garmin_yaml_spi.WorkoutGarmin] = [
        map_workout_to_garmin(workout) for workout in plan.workouts
    ]
    if not days:
        days = plan.days
    assert len(days) == len(plan.days)
    definitions: dict[str, str] = generate_intensity_definitions()

    # Drop the workout corresponding to the race
    workouts_garmin = workouts_garmin[:-1]
    workouts_garmin = rename_workouts(workouts_garmin, days)

    return garmin_yaml_spi.TrainingPlanGarmin(
        workouts=workouts_garmin,
        days=days,
        start_date=start_date,
        intensity_definitions=definitions,
    )


def generate_intensity_definitions() -> dict[str, str]:
    delta_ef: float = 0.10
    return {
        PACE_DEFINITIONS[PaceType.BASE]: generate_pace_str(
            PACES[PaceType.BASE], delta_ef
        ),
        PACE_DEFINITIONS[PaceType.MARATHON]: generate_pace_str(
            PACES[PaceType.MARATHON]
        ),
        PACE_DEFINITIONS[PaceType.HALF_MARATHON]: generate_pace_str(
            PACES[PaceType.HALF_MARATHON]
        ),
        PACE_DEFINITIONS[PaceType.TEN_KM]: generate_pace_str(PACES[PaceType.TEN_KM]),
        PACE_DEFINITIONS[PaceType.FIVE_KM]: generate_pace_str(PACES[PaceType.FIVE_KM]),
    }


def generate_pace_str(pace: Pace, delta_percentage: float = 0.05) -> str:
    base_pace_seconds: int = pace.minutes * 60 + pace.seconds
    delta: int = int(base_pace_seconds * delta_percentage)
    min_pace: int = max(0, base_pace_seconds - delta)
    max_pace: int = base_pace_seconds + delta
    return (
        f"{min_pace // 60:02}:{min_pace % 60:02}-{max_pace // 60:02}:{max_pace % 60:02}"
    )


def map_workout_to_garmin(workout: Workout) -> garmin_yaml_spi.WorkoutGarmin:
    steps_garmin: list[garmin_yaml_spi.StepGarmin | garmin_yaml_spi.RepeatGarmin] = []
    for step in workout.steps:
        steps_garmin.append(map_base_step_to_garmin(step))
    return garmin_yaml_spi.WorkoutGarmin(name=workout.title, steps=steps_garmin)


def map_base_step_to_garmin(
    step: BaseStep, no_pace: bool = False
) -> garmin_yaml_spi.StepGarmin | garmin_yaml_spi.RepeatGarmin:
    if isinstance(step, ConstantStep):
        return map_constant_step(step, no_pace=no_pace)
    elif isinstance(step, IntervalStep):
        return map_interval_step(step)
    elif isinstance(step, ProgressiveStep):
        return map_progressive_step(step)
    else:
        return garmin_yaml_spi.StepGarmin(
            step_type=garmin_yaml_spi.StepType.OTHER,
            duration_seconds=0,
            intensity_target=step.description,
        )


def map_constant_step(
    step: ConstantStep, no_pace: bool = False
) -> garmin_yaml_spi.StepGarmin:
    """Map a constant step to StepGarmin."""
    duration_seconds = int(step.duration_minutes * 60)

    if step.pace in [PaceType.BASE, PaceType.SLOW]:
        step_type: garmin_yaml_spi.StepType = garmin_yaml_spi.StepType.RECOVERY
    else:
        step_type = garmin_yaml_spi.StepType.RUN

    if no_pace:
        intensity_target: str | None = None
    elif step.pace in [
        PaceType.BASE,
        PaceType.FIVE_KM,
        PaceType.TEN_KM,
        PaceType.HALF_MARATHON,
        PaceType.MARATHON,
    ]:
        intensity_target = PACE_DEFINITIONS[step.pace]
    else:
        intensity_target: str | None = None

    return garmin_yaml_spi.StepGarmin(
        step_type=step_type,
        duration_seconds=duration_seconds,
        intensity_target=intensity_target,
    )


def map_interval_step(step: IntervalStep) -> garmin_yaml_spi.RepeatGarmin:
    run_step: garmin_yaml_spi.StepGarmin | garmin_yaml_spi.RepeatGarmin = (
        map_base_step_to_garmin(step.workout)
    )
    assert isinstance(run_step, garmin_yaml_spi.StepGarmin)
    rest_step: garmin_yaml_spi.StepGarmin | garmin_yaml_spi.RepeatGarmin = (
        map_base_step_to_garmin(step.rest, no_pace=True)
    )
    assert isinstance(rest_step, garmin_yaml_spi.StepGarmin)
    return garmin_yaml_spi.RepeatGarmin(
        count=step.repeat_count, run_step=run_step, recovery_step=rest_step
    )


def map_progressive_step(step: ProgressiveStep) -> garmin_yaml_spi.StepGarmin:
    duration_sec = int(step.duration_minutes * 60)

    start_pace: Pace = PACES[step.start_pace]
    end_pace: Pace = PACES[step.end_pace]
    min_pace: Pace = min(start_pace, end_pace)
    max_pace: Pace = max(start_pace, end_pace)

    min_intensity: str = generate_pace_str(min_pace)
    max_intensity: str = generate_pace_str(max_pace)

    min_pace_str: str = min_intensity.split("-")[0]
    max_pace_str: str = max_intensity.split("-")[1]
    intensity_target: str = f"{min_pace_str}-{max_pace_str}"

    return garmin_yaml_spi.StepGarmin(
        step_type=garmin_yaml_spi.StepType.RUN,
        duration_seconds=duration_sec,
        intensity_target=intensity_target,
    )


def rename_workouts(
    workouts: list[garmin_yaml_spi.WorkoutGarmin], days: list[Day]
) -> list[garmin_yaml_spi.WorkoutGarmin]:
    weekly_workout_count: int = len(days)

    for i, workout in enumerate(workouts):
        week_number: int = (i // weekly_workout_count) + 1
        day_number: int = (i % weekly_workout_count) + 1

        step_descriptions: list[str] = []
        for step in workout.steps:
            step_descriptions.append(describe_step(step))
        description: str = " | ".join(step_descriptions)

        workout.name = f"S{week_number}E{day_number} : {description}"

    return workouts


def describe_step(
    step: garmin_yaml_spi.StepGarmin | garmin_yaml_spi.RepeatGarmin,
) -> str:
    if isinstance(step, garmin_yaml_spi.RepeatGarmin):
        run_desc: str = describe_step(step.run_step)
        rec_desc: str = describe_step(step.recovery_step)
        return f"{step.count} x {run_desc} + {rec_desc}"

    elif isinstance(step, garmin_yaml_spi.StepGarmin):
        minutes: int = step.duration_seconds // 60
        seconds: int = step.duration_seconds % 60

        if minutes > 0 and seconds > 0:
            duration: str = f"{minutes}'{seconds:02}"
        elif minutes > 0:
            duration = f"{minutes}'"
        else:
            duration = f'{seconds}"'

        intensity: str = step.intensity_target if step.intensity_target else "Recup"

        return f"{duration} {intensity}"

    else:
        return "Inconnu"
