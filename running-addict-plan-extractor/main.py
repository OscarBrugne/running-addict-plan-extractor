import requests
import bs4

URL = "https://www.running-addict.fr/plan-dentrainement-semi-marathon-3-seances-sur-12-semaines/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}


def get_html(url: str) -> str:
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.text


def parse_training_plan(html: str) -> bs4.element.PageElement:
    soup = bs4.BeautifulSoup(html, "html.parser")

    plan_anchor = soup.select_one("#plandentrainement")
    if not plan_anchor:
        raise ValueError("Training plan anchor not found in the HTML.")

    training_plan_container = plan_anchor.find_next("div", class_="tdc-row stretch_row")
    if not training_plan_container:
        raise ValueError("Training plan container not found in the HTML.")

    return training_plan_container


if __name__ == "__main__":
    url: str = URL

    html: str = get_html(url)
    training_plan: bs4.element.PageElement = parse_training_plan(html)
    print(training_plan)
