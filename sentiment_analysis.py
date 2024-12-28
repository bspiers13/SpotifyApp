from textblob import TextBlob
import gensim.downloader as api
import numpy as np
from gensim.models import KeyedVectors
import json
import os
import spotipy


def set_model():
    print("Loading model...")
    word2vec = api.load("word2vec-google-news-300")
    return word2vec


def analyse_input(input, model):
    # Split the input into individual words
    input_words = input.split()

    # Initialize variables to aggregate the weighted ranges
    total_weighted_range = [0, 0, 0, 0]
    total_similarity = 0

    # Process each word in the input
    for word in input_words:
        weighted_range = calculate_weighted_range(word, load_mood_map(), model)
        if weighted_range:
            total_similarity += 1
            total_weighted_range = [
                total_weighted_range[i] + weighted_range[i] for i in range(4)
            ]

    # Calculate the average weighted range
    if total_similarity > 0:
        average_weighted_range = [
            round(total_weighted_range[i] / total_similarity, 2) for i in range(4)
        ]
        # First two values: valence_min, valence_max
        valence_range = average_weighted_range[:2]
        # Last two values: tempo_min, tempo_max
        tempo_range = average_weighted_range[2:]
        print(f"Valence range for '{input}': {valence_range[0]} to {valence_range[1]}")
        print(f"Tempo range for '{input}': {tempo_range[0]} to {tempo_range[1]} BPM")
    else:
        print(f"No information found for '{input}'")

    return average_weighted_range


def load_mood_map():
    app_directory = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(app_directory, "mood_map.json")

    if not os.path.exists(json_path):
        raise FileNotFoundError(f"The file {json_path} does not exist.")

    with open(json_path, "r") as file:
        return json.load(file)


# Function to calculate weighted ranges based on similarity
def calculate_weighted_range(input_word, word_dict, model):
    total_similarity = 0
    weighted_range = [0, 0, 0, 0]  # [valence_min, valence_max, tempo_min, tempo_max]

    for dict_word, value_range in word_dict.items():
        try:
            similarity = model.similarity(input_word, dict_word)
            weighted_range[0] += similarity * value_range[0]  # valence_min
            weighted_range[1] += similarity * value_range[1]  # valence_max
            weighted_range[2] += similarity * value_range[2]  # tempo_min
            weighted_range[3] += similarity * value_range[3]  # tempo_max
            total_similarity += similarity
        except KeyError:
            # Skip words not in the model vocabulary
            continue

    if total_similarity > 0:
        weighted_range[0] /= total_similarity
        weighted_range[1] /= total_similarity
        weighted_range[2] /= total_similarity
        weighted_range[3] /= total_similarity
        return [
            round(weighted_range[0], 2),
            round(weighted_range[1], 2),
            round(weighted_range[2], 2),
            round(weighted_range[3], 2),
        ]
    else:
        return None


def get_audio_features(sp, track):
    audio_features = None
    try:
        # Get audio features
        audio_features = sp.audio_features(track["id"])
    except spotipy.exceptions.SpotifyException as e:
        print(f"Error fetching audio features for {track['name']}: {e}")

    return audio_features


def audio_features_fit_theme(track, audio_features, theme_analysis, filtered_songs):
    # Call analyse_input function and get the analysis result
    # theme_analysis = analyse_input(theme)

    if audio_features:
        # print(f"Audio features: {audio_features[0]}")
        if (
            theme_analysis[0] <= audio_features["valence"] <= theme_analysis[1]
            and theme_analysis[2] <= audio_features["tempo"] <= theme_analysis[3]
        ):
            filtered_songs.append(f"{track['name']} by {track['artists'][0]['name']}")
            print("Filtering: ", track["name"])
            print(audio_features["valence"])
            print(audio_features["tempo"])

            return True
    else:
        print("No audio features found.")

        return False


def filter_song(sp, track, theme_analysis, filtered_songs):
    # Get audio features of the current song, then check if they fit the theme
    audio_features = get_audio_features(sp, track)
    if audio_features_fit_theme(track, audio_features, theme_analysis, filtered_songs):
        filtered_songs.append(track)  # If so, add to filtered songs list


def demo():
    print("Loading word2vec model...")

    word2vec = api.load("word2vec-google-news-300")
    # analyse_input(user_input, word2vec)

    dummy_features = {
        "2takcwOaAZWiXQijPHIx7B": {"tempo": 120, "valence": 0.8},
        "3takcwOaAZWiXQijPHIx7B": {"tempo": 70, "valence": -0.5},
        "4takcwOaAZWiXQijPHIx7B": {"tempo": 140, "valence": 0.6},
        "5takcwOaAZWiXQijPHIx7B": {"tempo": 60, "valence": 0.2},
        "6takcwOaAZWiXQijPHIx7B": {"tempo": 128, "valence": 0.9},
        "7takcwOaAZWiXQijPHIx7B": {"tempo": 100, "valence": 0.5},
    }

    dummy_tracks = [
        {
            "id": "2takcwOaAZWiXQijPHIx7B",
            "name": "Track 1",
            "artists": [{"name": "Artist 1"}],
        },
        {
            "id": "3takcwOaAZWiXQijPHIx7B",
            "name": "Track 2",
            "artists": [{"name": "Artist 2"}],
        },
        {
            "id": "4takcwOaAZWiXQijPHIx7B",
            "name": "Track 3",
            "artists": [{"name": "Artist 3"}],
        },
        {
            "id": "5takcwOaAZWiXQijPHIx7B",
            "name": "Track 4",
            "artists": [{"name": "Artist 4"}],
        },
        {
            "id": "6takcwOaAZWiXQijPHIx7B",
            "name": "Track 5",
            "artists": [{"name": "Artist 5"}],
        },
        {
            "id": "7takcwOaAZWiXQijPHIx7B",
            "name": "Track 6",
            "artists": [{"name": "Artist 6"}],
        },
    ]

    print("Demo songs:")
    print(dummy_tracks)

    print("Dummy audio features for each song:")
    print(dummy_features)

    print("Demo theme: 'happy'")

    theme_analysis = analyse_input("happy", word2vec)
    filtered_songs = []
    for track in dummy_tracks:
        track_id = track["id"]
        if track_id in dummy_features:
            audio_features_fit_theme(
                track, dummy_features[track_id], theme_analysis, filtered_songs
            )

    print("List of songs that fit the theme:")
    print(filtered_songs)


def main():
    # Ask user for input
    # user_input = input("Please enter a mood or genre: ").lower()
    demo()


if __name__ == "__main__":
    main()
