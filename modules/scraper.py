from bs4 import BeautifulSoup
import requests

url = "https://onlineradiobox.com/mx/classicfm/?cs=mx.classicfm"


def get_songs():
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    songs = soup.find_all("td", class_="track_history_item")
    songs = [song.get_text(strip=True) for song in songs]

    songs = [song.split(" - ") for song in songs]
    return [song for song in songs if len(song) == 2]
