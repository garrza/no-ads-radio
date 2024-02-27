import os
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
USERNAME = os.getenv("SPOTIFY_USERNAME")
PLAYLIST_ID = os.getenv("SPOTIFY_PLAYLIST_ID")
SCOPE = "playlist-modify-public"
TOKEN = util.prompt_for_user_token(
    username=USERNAME,
    scope=SCOPE,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    redirect_uri=REDIRECT_URI,
)

spotify = spotipy.Spotify(
    client_credentials_manager=SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
)


def get_song_id(artist, song):
    results = spotify.search(q=f"artist:{artist} track:{song}", type="track")
    items = results["tracks"]["items"]
    if items:
        print(items[0]["id"])
        return items[0]["id"]
    else:
        print(f"No track found for artist: {artist}, song: {song}")
        return None


def get_playlist_tracks():
    track_ids = []
    if TOKEN:
        sp = spotipy.Spotify(auth=TOKEN)
        sp.trace = False
        playlist = sp.user_playlist(USERNAME, PLAYLIST_ID)
        for item in playlist["tracks"]["items"]:
            track = item["track"]
            track_ids.append(track["id"])
    else:
        print("Can't get token for", USERNAME)

    return track_ids


def add_songs_to_playlist(songs):
    if TOKEN:
        sp = spotipy.Spotify(auth=TOKEN)
        sp.trace = False
        song_ids = [get_song_id(artist, song) for artist, song in songs]

        playlist_tracks = get_playlist_tracks()
        song_ids = [
            id for id in song_ids if id not in playlist_tracks if id is not None
        ]
        while song_ids:
            sp.user_playlist_add_tracks(USERNAME, PLAYLIST_ID, song_ids[:100])
            song_ids = song_ids[100:]

    else:
        print("Can't get token for", USERNAME)
        return None


get_playlist_tracks()
