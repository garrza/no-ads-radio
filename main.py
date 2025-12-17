from modules.scraper import get_songs
from modules.spotify import add_songs_to_playlist


def main():
    """
    Main entry point: fetch songs from radio station and add to Spotify playlist.
    """
    print("=" * 60)
    print("No Ads Radio - Classic FM → Spotify")
    print("=" * 60)

    try:
        print("\nFetching songs from radio station...")
        songs = get_songs()

        if not songs:
            print("\nNo songs found to add.")
            return

        print(f"\nAdding songs to Spotify playlist...")
        add_songs_to_playlist(songs)

        print("\n" + "=" * 60)
        print("✓ Process completed successfully!")
        print("=" * 60)

    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        raise  # Re-raise to fail GitHub Actions workflow


if __name__ == "__main__":
    main()
