from textblob import TextBlob
import gensim.downloader as api
import numpy as np
from gensim.models import KeyedVectors

# Predefined mapping of keywords to valence and tempo ranges
combined_dict = {
    "happy": [0.7, 1.0, 120, 150],
    "sad": [0.0, 0.3, 60, 80],
    "angry": [0.4, 0.5, 130, 160],
    "nostalgic": [0.3, 0.6, 80, 100],
    "excited": [0.6, 1.0, 130, 160],
    "melancholic": [0.0, 0.3, 60, 80],
    "romantic": [0.6, 0.9, 70, 110],
    "uplifting": [0.7, 1.0, 120, 150],
    "relaxing": [0.3, 0.6, 60, 80],
    "chill": [0.3, 0.7, 60, 90],
    "vibes": [0.4, 0.8, 90, 120],
    "party": [0.7, 1.0, 120, 150],
    "workout": [0.7, 1.0, 130, 160],
    "study": [0.4, 0.6, 60, 80],
    "relax": [0.3, 0.6, 60, 80],
    "love": [0.7, 1.0, 70, 110],
    "summer": [0.7, 1.0, 110, 130],
    "road trip": [0.7, 1.0, 100, 130],
    "dance": [0.6, 1.0, 120, 140],
    "sleep": [0.0, 0.3, 50, 70],
    "focus": [0.4, 0.7, 80, 100],
    "morning": [0.4, 0.7, 80, 100],
    "evening": [0.3, 0.6, 60, 90],
    "acoustic": [0.4, 0.7, 60, 80],
    "indie": [0.4, 0.8, 80, 110],
    "pop": [0.6, 1.0, 110, 130],
    "rock": [0.5, 0.9, 110, 140],
    "hip-hop": [0.5, 0.8, 90, 110],
    "jazz": [0.3, 0.7, 70, 120],
    "classical": [0.2, 0.6, 50, 100],
    "edm": [0.6, 1.0, 120, 150],
    "throwback": [0.4, 0.7, 80, 110],
    "hits": [0.7, 1.0, 110, 140],
    "favorites": [0.7, 1.0, 100, 130],
    "discover": [0.4, 0.8, 80, 120],
    "new releases": [0.5, 0.9, 90, 130],
    "top 40": [0.6, 1.0, 110, 130],
    "best of": [0.7, 1.0, 110, 130],
    "calm": [0.2, 0.5, 50, 70],
    "mellow": [0.3, 0.6, 60, 80],
    "upbeat": [0.7, 1.0, 120, 140],
    "energetic": [0.7, 1.0, 130, 160],
    "motivational": [0.7, 1.0, 130, 160],
    "inspirational": [0.7, 1.0, 130, 160],
    "feel good": [0.7, 1.0, 120, 150],
    "happy hour": [0.7, 1.0, 120, 140],
    "party hits": [0.7, 1.0, 120, 150],
    "dance party": [0.7, 1.0, 120, 150],
    "workout mix": [0.7, 1.0, 130, 160],
    "study beats": [0.4, 0.7, 60, 80],
    "chillout": [0.3, 0.6, 60, 80],
    "lo-fi": [0.3, 0.6, 60, 80],
    "ambient": [0.2, 0.5, 50, 70],
    "instrumental": [0.3, 0.6, 60, 80],
    "piano": [0.3, 0.6, 60, 80],
    "guitar": [0.4, 0.7, 80, 110],
    "female vocals": [0.6, 0.9, 100, 130],
    "male vocals": [0.6, 0.9, 100, 130],
    "duets": [0.6, 0.8, 90, 110],
    "covers": [0.5, 0.8, 90, 120],
    "remixes": [0.5, 0.9, 120, 140],
    "mashups": [0.6, 0.9, 120, 140],
    "acoustic versions": [0.4, 0.7, 60, 80],
    "live performances": [0.5, 0.8, 90, 120],
    "unplugged": [0.4, 0.7, 60, 80],
    "road trip tunes": [0.7, 1.0, 100, 130],
    "summer vibes": [0.7, 1.0, 110, 130],
    "beach party": [0.7, 1.0, 120, 150],
    "poolside": [0.7, 1.0, 110, 130],
    "sunset": [0.7, 1.0, 80, 100],
    "sunrise": [0.7, 1.0, 80, 100],
    "rainy day": [0.0, 0.4, 60, 80],
    "snowy day": [0.0, 0.4, 60, 80],
    "autumn": [0.3, 0.6, 80, 100],
    "winter": [0.2, 0.5, 50, 70],
    "spring": [0.6, 0.9, 100, 130],
    "fall": [0.3, 0.7, 80, 110],
    "morning coffee": [0.4, 0.7, 80, 100],
    "evening chill": [0.3, 0.6, 60, 80],
    "night drive": [0.5, 0.8, 90, 110],
    "midnight": [0.3, 0.6, 60, 80],
    "late night": [0.4, 0.7, 80, 100],
    "early morning": [0.4, 0.7, 80, 100],
    "wake up": [0.6, 0.9, 100, 130],
    "get up": [0.6, 0.9, 100, 130],
    "rise and shine": [0.7, 1.0, 120, 150],
    "good morning": [0.7, 1.0, 120, 150],
    "good night": [0.2, 0.5, 50, 70],
    "bedtime": [0.0, 0.3, 40, 60],
    "dreamy": [0.4, 0.7, 60, 80],
    "sleepy": [0.0, 0.3, 40, 60],
    "meditation": [0.2, 0.5, 40, 60],
    "yoga": [0.3, 0.6, 60, 80],
    "spa": [0.3, 0.6, 60, 80],
    "zen": [0.3, 0.6, 60, 80],
    "mindfulness": [0.3, 0.6, 60, 80],
    "relaxation": [0.3, 0.6, 60, 80],
    "healing": [0.4, 0.7, 70, 90],
    "meditative": [0.3, 0.6, 50, 70],
    "therapeutic": [0.3, 0.6, 60, 80],
    "self-care": [0.3, 0.6, 60, 80],
    "sleep sounds": [0.0, 0.3, 40, 60],
    "white noise": [0.0, 0.3, 40, 60],
    "nature": [0.4, 0.6, 50, 70],
    "rain": [0.0, 0.3, 40, 60],
    "ocean": [0.4, 0.7, 60, 80],
    "forest": [0.4, 0.7, 60, 80],
    "birds": [0.3, 0.6, 50, 70],
    "wind": [0.3, 0.6, 50, 70],
    "thunderstorm": [0.0, 0.3, 40, 60],
    "crickets": [0.3, 0.6, 50, 70],
    "river": [0.4, 0.6, 60, 80],
    "water": [0.4, 0.6, 60, 80],
    "cicadas": [0.3, 0.6, 50, 70],
}


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


