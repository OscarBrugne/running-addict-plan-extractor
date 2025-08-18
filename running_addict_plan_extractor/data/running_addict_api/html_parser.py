import bs4

from running_addict_plan_extractor.data.running_addict_api.dto import (
    StepRunningAddictDTO,
    WorkoutRunningAddictDTO,
    WeekRunningAddictDTO,
    TrainingPlanRunningAddictDTO,
)


def parse_training_plan(html: str) -> TrainingPlanRunningAddictDTO:
    """
    Parse the HTML content of a training plan from the Running Addict website.

    Args:
        html (str): The HTML content to parse.

    Returns:
        TrainingPlanRunningAddictDTO: The parsed training plan data.
    """
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(html, "html.parser")
    training_plan_container: bs4.Tag = extract_training_plan_container(soup)
    title: str = extract_title(training_plan_container)
    weeks: list[WeekRunningAddictDTO] = extract_weeks(training_plan_container)
    return TrainingPlanRunningAddictDTO(title, weeks)


def extract_training_plan_container(soup: bs4.BeautifulSoup) -> bs4.Tag:
    """
    Extract the container containing the training plan details.

    Args:
        soup (bs4.BeautifulSoup): The BeautifulSoup object representing the HTML.

    Returns:
        bs4.Tag: The training plan container element.
    """
    plan_anchor: bs4.Tag | None = soup.select_one("#plandentrainement")
    assert (
        plan_anchor
    ), "Training plan anchor '#plandentrainement' not found in the HTML."

    training_plan_container: bs4.element.PageElement | None = plan_anchor.find_next(
        "div", class_="tdc-row stretch_row"
    )
    assert (
        training_plan_container
    ), "Training plan container 'div.tdc-row.stretch_row' not found in the HTML."
    assert isinstance(
        training_plan_container, bs4.Tag
    ), "Training plan container is not a valid HTML element."

    return training_plan_container


def extract_title(training_plan_container: bs4.Tag) -> str:
    """Extract the title of the training plan.

    Args:
        training_plan_container (bs4.Tag): The training plan container element.

    Returns:
        str: The title of the training plan.
    """
    title_tag: bs4.Tag | None = training_plan_container.select_one("h4")
    assert title_tag, "Training plan title 'h4' not found in the HTML."

    title: str = title_tag.get_text(strip=True)
    return title


def extract_weeks(training_plan_container: bs4.Tag) -> list[WeekRunningAddictDTO]:
    """
    Extract the weeks of the training plan.

    Args:
        training_plan_container (bs4.Tag): The training plan container element.

    Returns:
        list[WeekRunningAddictDTO]: The list of weeks in the training plan.
    """
    weeks: list[WeekRunningAddictDTO] = []

    weeks_container: bs4.Tag | None = training_plan_container.select_one("#accordion")
    assert weeks_container, "Weeks container '#accordion' not found in the HTML."

    week_cards: bs4.ResultSet[bs4.Tag] = weeks_container.select(":scope > .card")
    for week_card in week_cards:
        week: WeekRunningAddictDTO = extract_week(week_card)
        weeks.append(week)

    return weeks


def extract_week(week_card: bs4.Tag) -> WeekRunningAddictDTO:
    """
    Extract details of a the week.

    Args:
        week_card (bs4.Tag): The week card element.

    Returns:
        WeekRunningAddictDTO: The extracted week data.
    """
    week_tag: bs4.Tag | None = week_card.select_one(".semaine")
    assert week_tag, "Week tag '.semaine' not found in week card"

    raw_week: str = week_tag.get_text(strip=True)

    workouts_container: bs4.Tag | None = week_card.select_one(".inneracco")
    assert workouts_container, "Workouts container '.inneracco' not found in week card"

    workouts: list[WorkoutRunningAddictDTO] = []
    workouts_divs: bs4.ResultSet[bs4.Tag] = workouts_container.select(":scope > .card")
    for workouts_div in workouts_divs:
        workout: WorkoutRunningAddictDTO = extract_workout(workouts_div)
        workouts.append(workout)

    return WeekRunningAddictDTO(week=raw_week, workouts=workouts)


def extract_workout(workout_div: bs4.Tag) -> WorkoutRunningAddictDTO:
    """
    Extract details of a workout.

    Args:
        workout_div (bs4.Tag): The workout div element.

    Returns:
        WorkoutRunningAddictDTO: The extracted workout data.
    """
    header: bs4.Tag | None = workout_div.select_one(".card-header")
    assert header, "Workout header '.card-header' not found in workout div"

    spans: bs4.ResultSet[bs4.Tag] = header.select("span")
    assert len(spans) == 3, "Workout header does not contain 3 span elements"

    raw_day: str = spans[0].get_text(strip=True)
    raw_duration: str = spans[1].get_text(strip=True)
    effort_level: int = len(spans[2].select(".fa-tint"))

    steps: list[StepRunningAddictDTO] = extract_steps(workout_div)

    coach_advice_tag: bs4.Tag | None = workout_div.select_one(".right-sec p")
    assert (
        coach_advice_tag
    ), "Coach advice paragraph '.right-sec p' not found in workout div"

    coach_advice: str = coach_advice_tag.get_text(strip=True)

    return WorkoutRunningAddictDTO(
        day=raw_day,
        duration=raw_duration,
        effort_level=effort_level,
        steps=steps,
        coach_advice=coach_advice,
    )


def extract_steps(workout_div: bs4.Tag) -> list[StepRunningAddictDTO]:
    """
    Extract the steps of a workout.

    Args:
        workout_div (bs4.Tag): The workout div element containing steps.

    Returns:
        list[StepDTO]: The list of extracted steps.
    """
    steps_container: bs4.Tag | None = workout_div.select_one(".left-sec")
    assert steps_container, "Left section '.left-sec' not found in workout card"

    steps: list[StepRunningAddictDTO] = []
    step_divs: bs4.ResultSet[bs4.Tag] = steps_container.select("div")
    for step_div in step_divs:
        raw_step_description: str = step_div.get_text(strip=True)
        assert raw_step_description, "Empty step description found in steps container"
        steps.append(StepRunningAddictDTO(description=raw_step_description))

    return steps
