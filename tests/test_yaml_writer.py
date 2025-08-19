import os
from running_addict_plan_extractor.data.garmin_yaml_spi.yaml_writer import (
    write_training_plan_yaml,
)
from running_addict_plan_extractor.data.garmin_yaml_spi.yaml_dto import (
    TrainingPlanYamlDTO,
    SettingsYamlDTO,
    WorkoutYamlDTO,
    StepYamlDTO,
    SchedulePlanYamlDTO,
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
                        type="warmup",
                        value="15min @H(z2)",
                    ),
                    StepYamlDTO(
                        type="repeat(8)",
                        value=[
                            StepYamlDTO(
                                type="run",
                                value="30sec @P($VO2MaxP)",
                            ),
                            StepYamlDTO(
                                type="recovery",
                                value="1200m",
                            ),
                        ],
                    ),
                    StepYamlDTO(
                        type="cooldown",
                        value="15min @H(z2)",
                    ),
                ],
            ),
            WorkoutYamlDTO(
                name="ga_5k",
                steps=[
                    StepYamlDTO(
                        type="warmup",
                        value="1000m @H(z2)",
                    ),
                    StepYamlDTO(
                        type="run",
                        value="3000m @P($GA)",
                    ),
                    StepYamlDTO(
                        type="cooldown",
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
