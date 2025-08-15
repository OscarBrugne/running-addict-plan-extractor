from running_addict_plan_extractor.data import client
from running_addict_plan_extractor.data.running_addict_api import html_parser
from running_addict_plan_extractor.data.running_addict_api.dto import (
    TrainingPlanRunningAddictDTO,
)


HALF_MARATHON_3X12WEEKS_URL: str = (
    "https://www.running-addict.fr/plan-dentrainement-semi-marathon-3-seances-sur-12-semaines/"
)


def get_half_marathon_plan_title() -> str:
    """Retrieve the Half Marathon 3x12 Weeks training plan from Running Addict.

    Returns:
        str: The title of the training plan.
    """
    html: str = client.get_html(HALF_MARATHON_3X12WEEKS_URL)
    training_plan: TrainingPlanRunningAddictDTO = html_parser.parse_training_plan(html)
    title: str = training_plan.title

    return title


def get_half_marathon_plan() -> TrainingPlanRunningAddictDTO:
    """Retrieve the Half Marathon 3x12 Weeks training plan from Running Addict.

    Returns:
        TrainingPlanRunningAddictDTO: The training plan DTO.
    """
    html: str = client.get_html(HALF_MARATHON_3X12WEEKS_URL)
    training_plan: TrainingPlanRunningAddictDTO = html_parser.parse_training_plan(html)

    return training_plan
