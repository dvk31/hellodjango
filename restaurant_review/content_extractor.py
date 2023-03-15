import requests
from bs4 import BeautifulSoup


def get_content_from_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")

    # Get the title
    title = soup.title.string if soup.title else "No Title"

    # Get the content
    content = soup.get_text()

    return title, content
