import os

from running_addict_plan_extractor.data.garmin_yaml_spi.yaml_dto import (
    TrainingPlanYamlDTO,
    SettingsYamlDTO,
    WorkoutYamlDTO,
    StepYamlDTO,
    SchedulePlanYamlDTO,
)
from running_addict_plan_extractor.data.garmin_yaml_spi.yaml_writer import (
    write_training_plan_yaml,
)


if __name__ == "__main__":
    # Run tests with python -m tests.test_yaml_writer
    print("TEST: Garmin YAML Writer")
    print("========================================")

    file_path: str = "./tests/tmp_test_output.yaml"

    plan = TrainingPlanYamlDTO(
        settings=SettingsYamlDTO(delete_same_name_workout=True),
        definitions={
            "GA": "6:35-7:00",
            "Threshold": "5:20-5:45",
            "VO2MaxP": "3:30-4:00",
        },
        workouts=[
            WorkoutYamlDTO(
                name="interval_VO2Max",
                steps=[
                    StepYamlDTO(
                        step_type="warmup",
                        value="15min @H(z2)",
                    ),
                    StepYamlDTO(
                        step_type="repeat(8)",
                        value=[
                            StepYamlDTO(
                                step_type="run",
                                value="30sec @P($VO2MaxP)",
                            ),
                            StepYamlDTO(
                                step_type="recovery",
                                value="1200m",
                            ),
                        ],
                    ),
                    StepYamlDTO(
                        step_type="cooldown",
                        value="15min @H(z2)",
                    ),
                ],
            ),
            WorkoutYamlDTO(
                name="ga_5k",
                steps=[
                    StepYamlDTO(
                        step_type="warmup",
                        value="1000m @H(z2)",
                    ),
                    StepYamlDTO(
                        step_type="run",
                        value="3000m @P($GA)",
                    ),
                    StepYamlDTO(
                        step_type="cooldown",
                        value="1000m @H(z2)",
                    ),
                ],
            ),
        ],
        schedule_plan=SchedulePlanYamlDTO(
            start_from="2024-10-08",
            workouts=["interval_VO2Max", "ga_5k", "rest"],
        ),
    )

    write_training_plan_yaml(plan, file_path)

    with open(file_path, "r") as file:
        content: str = file.read()
        print(content)

    os.remove(file_path)
