from running_addict_plan_extractor.data import running_addict_api


def get_training_plan_title() -> str:
    title: str = running_addict_api.get_half_marathon_plan()
    return title
