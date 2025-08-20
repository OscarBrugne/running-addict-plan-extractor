from unittest import result
from running_addict_plan_extractor.data.garmin_yaml_spi.model import (
    TrainingPlanGarmin,
    WorkoutGarmin,
    StepGarmin,
    RepeatGarmin,
)
from running_addict_plan_extractor.data.garmin_yaml_spi.yaml_dto import (
    TrainingPlanYamlDTO,
    WorkoutYamlDTO,
    StepYamlDTO,
    SchedulePlanYamlDTO,
    SettingsYamlDTO,
)
from running_addict_plan_extractor.model.enum import Day


def map_training_plan(plan: TrainingPlanGarmin) -> TrainingPlanYamlDTO:
    settings: SettingsYamlDTO = SettingsYamlDTO(delete_same_name_workout=True)
    definitions: dict[str, str] = plan.intensity_definitions
    workouts: list[WorkoutYamlDTO] = [map_workout(workout) for workout in plan.workouts]
    schedule_plan: SchedulePlanYamlDTO = map_schedule_plan(plan)
    return TrainingPlanYamlDTO(
        settings=settings,
        definitions=definitions,
        workouts=workouts,
        schedule_plan=schedule_plan,
    )


def map_workout(workout: WorkoutGarmin) -> WorkoutYamlDTO:
    steps: list[StepYamlDTO] = []
    for step in workout.steps:
        if isinstance(step, StepGarmin):
            steps.append(map_step(step))
        elif isinstance(step, RepeatGarmin):
            steps.append(map_repeat(step))
        else:
            raise ValueError(f"Unknown step type: {type(step)}")
    return WorkoutYamlDTO(
        name=workout.name,
        steps=steps,
    )


def map_step(step: StepGarmin) -> StepYamlDTO:
    step_type: str = step.step_type.value
    value: str = f"{step.duration_seconds}sec"
    if step.intensity_target is not None:
        value += f" {step.intensity_target}"
    return StepYamlDTO(
        step_type=step_type,
        value=value,
    )


def map_repeat(repeat: RepeatGarmin) -> StepYamlDTO:
    step_type: str = f"repeat({repeat.count})"
    steps: list[StepGarmin] = [repeat.run_step, repeat.recovery_step]
    value: list[StepYamlDTO] = [map_step(step) for step in steps]
    return StepYamlDTO(
        step_type=step_type,
        value=value,
    )


def map_schedule_plan(
    plan: TrainingPlanGarmin, rest_day_name: str = "rest"
) -> SchedulePlanYamlDTO:
    start_from: str = plan.start_date.isoformat()

    workout_names: list[str] = [workout.name for workout in plan.workouts]
    start_day: Day = Day(plan.start_date.weekday())
    training_days: list[Day] = plan.days

    schedule: list[str | None] = build_schedule(training_days, workout_names, start_day)

    workouts: list[str] = [
        workout if workout else rest_day_name for workout in schedule
    ]

    return SchedulePlanYamlDTO(start_from=start_from, workouts=workouts)


def build_schedule(
    training_days: list[Day], workout_names: list[str], start_day: Day
) -> list[str | None]:
    schedule: list[str | None] = []

    weekly_workout_count: int = len(training_days)
    total_workouts: int = len(workout_names)
    full_week_count: int = total_workouts // weekly_workout_count
    remaining_workout_count: int = total_workouts % weekly_workout_count

    training_day_indices: list[int] = [
        ((day.value - start_day.value) % 7) for day in training_days
    ]

    workout_index: int = 0

    # Build full weeks
    for _ in range(full_week_count):
        week: list[str | None] = [None] * 7
        for i in training_day_indices:
            week[i] = workout_names[workout_index]
            workout_index += 1
        schedule.extend(week)

    # Build remaining workouts
    if remaining_workout_count > 0:
        last_week_length: int = max(training_day_indices[:remaining_workout_count]) + 1
        week: list[str | None] = [None] * last_week_length
        for idx in training_day_indices[:remaining_workout_count]:
            week[idx] = workout_names[workout_index]
            workout_index += 1
        schedule.extend(week)

    return schedule
