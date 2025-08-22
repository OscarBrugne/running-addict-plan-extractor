from running_addict_plan_extractor.config import TrainingPlanType
from running_addict_plan_extractor.data import client
from running_addict_plan_extractor.data.running_addict_api import html_parser
from running_addict_plan_extractor.data.running_addict_api.dto import (
    TrainingPlanRunningAddictDTO,
)
from running_addict_plan_extractor.data.running_addict_api import mapper
from running_addict_plan_extractor.model.model import TrainingPlan


TRAINING_PLAN_URLS: dict[TrainingPlanType, str] = {
    TrainingPlanType.HALF_MARATHON_3X12WEEKS: "https://www.running-addict.fr/plan-dentrainement-semi-marathon-3-seances-sur-12-semaines/",
    TrainingPlanType.HALF_MARATHON_4X12WEEKS: "https://www.running-addict.fr/plan-dentrainement-semi-marathon-4-seances-sur-12-semaines/",
    TrainingPlanType.HALF_MARATHON_1H30: "https://www.running-addict.fr/plan-dentrainement-semi-marathon-1h30/",
}


def get_half_marathon_plan(plan_type: TrainingPlanType) -> TrainingPlan:
    """Retrieve the Half Marathon 3x12 Weeks training plan from Running Addict.

    Returns:
        TrainingPlan: The training plan.
    """
    url: str = TRAINING_PLAN_URLS[plan_type]
    html: str = client.get_html(url)
    training_plan_dto: TrainingPlanRunningAddictDTO = html_parser.parse_training_plan(
        html
    )
    training_plan: TrainingPlan = mapper.map_training_plan(training_plan_dto)

    return training_plan
