from running_addict_plan_extractor.data import client
from running_addict_plan_extractor.data.running_addict_api import html_parser
from running_addict_plan_extractor.data.running_addict_api.dto import (
    TrainingPlanRunningAddictDTO,
)
from running_addict_plan_extractor.data.running_addict_api import mapper
from running_addict_plan_extractor.model.model import TrainingPlan


HALF_MARATHON_3X12WEEKS_URL: str = (
    "https://www.running-addict.fr/plan-dentrainement-semi-marathon-3-seances-sur-12-semaines/"
)


def get_half_marathon_plan() -> TrainingPlan:
    """Retrieve the Half Marathon 3x12 Weeks training plan from Running Addict.

    Returns:
        TrainingPlan: The training plan.
    """
    html: str = client.get_html(HALF_MARATHON_3X12WEEKS_URL)
    training_plan_dto: TrainingPlanRunningAddictDTO = html_parser.parse_training_plan(
        html
    )
    training_plan: TrainingPlan = mapper.map_training_plan(training_plan_dto)

    return training_plan
