from running_addict_plan_extractor.data.garmin_yaml_spi.model import TrainingPlanGarmin
from running_addict_plan_extractor.data.garmin_yaml_spi.yaml_dto import (
    TrainingPlanYamlDTO,
)
from running_addict_plan_extractor.data.garmin_yaml_spi.yaml_mapper import (
    map_training_plan,
)
from running_addict_plan_extractor.data.garmin_yaml_spi.yaml_writer import (
    write_training_plan_yaml,
)


def save_training_plan_to_yaml(plan: TrainingPlanGarmin, file_path: str) -> None:
    training_plan_yaml: TrainingPlanYamlDTO = map_training_plan(plan)
    write_training_plan_yaml(training_plan_yaml, file_path)
