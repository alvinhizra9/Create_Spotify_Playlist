import requests
from bs4 import BeautifulSoup
import re

PATTERN = r'"nextPageLink":"([^"]+)"'
URL = "https://www.rollingstone.com/music/music-lists/best-hip-hop-albums-1323916/"


def get_albums() -> list[str]:
    """
    Get albums from rollingstone. com and return them as a list.


    @return list of albums in
    """
    url = URL
    albums = []
    # Get all the albums from the web page and add them to the list.
    while True:
        req = requests.get(url=url)

        soup = BeautifulSoup(req.content, "html.parser")

        soup.find_all(
            "li", class_="pmc-fallback-list-item-wrap lrv-u-margin-b-2"
        )

        # Add albums to the list of albums
        for album in soup.find_all("h2")[:50]:
            albums.append(album.get_text())

        text = str(soup.find("script", id="pmc-lists-front-js-extra"))

        match = re.search(PATTERN, text)

        # If match is None break the match.
        if match is None:
            break

        url = match.group(1).replace("\\", "")

    return albums
