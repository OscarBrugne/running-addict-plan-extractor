import re

from running_addict_plan_extractor.data.running_addict_api.dto import (
    StepRunningAddictDTO,
)
from running_addict_plan_extractor.model.enum import PaceType
from running_addict_plan_extractor.model.model import (
    BaseStep,
    ConstantStep,
    IntervalStep,
    ProgressiveStep,
)

# Regular expressions for parsing step descriptions
DURATION_REGEX: re.Pattern[str] = re.compile(
    r"(?:(?P<hours>\d+)h)?\s*(?:(?P<minutes>\d+)'?)?\s*(?:(?P<seconds>\d+)\")?",
    re.IGNORECASE,
)
PACE_REGEX: re.Pattern[str] = re.compile(
    r"(ef|allure\s*(?:5|10|21|42)km|.*footing.*|.*lent.*|.*côte.*)",
    re.IGNORECASE,
)
CONSTANT_STEP_REGEX: re.Pattern[str] = re.compile(
    r"(?:(?P<hours>\d+)h|(?P<minutes>\d+)'|(?P<seconds>\d+)\")\s*(?P<pace>.+)",
    re.IGNORECASE,
)
INTERVAL_STEP_REGEX: re.Pattern[str] = re.compile(
    r"(?P<repeat>\d+)x(?P<workout>.+?)\s*(?:/?\s*r[eé]cup|/)\s*:?\s*(?P<rest>.+)$",
    re.IGNORECASE,
)
PROGRESSIVE_STEP_REGEX: re.Pattern[str] = re.compile(
    r"(?:(?P<hours>\d+)h)?\s*(?:(?P<minutes>\d+)'?)?\s*(?:(?P<seconds>\d+)\")?\s*progressif\s*(?P<start_pace>.+?)\s*>\s*(?P<end_pace>.+)",
    re.IGNORECASE,
)


class ParseError(Exception):
    pass


def parse_step(step_dto: StepRunningAddictDTO) -> BaseStep:
    description: str = (
        step_dto.description.replace(" x", "x").replace("x ", "x").lower().strip()
    )
    try:
        if CONSTANT_STEP_REGEX.match(description):
            return parse_constant_step(description)
        if INTERVAL_STEP_REGEX.match(description):
            return parse_interval_step(description)
        if PROGRESSIVE_STEP_REGEX.match(description):
            return parse_progressive_step(description)
    except ParseError as e:
        # Error while parsing step, returning base step
        # TODO : Use a logging framework instead of print
        print(f"Error while parsing step '{description}': {e}")
    except Exception as e:
        # TODO : Use a logging framework instead of print
        print(f"Unexpected error while parsing step '{description}': {e}")

    return BaseStep(description=description)


def parse_duration(duration_str: str) -> float:
    match: re.Match[str] | None = DURATION_REGEX.match(duration_str)
    if not match:
        raise ParseError(f"Unknown duration format: '{duration_str}'")

    hours = int(match.group("hours") or 0)
    minutes = int(match.group("minutes") or 0)
    seconds = int(match.group("seconds") or 0)

    return hours * 60 + minutes + seconds / 60


def parse_pace(pace_str: str) -> PaceType:
    match: re.Match[str] | None = PACE_REGEX.search(pace_str)
    if not match:
        raise ParseError(f"Unknown pace format: '{pace_str}'")

    pace_val: str = match.group(1).lower()
    if "ef" in pace_val in pace_val:
        return PaceType.BASE
    if "5km" in pace_val:
        return PaceType.FIVE_KM
    if "10km" in pace_val:
        return PaceType.TEN_KM
    if "21km" in pace_val:
        return PaceType.HALF_MARATHON
    if "42km" in pace_val:
        return PaceType.MARATHON
    if "footing" in pace_val or "lent" in pace_val:
        return PaceType.SLOW
    if "côte" in pace_val:
        return PaceType.HILL

    raise ParseError(f"Unknown pace format: '{pace_str}'")


def parse_constant_step(description: str) -> ConstantStep:
    match: re.Match[str] | None = CONSTANT_STEP_REGEX.match(description)
    if not match:
        raise ParseError(f"Unknown constant step format: '{description}'")

    duration_str: str = description.replace(match.group("pace"), "").strip()
    pace_str: str = match.group("pace").strip()
    duration_minutes: float = parse_duration(duration_str)
    pace: PaceType = parse_pace(pace_str)

    return ConstantStep(
        description=description, duration_minutes=duration_minutes, pace=pace
    )


def parse_interval_step(description: str) -> IntervalStep:
    match: re.Match[str] | None = INTERVAL_STEP_REGEX.match(description)
    if not match:
        raise ParseError(f"Unknown interval step format: '{description}'")

    repeat_count: int = int(match.group("repeat"))
    workout_desc: str = match.group("workout").strip()
    rest_desc: str | None = match.group("rest").strip()
    if not rest_desc:
        raise ParseError(f"Unknown rest format: '{description}'")

    workout: ConstantStep = parse_constant_step(workout_desc)
    rest: ConstantStep = parse_constant_step(rest_desc)

    return IntervalStep(
        description=description, repeat_count=repeat_count, workout=workout, rest=rest
    )


def parse_progressive_step(description: str) -> ProgressiveStep:
    match: re.Match[str] | None = PROGRESSIVE_STEP_REGEX.match(description)
    if not match:
        raise ParseError(f"Unknown progressive step format: '{description}'")

    duration_str: str = description.split("progressif")[0].strip()
    duration_minutes: float = parse_duration(duration_str)
    start_pace: PaceType = parse_pace(match.group("start_pace").strip())
    end_pace: PaceType = parse_pace(match.group("end_pace").strip())

    return ProgressiveStep(
        description=description,
        duration_minutes=duration_minutes,
        start_pace=start_pace,
        end_pace=end_pace,
    )
