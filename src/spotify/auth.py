import spotipy
from dotenv import dotenv_values
from spotipy.oauth2 import SpotifyOAuth


def cursor():
    config = dotenv_values('.env')

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=config['CLIENT_ID'],
            client_secret=config['CLIENT_SECRET'],
            redirect_uri=config['REDIRECT_URI'],
            username=config['USERNAME'],
            scope=config['scope'],
        )
    )

    return sp
