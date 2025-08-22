import argparse

from running_addict_plan_extractor.config import TrainingPlanType
from running_addict_plan_extractor.model.model import TrainingPlan
from running_addict_plan_extractor.service import running_addict_service


PLAN_CHOICES: dict[str, TrainingPlanType] = {
    "3x12": TrainingPlanType.HALF_MARATHON_3X12WEEKS,
    "4x12": TrainingPlanType.HALF_MARATHON_4X12WEEKS,
    "1h30": TrainingPlanType.HALF_MARATHON_1H30,
}


def run() -> None:
    plan_type: TrainingPlanType = parse_args()
    training_plan: TrainingPlan = running_addict_service.get_training_plan(plan_type)
    training_plan_str: str = running_addict_service.pretty_format_training_plan(
        training_plan
    )
    print(training_plan_str)


def parse_args() -> TrainingPlanType:
    parser = argparse.ArgumentParser(
        description="Export a Running Addict training plan to Garmin YAML."
    )
    parser.add_argument(
        "plan",
        choices=PLAN_CHOICES.keys(),
        type=str,
        help="Select a training plan (3x12, 4x12, 1h30)",
    )

    args: argparse.Namespace = parser.parse_args()
    return PLAN_CHOICES[args.plan]
