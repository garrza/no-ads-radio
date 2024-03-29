# Radio Station Song Fetcher Bot

This project is an automated bot built using Python, the Spotify API, and web scraping. The bot fetches songs from a local radio station and adds them to a Spotify playlist, providing a seamless and ad-free listening experience.

## Features

- Automatically fetches songs from a local radio station.
- Adds fetched songs to a Spotify playlist.
- Hosted on Google Cloud Functions for scalability and easy management.
- Scheduled HTTP calls ensure that the playlist stays updated every 60 minutes.

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/your_username/radio-station-song-fetcher.git
   cd radio-station-song-fetcher
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Set up your Spotify Developer account and obtain API credentials.
2. Configure the bot with your Spotify API credentials and the URL of the radio station.
3. Deploy the bot to Google Cloud Functions.
4. Set up a scheduled HTTP call to trigger the bot every 60 minutes.

## Configuration

You need to configure the following environment variables:

- `SPOTIFY_CLIENT_ID`: Your Spotify API client ID.
- `SPOTIFY_CLIENT_SECRET`: Your Spotify API client secret.
- `RADIO_STATION_URL`: The URL of the local radio station's website.

## Link to Playlist

You can access the playlist generated by the bot [here](https://open.spotify.com/playlist/2nGXIsEZ0ggH2M2shAsCmg?si=5fe3038a63b2471b).

## Contributing

Contributions are welcome! Feel free to open issues or submit pull requests to improve the project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
