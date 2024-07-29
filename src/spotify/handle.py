from thefuzz import fuzz

from src.constants import console
from src.exystence import Album

from .auth import cursor

sp = cursor()


def search_a_album(query: str) -> list:
    query = sp.search(q=query, type='album')
    return query['albums']['items']


def add_album(albums: list[Album]) -> list[Album]:
    """Saves the collected albums from exystence.net to user spotify library.

    Args:
        albums (Album): List of albums collected.

    Returns:
        Album: List of albums saved to user library.
    """

    success_add_albums = list()

    with console.status('[bold green]Working on albums...') as _:
        for album in albums:

            artist, title = album.title.split(' – ')
            title, year = title.rsplit(' ', 1)
            year = year[1:-1]

            items = search_a_album(
                f'album: {title} artist: {artist} year: {year}'
            )

            if item := items[0]:
                album_uri = item['uri']
                album_already_added = sp.current_user_saved_albums_contains(
                    [album_uri]
                )[0]

                artist_ratio = fuzz.ratio(artist, item['artists'][0]['name'])
                album_ratio = fuzz.ratio(title, item['name'])
                year_item = item['release_date'][:4]

                console.print(f'\nTrying to save {album.title}.')

                if (
                    not album_already_added
                    and artist_ratio > 98
                    and album_ratio > 60
                    and year == year_item
                ):
                    sp.current_user_saved_albums_add([album_uri])
                    success_add_albums.append(album)
                    console.print('✅ Saved in your spotify library.')
                    continue

                console.print('🔴 Not saved in your spotify library.')

    return success_add_albums
