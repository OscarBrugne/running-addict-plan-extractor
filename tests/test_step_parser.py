from running_addict_plan_extractor.data.running_addict_api.step_parser import (
    parse_step,
)
from running_addict_plan_extractor.data.running_addict_api.dto import (
    StepRunningAddictDTO,
)
from running_addict_plan_extractor.model.enum import Pace
from running_addict_plan_extractor.model.model import (
    BaseStep,
    ConstantStep,
    IntervalStep,
    ProgressiveStep,
)

if __name__ == "__main__":
    # Run tests with python -m tests.test_step_parser
    print("TEST: Running Addict Step Parser")
    print("========================================")

    steps: list[str] = [
        "20’ EF",
        "50′ EF",
        "1h30 EF",
        "8×1′ allure 10km / récup: 1′ EF",
        "8 x 1’30 Allure 5km / 1’30 EF",
        "5×5′ Allure 42km récup : 3′ EF",
        "5×4′ allure 10km (récup:1’30 EF)",
        "4×5′ Allure 21km récup : 2′ EF",
        "3 x 2′ allure 21km (recup 2′ footing très lent)",
        "6×10″ sprint en côte / récup: 1’30 lent",
        "15′ progressif allure 42km > allure 10km",
        "20′ progressif Allure 42km > Allure 10km",
        "6x100m en accélération progressive",
        "SEMI-MARATHON !",
    ]

    for step in steps:
        print(f"Testing step: {step}")
        step_dto = StepRunningAddictDTO(description=step)
        parsed_step: BaseStep = parse_step(step_dto)
        print(f"  Parsed step: {parsed_step}")
        print()

    steps_errors: list[str] = [
        "10 x 30″ en côte (recup descente en footing lent)",
    ]
    for step in steps_errors:
        print(f"Testing step (expected error): {step}")
        step_dto = StepRunningAddictDTO(description=step)
        parsed_step: BaseStep = parse_step(step_dto)
        print(f"  Parsed step: {parsed_step}")
        print()
