import os
import json
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Spotify API credentials
CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = os.getenv("SPOTIFY_REDIRECT_URI")
REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")

# Playlist configuration
USERNAME = os.getenv("SPOTIFY_USERNAME")
PLAYLIST_ID = os.getenv("SPOTIFY_PLAYLIST_ID")
SCOPE = "playlist-modify-public"


def get_spotify_client():
    """
    Create an authenticated Spotify client.

    Uses refresh token for non-interactive authentication, suitable for CI/CD.

    Returns:
        spotipy.Spotify: Authenticated Spotify client.
    """
    auth_manager = SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        open_browser=False,
        cache_path=".spotify_cache",
    )

    # Create cache file with refresh token for non-interactive auth
    if REFRESH_TOKEN:
        token_info = {
            "access_token": "",
            "token_type": "Bearer",
            "expires_in": 3600,
            "scope": SCOPE,
            "expires_at": 0,  # Force token refresh
            "refresh_token": REFRESH_TOKEN,
        }
        with open(".spotify_cache", "w") as f:
            json.dump(token_info, f)

    return spotipy.Spotify(auth_manager=auth_manager)


# Create a Spotify client for searching (uses the same auth)
spotify = get_spotify_client()


def get_song_id(artist, song):
    """
    Search for a song on Spotify and return its track ID.

    Args:
        artist: The artist name.
        song: The song title.

    Returns:
        str: Spotify track ID if found, None otherwise.
    """
    query = f"artist:{artist} track:{song}"
    results = spotify.search(q=query, type="track", limit=1)
    items = results["tracks"]["items"]
    return items[0]["id"] if items else None


def add_songs_to_playlist(songs):
    """
    Add songs to the Spotify playlist, skipping duplicates.

    Args:
        songs: List of [artist, song_title] pairs to add.
    """
    try:
        sp = get_spotify_client()
        sp.trace = False

        # Fetch all current tracks in the playlist
        print("Checking existing playlist tracks...")
        current_tracks = set()
        offset = 0
        while True:
            response = sp.playlist_tracks(
                PLAYLIST_ID, offset=offset, fields="items(track(id)),next"
            )
            current_tracks.update(
                item["track"]["id"] for item in response["items"] if item["track"]
            )
            if not response["next"]:
                break
            offset += len(response["items"])

        print(f"Playlist currently has {len(current_tracks)} tracks\n")

        # Search for songs and collect track IDs
        song_ids = []
        for artist, song in songs:
            song_id = get_song_id(artist, song)

            if not song_id:
                print(f"  ✗ Not found on Spotify: {artist} - {song}")
            elif song_id in current_tracks:
                print(f"  ⊘ Already in playlist: {artist} - {song}")
            else:
                song_ids.append(song_id)
                print(f"  ✓ Will add: {artist} - {song}")

        # Add songs to playlist in batches of 100 (Spotify API limit)
        if song_ids:
            print(f"\nAdding {len(song_ids)} new song(s) to playlist...")
            for i in range(0, len(song_ids), 100):
                batch = song_ids[i : i + 100]
                sp.user_playlist_add_tracks(USERNAME, PLAYLIST_ID, batch)
                print(f"  Added batch {i // 100 + 1} ({len(batch)} songs)")
            print(f"\n✓ Successfully added {len(song_ids)} song(s)!")
        else:
            print("\nNo new songs to add (all songs already in playlist).")

    except Exception as e:
        print(f"\n✗ Error adding songs to playlist: {str(e)}")
        raise
