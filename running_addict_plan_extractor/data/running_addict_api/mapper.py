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


def map_training_plan(plan_dto: TrainingPlanRunningAddictDTO) -> TrainingPlan:
    title: str = plan_dto.title
    description: str = ""
    workouts: list[Workout] = [
        map_workout(workout_dto)
        for week_dto in plan_dto.weeks
        for workout_dto in week_dto.workouts
    ]
    days: list[Day] = extract_days(plan_dto)
    return TrainingPlan(
        title=title,
        description=description,
        workouts=workouts,
        days=days,
    )


def map_week(week_dto: WeekRunningAddictDTO) -> list[Workout]:
    return [map_workout(workout_dto) for workout_dto in week_dto.workouts]


def map_workout(workout_dto: WorkoutRunningAddictDTO) -> Workout:
    duration: str = workout_dto.duration.replace("′", "'")
    title: str = (
        f"{workout_dto.day} - {duration} - Effort Level: {workout_dto.effort_level}"
    )
    description: str = workout_dto.coach_advice if workout_dto.coach_advice else ""
    steps: list[BaseStep] = [map_step(step_dto) for step_dto in workout_dto.steps]
    return Workout(
        title=title,
        description=description,
        steps=steps,
    )


def extract_days(plan_dto: TrainingPlanRunningAddictDTO) -> list[Day]:
    days: list[Day] = []
    week_dto: WeekRunningAddictDTO = plan_dto.weeks[0]
    for workout_dto in week_dto.workouts:
        day_str: str = workout_dto.day.lower()
        match day_str:
            case "lundi":
                days.append(Day.MONDAY)
            case "mardi":
                days.append(Day.TUESDAY)
            case "mercredi":
                days.append(Day.WEDNESDAY)
            case "jeudi":
                days.append(Day.THURSDAY)
            case "vendredi":
                days.append(Day.FRIDAY)
            case "samedi":
                days.append(Day.SATURDAY)
            case "dimanche":
                days.append(Day.SUNDAY)
    return days


def map_step(step_dto: StepRunningAddictDTO) -> BaseStep:
    return parse_step(step_dto)
