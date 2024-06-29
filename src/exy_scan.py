import os
import pickle
from dataclasses import dataclass, field

import requests
from bs4 import BeautifulSoup

LAST_ALBUM_FILE = f'{os.getcwd()}/last_albums'
URL = 'https://exystence.net/page'


def get_albums_list(
    user_categories: list[str] = None, max_entries: int = 20
) -> list[str] | bool:
    """This functions agregate whole functions in this file returning the
    final list requested by user to be added in his spotify library.

        If there is a pickle file with the last album, this functions will search
    for new albums until to complete the max_entries.

        If there is no a last album, it will search for the last new albums to
    complete the max_entries.

    Args:
        user_categories (list[str]): List of genres/tags defined by user.
        max_entries (int, optional): Max albums to be collected. Defaults to 20.

    Returns:
        list[str] | bool: List of albums to be add in user's spotify library.
    """

    last_album = get_last_album()
    if bool(last_album):
        print(
            f'Your last album collected was "{last_album}".\n'
            f'We will try {max_entries} first albums since it.\n'
        )

    n = 1
    new_entries = list()

    while True:
        albums = get_albums_info(f'{URL}/{n}')
        filtered_albums = filter_categories(albums, user_categories)

        new_entries.extend(filtered_albums)

        if last_album in new_entries:
            pos_last_album = new_entries.index(last_album)
            new_entries = new_entries[:pos_last_album]

            if len(new_entries) > 0:
                print(
                    f'{len(new_entries)} new albums collected since the last album.'
                )
            break

        if len(new_entries) >= max_entries:
            new_entries = new_entries[:max_entries]
            print(f'{len(new_entries)} new albums collected!')
            break

        print(f'Colleting new albums from the page {n}...')
        n = n + 1

        # if last_album in [a.title for a in albums]:
        #     break

    if new_entries:
        save_last_abum(new_entries[0])
        return new_entries

    print('There is no albums to be collected.')
    return False


def filter_categories(
    albums: dataclass, user_categories: list[str]
) -> list[str]:
    """Return a list filtered by tags/categories defined by user.

    Args:
        albums (dataclass): An album dataclass.
        user_categories (list[str]): List of tags defined by user.

    Returns:
        list[str]: List of album's titles.
    """

    if user_categories:
        return [
            album.title
            for album in albums
            if bool(set(album.categories) & set(user_categories))
        ]

    return [album.title for album in albums]


def album_dataclass(
    album_title: str, album_categories: list[str]
) -> dataclass:
    """Function that return a album dataclass.

    Args:
        album_title (str): Title of album.
        album_categories (list[str]): The tags of album (rock, jazz, punk...)

    Returns:
        dataclass: Album dataclass.
    """

    @dataclass
    class Album:
        title: str
        categories: list[str] = field(default_factory=list)

    return Album(album_title, album_categories)


def get_albums_info(url: str) -> list[dataclass]:
    """Make requests to the site target collecting all the name and tag info
    from the albums and return a list of dataclasses.

    Args:
        url (str): The exystence url (it could be page/1, page/2 etc).

    Returns:
        list[dataclass]: List of dataclasses with album infos.
    """

    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    divs = soup.find_all('div', {'class': 'posttop'})

    new_albums = list()
    for div in divs:
        title = div.find('h2', {'class': 'posttitle'}).find('a').text

        tags_element = div.find('div', {'class': 'categs'}).find_all('a')

        tags = list()
        for tag in tags_element:
            if tag.has_attr('rel') and tag['rel'] == ['category', 'tag']:
                tags.append(tag.text)

        new_albums.append(album_dataclass(title, tags))

    return new_albums


def get_last_album() -> str:
    """Get the last album pickled.

    Returns:
        str: Title of last album.
    """

    if not os.path.exists(LAST_ALBUM_FILE):
        return ''

    with open(LAST_ALBUM_FILE, 'rb') as f:
        last_album = pickle.load(f)

    return last_album


def save_last_abum(album_name: str) -> None:
    """Saves a pickle file of last album.

    Args:
        album_name (str): Title of last album.
    """

    with open(LAST_ALBUM_FILE, 'wb') as f:
        pickle.dump(album_name, f)
