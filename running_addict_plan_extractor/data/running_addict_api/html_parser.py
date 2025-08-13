import bs4


def parse_training_plan_title(html: str) -> str:
    """Parse the title of the training plan the HTML content.

    Args:
        html (str): The HTML content of the training plan page.

    Returns:
        str: The title of the training plan.
    """
    soup: bs4.BeautifulSoup = bs4.BeautifulSoup(html, "html.parser")

    plan_anchor: bs4.Tag | None = soup.select_one("#plandentrainement")
    assert plan_anchor, "Training plan anchor not found in the HTML."

    training_plan_container: bs4.element.PageElement | None = plan_anchor.find_next(
        "div", class_="tdc-row stretch_row"
    )
    assert training_plan_container, "Training plan container not found in the HTML."
    assert isinstance(
        training_plan_container, bs4.Tag
    ), "Training plan container is not a valid HTML element."

    title_tag: bs4.Tag | None = training_plan_container.select_one("h4")
    assert title_tag, "Training plan title <h4> not found in the HTML."

    title: str = title_tag.get_text(strip=True)
    return title
