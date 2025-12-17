"""
No Ads Radio - Automated Spotify Playlist Updater
Scrapes Classic FM Monterrey playlist and adds songs to Spotify.
"""

from modules.scraper import get_songs
from modules.spotify import add_songs_to_playlist


def main():
    """
    Main entry point: fetch songs from radio station and add to Spotify playlist.
    """
    print("=" * 60)
    print("No Ads Radio - Classic FM Monterrey → Spotify")
    print("=" * 60)

    try:
        print("\n📻 Fetching songs from radio station...")
        songs = get_songs()

        if not songs:
            print("\n⚠ No songs found to add.")
            return

        print(f"\n🎵 Adding songs to Spotify playlist...")
        add_songs_to_playlist(songs)

        print("\n" + "=" * 60)
        print("✓ Process completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        raise  # Re-raise to fail GitHub Actions workflow


if __name__ == "__main__":
    main()
