import json
import requests
from bs4 import BeautifulSoup


def parse_url(url):
    # Make a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the response using BeautifulSoup
    soup = BeautifulSoup(response.content, "html.parser")

    # Extract the relevant content from the parsed HTML using BeautifulSoup
    title = soup.find("title").text
    description = soup.find("meta", attrs={"name": "description"})["content"]

    # Create a dictionary to hold the extracted content
    content = {"title": title, "description": description}

    # Write the content to a JSON file
    with open("content.json", "w") as f:
        json.dump(content, f)

    return content


url = "https://www.youtube.com/watch?v=W-oaVLRH-js"
parse_url(url)
