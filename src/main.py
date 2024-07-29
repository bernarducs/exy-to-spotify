from exystence import dump_last_albums, get_albums_list
from spotify import add_album

CATEGORIES = [
    'reggae',
    'dub',
    'soul',
    'rock',
    'southern',
    'blues',
    'americana',
]

albums = get_albums_list(CATEGORIES)

if albums:
    saved_albums = add_album(albums)

    if saved_albums:
        dump_last_albums(saved_albums)

    print(f'\n💃🕺 End of task. Total of {len(saved_albums)} albums saved!')
