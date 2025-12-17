import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
USERNAME = os.getenv("SPOTIFY_USERNAME")
PLAYLIST_ID = os.getenv("SPOTIFY_PLAYLIST_ID")
REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")
SCOPE = "playlist-modify-public"


def get_spotify_client():
    """
    Create a Spotify client with proper authentication.
    Uses refresh token for non-interactive authentication in CI/CD environments.
    """
    # Create auth manager
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        open_browser=False,
        cache_path=".spotify_cache",
    )

    # If we have a refresh token, create a cache file with it
    if REFRESH_TOKEN:
        token_info = {
            "access_token": "",  # Will be refreshed
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": SCOPE,
            "expires_at": 0,  # Force refresh
            "refresh_token": REFRESH_TOKEN,
        }
        # Write to cache file
        with open(".spotify_cache", "w") as f:
            json.dump(token_info, f)

    return spotipy.Spotify(auth_manager=auth_manager)


# Create a Spotify client for searching (uses the same auth)
spotify = get_spotify_client()


def get_song_id(artist, song):
    results = spotify.search(q=f"artist:{artist} track:{song}", type="track")
    items = results["tracks"]["items"]
    if items:
        print(items[0]["id"])
        return items[0]["id"]
    else:
        print(f"No track found for artist: {artist}, song: {song}")
        return None


def add_songs_to_playlist(songs):
    try:
        # Create authenticated Spotify client
        sp = get_spotify_client()
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

        print(f"Added {len(song_ids)} new song(s) to the playlist.")
    except Exception as e:
        print(f"Error adding songs to playlist: {str(e)}")
        raise
