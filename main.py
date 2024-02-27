import time
from modules.scraper import get_songs
from modules.spotify import add_songs_to_playlist

FETCH_INTERVAL = 20


def main():
    while True:
        try:
            songs = get_songs()
            add_songs_to_playlist(songs)
            print("Songs added to playlist successfully.")

        except Exception as e:
            print(f"An error occurred: {str(e)}")
        time.sleep(FETCH_INTERVAL)


if __name__ == "__main__":
    main()
