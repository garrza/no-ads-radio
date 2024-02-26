import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
USERNAME = os.getenv("SPOTIFY_USERNAME")
PLAYLIST_ID = os.getenv("SPOTIFY_PLAYLIST_ID")

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
)


def get_song_id(artist, song):
    results = spotify.search(q=f"artist:{artist} track:{song}", type="track")
    try:
        print(results["tracks"]["items"][0]["id"])
        return results["tracks"]["items"][0]["id"]
    except IndexError:
        return None


def add_songs_to_playlist(songs):
    song_ids = [get_song_id(artist, song) for artist, song in songs]
    song_ids = [id for id in song_ids if id is not None]
    spotify.user_playlist_add_tracks(USERNAME, PLAYLIST_ID, song_ids)
