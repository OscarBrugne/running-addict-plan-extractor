from running_addict_plan_extractor.data.running_addict_api.dto import (
    StepRunningAddictDTO,
    WorkoutRunningAddictDTO,
    WeekRunningAddictDTO,
    TrainingPlanRunningAddictDTO,
)
from running_addict_plan_extractor.data.running_addict_api.step_parser import parse_step
from running_addict_plan_extractor.model.enum import Day
from running_addict_plan_extractor.model.model import (
    BaseStep,
    Workout,
    TrainingPlan,
)


def map_base_step(step_dto: StepRunningAddictDTO) -> BaseStep:
    return BaseStep(description=step_dto.description)


def map_step(step_dto: StepRunningAddictDTO) -> BaseStep:
    return parse_step(step_dto)


def map_workout(workout_dto: WorkoutRunningAddictDTO) -> Workout:
    title: str = (
        f"{workout_dto.day} - {workout_dto.duration} - Effort Level: {workout_dto.effort_level}"
    )
    description: str = workout_dto.coach_advice if workout_dto.coach_advice else ""
    steps: list[BaseStep] = [map_step(step_dto) for step_dto in workout_dto.steps]
    return Workout(
        title=title,
        description=description,
        steps=steps,
    )


def map_week(week_dto: WeekRunningAddictDTO) -> list[Workout]:
    return [map_workout(workout_dto) for workout_dto in week_dto.workouts]


def map_training_plan(plan_dto: TrainingPlanRunningAddictDTO) -> TrainingPlan:
    title: str = plan_dto.title
    description: str = ""
    workouts: list[Workout] = [
        map_workout(workout_dto)
        for week_dto in plan_dto.weeks
        for workout_dto in week_dto.workouts
    ]
    days: list[Day] = []
    return TrainingPlan(
        title=title,
        description=description,
        workouts=workouts,
        days=days,
    )
