import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
from flask import Flask, request, render_template

app = Flask(__name__)


# Default page
@app.route("/")
def home():
    return render_template("index.html")


# Collect user's saved playlists from Spotify
@app.route("/fetch-playlists", methods=["POST"])
def fetch_playlists_route():
    fetched_playlists = fetch_playlists(sp)

    return render_template("index.html", playlists=fetched_playlists)


# Retrieve selected playlists from HTML, then collect songs from each playlist from Spotify
@app.route("/submit-playlists", methods=["POST"])
def submit_playlists():
    # Retrieve selected playlists from the form
    selected_playlists = request.form.getlist("selected_playlists")

    # Set to track unique song IDs
    unique_song_ids = set()
    all_selected_songs = []

    # Fetch all playlists once to avoid redundant fetching
    playlists = fetch_playlists(sp)

    for playlist_id in selected_playlists:
        if playlist_id == "liked_songs":
            # Fetch liked songs if "Liked Songs" was selected
            liked_songs = fetch_liked_songs(sp)
            for song in liked_songs:
                if song["id"] not in unique_song_ids:
                    unique_song_ids.add(song["id"])
                    all_selected_songs.append(
                        f"{song['name']} by {song['artists'][0]['name']}"
                    )
                else:
                    print("Doubled song: ", song)
        else:
            # Fetch songs from a specific playlist
            playlist = next((p for p in playlists if p["id"] == playlist_id), None)
            if playlist:
                playlist_tracks = fetch_playlist_tracks(sp, playlist["id"])
                for item in playlist_tracks:
                    track = item["track"]
                    # Check if track ID has already been collected - if so, this is a double
                    if track["id"] not in unique_song_ids:
                        unique_song_ids.add(track["id"])
                        all_selected_songs.append(
                            f"{track['name']} by {track['artists'][0]['name']}"
                        )
                    else:
                        print("Doubled song: ", track["name"])

    # print("Fetched songs from selected playlists:", all_selected_songs)

    # Return the updated page with the songs
    return render_template(
        "index.html",
        playlists=playlists,
        selected=selected_playlists,
        songs=all_selected_songs,
    )


@app.route("/fetch-songs", methods=["POST"])
def submit():
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

    # Get the directory where the app.py script is located
    app_directory = os.path.dirname(os.path.abspath(__file__))
    CACHE_PATH = os.path.join(app_directory, ".spotify_cache")
    print(CACHE_PATH)

    sp = spotipy.Spotify(
        auth_manager=SpotifyOAuth(
            client_id=client_id,
            client_secret=client_secret,
            redirect_uri=REDIRECT_URI,
            scope=SCOPE,
            cache_path=CACHE_PATH,
        )
    )

    return sp


def fetch_liked_songs(sp):
    # Fetch the user's liked songs
    results = sp.current_user_saved_tracks(limit=50)
    liked_songs = []
    for item in results["items"]:
        track = item["track"]
        liked_songs.append(
            {"id": track["id"], "name": track["name"], "artists": track["artists"]}
        )
    return liked_songs


def fetch_playlists(sp):
    playlists = []
    results = sp.current_user_playlists(limit=50)
    playlists.extend(results["items"])

    # Handle pagination for more than 50 playlists
    while results["next"]:
        results = sp.next(results)
        playlists.extend(results["items"])

    # Include "Liked Songs" as a special case with a unique identifier
    playlist_data = [{"name": "Liked Songs", "image_url": None, "id": "liked_songs"}]

    for playlist in playlists:
        image_url = playlist["images"][0]["url"] if playlist["images"] else None
        playlist_data.append(
            {"name": playlist["name"], "image_url": image_url, "id": playlist["id"]}
        )

    return playlist_data


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
            all_tracks.append(
                {"id": track["id"], "name": track["name"], "artists": track["artists"]}
            )
    return all_tracks


if __name__ == "__main__":
    # Authenticate with Spotify
    CLIENT_ID, CLIENT_SECRET = load_environment_variables()
    sp = authenticate_spotify(CLIENT_ID, CLIENT_SECRET)
    app.run(debug=True)
