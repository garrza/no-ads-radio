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
            print(track["id"])
    else:
        print("Can't get token for", USERNAME)

    return track_ids


def add_songs_to_playlist(songs):
    if TOKEN:
        sp = spotipy.Spotify(auth=TOKEN)
        sp.trace = False

        # Get the current track IDs in the playlist
        current_tracks = []
        offset = 0
        while True:
            response = sp.playlist_tracks(PLAYLIST_ID, offset=offset)
            current_tracks += [item["track"]["id"] for item in response["items"]]
            offset += len(response["items"])
            if not response["next"]:
                break

        song_ids = []
        for song_info in songs:
            if len(song_info) == 2:
                artist, song = song_info
                song_id = get_song_id(artist, song)
                if song_id:
                    if (
                        song_id not in current_tracks
                    ):  # Check if the song is not already in the playlist
                        song_ids.append(song_id)
                    else:
                        print(
                            f"Song '{song}' by '{artist}' is already in the playlist."
                        )
                else:
                    print(f"Song ID not found for {artist} - {song}")
            else:
                print(f"Invalid entry: {song_info}")

        while song_ids:
            sp.user_playlist_add_tracks(USERNAME, PLAYLIST_ID, song_ids[:100])
            song_ids = song_ids[100:]
    else:
        print("Can't get token for", USERNAME)
