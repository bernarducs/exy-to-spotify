from dataclasses import dataclass, field
import requests
from bs4 import BeautifulSoup
from dateutil.parser import parse
from datetime import datetime


@dataclass
class Album:
    title: str
    link: str
    date_post: datetime
    categories: list[str] = field(default_factory=list)


def get_albums_data(url: str) -> list[Album]:
    """Make requests to one exystence.net page collecting all the name
    and tag info from the albums and return a list of dataclasses.

    Args:
        url (str): The exystence url (it could be page/1, page/2 etc).

    Returns:
        list[Album]: List of dataclasses with album infos.
    """

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    divs = soup.find_all('div', {'class': 'posttop'})

    albums = list()
    for div in divs:
        title = div.find('h2', {'class': 'posttitle'}).find('a').text
        link = div.find('h2', {'class': 'posttitle'}).find('a').get('href')

        date: str = div.find('div', {'class': 'date'}).find('a').text
        date_post = parse(date)

        tags_element = div.find('div', {'class': 'categs'}).find_all('a')

        tags = list()
        for tag in tags_element:
            if tag.has_attr('rel') and tag['rel'] == ['category', 'tag']:
                tags.append(tag.text)

        albums.append(Album(title, link, date_post, tags))

    return albums
