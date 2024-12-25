import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from flask import Flask, render_template


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/fetch-songs", methods=["POST"])
def submit():
    # Authenticate with Spotify
    CLIENT_ID, CLIENT_SECRET = load_environment_variables()
    sp = authenticate_spotify(CLIENT_ID, CLIENT_SECRET)

    # Fetch and store liked songs
    liked_songs = fetch_liked_songs(sp)

    # Fetch and store tracks from all playlists
    playlist_tracks = fetch_all_playlist_tracks(sp)

    # Combine liked songs and playlist tracks
    all_songs = liked_songs + playlist_tracks

    # Pass all songs to the template
    return render_template("index.html", songs=all_songs)


def load_environment_variables():
    # Load environment variables from .env file
    if not load_dotenv():
        print(
            "Error: Could not load the environment variables. Please ensure you have a .env file with your credentials."
        )
        exit(1)

    CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
    CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")

    if not CLIENT_ID or not CLIENT_SECRET:
        print(
            "Error: Missing Spotify Client ID or Client Secret in the environment variables."
        )
        exit(1)

    return CLIENT_ID, CLIENT_SECRET


def authenticate_spotify(client_id, client_secret):
    # Authenticate with Spotify
    REDIRECT_URI = "http://localhost:8888/callback"
    SCOPE = "user-library-read playlist-read-private playlist-read-collaborative"

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            cache_path="/.cache",
        )
    )

    return sp


def fetch_liked_songs(sp):
    # Fetch the user's liked songs
    results = sp.current_user_saved_tracks(limit=50)
    liked_songs = []
    for idx, item in enumerate(results["items"]):
        track = item["track"]
        liked_songs.append(f"{track['name']} by {track['artists'][0]['name']}")
    return liked_songs


def fetch_playlists(sp):
    # Fetch all playlists of the user
    playlists = []
    results = sp.current_user_playlists(limit=50)
    playlists.extend(results["items"])

    # Handle pagination if the user has more than 50 playlists
    while results["next"]:
        results = sp.next(results)
        playlists.extend(results["items"])

    return playlists


def fetch_playlist_tracks(sp, playlist_id):
    # Fetch all tracks from a specific playlist.
    tracks = []
    results = sp.playlist_tracks(playlist_id, limit=100)
    tracks.extend(results["items"])

    # Handle pagination if there are more than 100 tracks
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])

    return tracks


def fetch_all_playlist_tracks(sp):
    # Fetch and return all tracks from all playlists
    playlists = fetch_playlists(sp)
    all_tracks = []
    for playlist in playlists:
        tracks = fetch_playlist_tracks(sp, playlist["id"])
        for item in tracks:
            track = item["track"]
            all_tracks.append(f"{track['name']} by {track['artists'][0]['name']}")
    return all_tracks


if __name__ == "__main__":
    # Load environment variables
    CLIENT_ID, CLIENT_SECRET = load_environment_variables()
    app.run(debug=True)
