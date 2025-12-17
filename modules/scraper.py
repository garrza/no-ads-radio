from bs4 import BeautifulSoup
import requests
from datetime import datetime, timedelta

# Use the playlist page which shows full day's history
url = "https://onlineradiobox.com/mx/classicfm/playlist/?cs=mx.classicfm&played=1"


def get_songs(hours_back=24):
    """
    Scrapes the radio station playlist page for all songs played.

    Args:
        hours_back: How many hours of history to fetch (default: 24 hours)
                   Set to None to get all available songs on the page

    Returns:
        A list of [artist, song_title] pairs.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")

    # Find the playlist table
    table = soup.find("table")
    if not table:
        print("Could not find playlist table")
        return []

    rows = table.find_all("tr")
    songs = []
    seen = set()  # Track unique songs to avoid duplicates

    for row in rows:
        cells = row.find_all("td")
        if len(cells) >= 2:
            # First cell is time, second cell is track info
            time_text = cells[0].get_text(strip=True)
            track_text = cells[1].get_text(strip=True)

            # Skip ads, station IDs, and non-music entries
            if not track_text or any(
                skip in track_text.upper()
                for skip in ["XHPJ", "MONTERREY", "ADWTAG", "LIGADOR", "NAVIDAD"]
            ):
                continue

            # Parse artist and song (format: "Artist - Song Title")
            if " - " in track_text:
                parts = track_text.split(" - ", 1)
                if len(parts) == 2:
                    artist = parts[0].strip()
                    song_title = parts[1].strip()

                    # Create a unique key to avoid duplicates
                    song_key = f"{artist.lower()}|{song_title.lower()}"

                    if song_key not in seen and artist and song_title:
                        songs.append([artist, song_title])
                        seen.add(song_key)
                        print(f"Found: {artist} - {song_title}")

    print(f"\nTotal unique songs found: {len(songs)}")
    return songs
