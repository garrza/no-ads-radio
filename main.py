from modules.scraper import get_songs
from modules.spotify import add_songs_to_playlist


def main():
    """
    Main function that fetches songs from the radio station
    and adds them to the Spotify playlist.
    Designed to run once per execution
    """
    try:
        print("Fetching songs from radio station...")
        songs = get_songs()
        print(f"Found {len(songs)} song(s)")

        if songs:
            print("Adding songs to Spotify playlist...")
            add_songs_to_playlist(songs)
            print("✓ Process completed successfully!")
        else:
            print("No songs found to add.")

    except Exception as e:
        print(f"✗ An error occurred: {str(e)}")
        raise  # Raise to ensure GitHub Actions marks the run as failed


if __name__ == "__main__":
    main()
