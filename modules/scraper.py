from bs4 import BeautifulSoup
import requests

# Classic FM Monterrey playlist page - shows full day's history
PLAYLIST_URL = (
    "https://onlineradiobox.com/mx/classicfm/playlist/?cs=mx.classicfm&played=1"
)

# Keywords to filter out non-music entries (ads, station IDs, etc.)
SKIP_KEYWORDS = ["XHPJ", "MONTERREY", "ADWTAG", "LIGADOR", "NAVIDAD"]


def get_songs():
    """
    Scrapes the radio station playlist page for all songs played today.

    Returns:
        list: A list of [artist, song_title] pairs from the day's playlist.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    response = requests.get(PLAYLIST_URL, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, "html.parser")

    # Find the playlist table
    table = soup.find("table")
    if not table:
        print("⚠ Could not find playlist table")
        return []

    songs = []
    seen = set()  # Track unique songs to avoid duplicates

    for row in table.find_all("tr"):
        cells = row.find_all("td")
        if len(cells) < 2:
            continue

        track_text = cells[1].get_text(strip=True)

        # Skip ads, station IDs, and non-music entries
        if not track_text or any(skip in track_text.upper() for skip in SKIP_KEYWORDS):
            continue

        # Parse artist and song (format: "Artist - Song Title")
        if " - " not in track_text:
            continue

        artist, song_title = track_text.split(" - ", 1)
        artist = artist.strip()
        song_title = song_title.strip()

        if not artist or not song_title:
            continue

        # Create a unique key to avoid duplicates
        song_key = f"{artist.lower()}|{song_title.lower()}"

        if song_key not in seen:
            songs.append([artist, song_title])
            seen.add(song_key)
            print(f"Found: {artist} - {song_title}")

    print(f"\nTotal unique songs found: {len(songs)}")
    return songs
