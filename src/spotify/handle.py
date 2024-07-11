from datetime import datetime, timezone
from dataclasses import dataclass, field

from .auth import cursor


sp = cursor()


def add_album(albums):

    success_add_albums = list()

    for album in albums:

        artist, title = album.title.split(' – ')

        query = sp.search(q=f'album: {title} artist: {artist}', type='album')
        items = query['albums']['items']

        if items:
            album_uri = items[0]['uri']
            sp.current_user_saved_albums_add([album_uri])
            success_add_albums.append(album)
            print(f'\n\n{title}, from {artist} was successfully added')

        else:
            print(f"\n\n{title}, from {artist} wasn't successfully added")

    print(
        f'\n\n\n{len(success_add_albums)} was added to your spotify library.'
    )
    return success_add_albums
