from exystence import get_albums_list
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
add_album(albums)
