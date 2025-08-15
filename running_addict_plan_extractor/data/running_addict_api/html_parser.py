import bs4

from running_addict_plan_extractor.data.running_addict_api.dto import (
    StepDTO,
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
    assert plan_anchor, "Training plan anchor not found in the HTML."

    training_plan_container: bs4.element.PageElement | None = plan_anchor.find_next(
        "div", class_="tdc-row stretch_row"
    )
    assert training_plan_container, "Training plan container not found in the HTML."
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
    assert title_tag, "Training plan title <h4> not found in the HTML."

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
    # TODO: Implement week extraction logic
    return weeks
