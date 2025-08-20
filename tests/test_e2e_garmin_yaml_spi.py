import os
from datetime import date

from running_addict_plan_extractor.data.garmin_yaml_spi.model import (
    TrainingPlanGarmin,
    WorkoutGarmin,
    StepGarmin,
    RepeatGarmin,
)
from running_addict_plan_extractor.data.garmin_yaml_spi.enum import StepType
from running_addict_plan_extractor.model.enum import Day
from running_addict_plan_extractor.data.garmin_yaml_spi.spi import (
    save_training_plan_to_yaml,
)


if __name__ == "__main__":
    # Run tests with python -m tests.test_e2e_garmin_yaml_spi
    print("TEST E2E: Garmin YAML Writer")
    print("========================================")

    file_path: str = "./tests/tmp_test_output.yaml"

    days: list[Day] = [Day.TUESDAY, Day.THURSDAY, Day.SATURDAY, Day.SUNDAY]
    start_date: date = date(2024, 10, 8)  # Tuesday
    intensity_definitions: dict[str, str] = {
        "EF": "06:00-07:20",
        "Pace42km": "05:06-05:38",
        "Pace21km": "04:16-04:44",
        "Pace10km": "04:05-04:31",
        "Pace5km": "03:55-04:19",
    }

    # workouts:
    #   S1E1_8x1'30_P5km_1'30_EF:
    #     - warmup: 20min @P($EF)
    #     - repeat(8):
    #         - run: 90sec @P($Pace5km)
    #         - recovery: 90sec
    #     - cooldown: 5min @P($EF)

    workout_s1e1: WorkoutGarmin = WorkoutGarmin(
        name="S1E1_8x1'30_P5km_1'30_EF",
        steps=[
            StepGarmin(
                step_type=StepType.WARMUP,
                duration_seconds=20 * 60,
                intensity_target="@P($EF)",
            ),
            RepeatGarmin(
                count=8,
                run_step=StepGarmin(
                    step_type=StepType.RUN,
                    duration_seconds=90,
                    intensity_target="@P($Pace5km)",
                ),
                recovery_step=StepGarmin(
                    step_type=StepType.RECOVERY,
                    duration_seconds=90,
                    # No intensity target
                ),
            ),
            StepGarmin(
                step_type=StepType.COOLDOWN,
                duration_seconds=5 * 60,
                intensity_target="@P($EF)",
            ),
        ],
    )
    example_step: StepGarmin = StepGarmin(
        step_type=StepType.RUN,
        duration_seconds=30 * 60,
        intensity_target="@P($Pace21km)",
    )
    workout_s1e2: WorkoutGarmin = WorkoutGarmin(
        name="S1E2_Example", steps=[example_step]
    )
    workout_s1e3: WorkoutGarmin = WorkoutGarmin(
        name="S1E3_Example", steps=[example_step]
    )
    workout_s1e4: WorkoutGarmin = WorkoutGarmin(
        name="S1E4_Example", steps=[example_step]
    )
    workout_s2e1: WorkoutGarmin = WorkoutGarmin(
        name="S2E1_Example", steps=[example_step]
    )
    workout_s2e2: WorkoutGarmin = WorkoutGarmin(
        name="S2E2_Example", steps=[example_step]
    )

    workouts: list[WorkoutGarmin] = [
        workout_s1e1,
        workout_s1e2,
        workout_s1e3,
        workout_s1e4,
        workout_s2e1,
        workout_s2e2,
    ]

    plan: TrainingPlanGarmin = TrainingPlanGarmin(
        workouts, days, start_date, intensity_definitions
    )

    save_training_plan_to_yaml(plan, file_path)

    with open(file_path, "r") as file:
        content: str = file.read()
        print(content)

    os.remove(file_path)
