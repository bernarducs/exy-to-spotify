import os
import pickle

from .scrape import Album, get_albums_data


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

    if last_album := get_last_album():
        print(
            f'\n\n\nYour last album collected was "{last_album.title}".\n'
            f'We will try {max_entries} first albums since it.\n'
        )
    else:
        print(
            "\n\n\nWe didn't find the last album added. We will collect new albums until page 20."
        )

    page = 1
    new_entries = list()

    while page <= 20:
        print(f'\n\nColleting new albums from the page {page}...')

        albums = get_albums_data(f'{URL}/{page}')
        filtered_albums = filter_categories(albums, user_categories)

        new_entries.extend(filtered_albums)

        if last_album in new_entries:
            pos_last_album = new_entries.index(last_album)
            new_entries = new_entries[:pos_last_album]
            break

        if len(new_entries) >= max_entries:
            new_entries = new_entries[:max_entries]
            break

        page += 1

    if new_entries:
        print(f'{len(new_entries)} new albums collected!')
        save_last_albums(new_entries)
        return new_entries

    print('There is no albums to be collected.')
    return False


def filter_categories(
    albums: list[Album], user_categories: list[str]
) -> list[Album]:
    """Return a list filtered by tags/categories defined by user.

    Args:
        albums (dataclass): An album dataclass.
        user_categories (list[str]): List of tags defined by user.

    Returns:
        list[str]: List of album's titles.
    """

    if user_categories:
        return [
            album
            for album in albums
            if bool(set(album.categories) & set(user_categories))
        ]

    return albums


def save_last_albums(albums: list[Album]) -> None:
    """Saves a pickle file of last album.

    Args:
        album_name (str): Title of last album.
    """

    with open(LAST_ALBUM_FILE, 'wb') as f:
        pickle.dump(albums, f)


def get_last_album() -> Album | str:
    """Get the last album pickled.

    Returns:
        Album: Album dataclass.
    """

    if not os.path.exists(LAST_ALBUM_FILE):
        return ''

    with open(LAST_ALBUM_FILE, 'rb') as f:
        albums = pickle.load(f)

    return albums[0]
