from bs4 import BeautifulSoup
import requests

url = "https://onlineradiobox.com/mx/classicfm/?cs=mx.classicfm"


def get_songs():
    """
    Scrapes the radio station website for currently playing songs.
    Returns a list of [artist, song_title] pairs.
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    page = requests.get(url, headers=headers)
    soup = BeautifulSoup(page.content, "html.parser")
    
    track_elements = soup.find_all("td", class_="track_history_item")
    songs = []
    
    for track in track_elements:
        # Artist is in <b> tag, song title is the remaining text
        artist_tag = track.find("b")
        if artist_tag:
            artist = artist_tag.get_text(strip=True)
            # Get the full text and remove the artist part to get the song title
            full_text = track.get_text(strip=True)
            song_title = full_text.replace(artist, "", 1).strip()
            
            if artist and song_title:
                songs.append([artist, song_title])
                print(f"Found: {artist} - {song_title}")
    
    return songs