def main():
    # Load word2vec model
    word2vec = api.load("word2vec-google-news-300")

    # Ask user for input
    user_input = input("Please enter a mood or genre: ").lower()

    # Split the input into individual words
    input_words = user_input.split()

    # Initialize variables to aggregate the weighted ranges
    total_weighted_range = [0, 0, 0, 0]
    total_similarity = 0

    # Process each word in the input
    for word in input_words:
        weighted_range = calculate_weighted_range(word, combined_dict, word2vec)
        if weighted_range:
            total_similarity += 1
            total_weighted_range = [
                total_weighted_range[i] + weighted_range[i] for i in range(4)
            ]

    # Calculate the average weighted range if we processed any words
    if total_similarity > 0:
        average_weighted_range = [
            round(total_weighted_range[i] / total_similarity, 2) for i in range(4)
        ]
        valence_range = average_weighted_range[
            :2
        ]  # First two values: valence_min, valence_max
        tempo_range = average_weighted_range[
            2:
        ]  # Last two values: tempo_min, tempo_max
        print(
            f"Valence range for '{user_input}': {valence_range[0]} to {valence_range[1]}"
        )
        print(
            f"Tempo range for '{user_input}': {tempo_range[0]} to {tempo_range[1]} BPM"
        )
    else:
        print(f"No information found for '{user_input}'")


if __name__ == "__main__":
    main()
