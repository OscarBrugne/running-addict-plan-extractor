from running_addict_plan_extractor.service import running_addict_service


def run() -> None:
    title: str = running_addict_service.get_training_plan_title()
    print(title)
    print()

    training_plan: str = running_addict_service.get_training_plan_str()
    print(training_plan)
    print()

    steps: list[str] = running_addict_service.get_steps_description()
    for step in steps:
        print(step)
