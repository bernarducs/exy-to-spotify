from thefuzz import fuzz
from .auth import cursor


sp = cursor()


def add_album(albums):

    success_add_albums = list()

    for album in albums:

        artist, title = album.title.split(' – ')
        title, year = title.rsplit(' ', 1)
        year = year[1:-1]

        query = sp.search(q=f'album: {title} artist: {artist}', type='album')
        items = query['albums']['items']

        if item:= items[0]:
            album_uri = item['uri']
            album_already_added = sp.current_user_saved_albums_contains([album_uri])[0]

            artist_ratio = fuzz.ratio(artist, item['artists'][0]['name'])
            album_ratio = fuzz.ratio(title, item['name'])
            year_item = item['release_date'][:4]
            
            if not album_already_added and artist_ratio > 98 and album_ratio > 60 and year == year_item:
                sp.current_user_saved_albums_add([album_uri])
                success_add_albums.append(album)
     
    return success_add_albums
