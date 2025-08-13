import requests

HEADERS: dict[str, str] = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}


def get_html(url: str) -> str:
    """Retrieve the HTML content from a web page.

    Args:
        url (str): The URL to retrieve the HTML content from.

    Raises:
        HTTPError: If the HTTP request returned an unsuccessful status code.

    Returns:
        str: The HTML content of the response.
    """
    response: requests.Response = requests.get(url, headers=HEADERS)
    response.raise_for_status()
    return response.text
