import sys
from textblob import TextBlob
import gensim.downloader as api
import numpy as np
from gensim.models import KeyedVectors

# Predefined mapping of keywords to valence ranges
valence_dict = {
    "happy": [0.7, 1.0],
    "sad": [0.0, 0.3],
    "angry": [0.4, 0.5],
    "nostalgic": [0.3, 0.6],
    "excited": [0.6, 1.0],
    "melancholic": [0.0, 0.3],
    "romantic": [0.6, 0.9],
    "uplifting": [0.7, 1.0],
    "relaxing": [0.3, 0.6],
    "chill": [0.3, 0.7],
    "vibes": [0.4, 0.8],
    "party": [0.7, 1.0],
    "workout": [0.7, 1.0],
    "study": [0.4, 0.6],
    "relax": [0.3, 0.6],
    "happy": [0.7, 1.0],
    "sad": [0.0, 0.3],
    "love": [0.7, 1.0],
    "summer": [0.7, 1.0],
    "road trip": [0.7, 1.0],
    "dance": [0.6, 1.0],
    "sleep": [0.0, 0.3],
    "focus": [0.4, 0.7],
    "morning": [0.4, 0.7],
    "evening": [0.3, 0.6],
    "acoustic": [0.4, 0.7],
    "indie": [0.4, 0.8],
    "pop": [0.6, 1.0],
    "rock": [0.5, 0.9],
    "hip-hop": [0.5, 0.8],
    "jazz": [0.3, 0.7],
    "classical": [0.2, 0.6],
    "edm": [0.6, 1.0],
    "throwback": [0.4, 0.7],
    "hits": [0.7, 1.0],
    "favorites": [0.7, 1.0],
    "discover": [0.4, 0.8],
    "new releases": [0.5, 0.9],
    "top 40": [0.6, 1.0],
    "best of": [0.7, 1.0],
    "relaxing": [0.3, 0.6],
    "calm": [0.2, 0.5],
    "mellow": [0.3, 0.6],
    "upbeat": [0.7, 1.0],
    "energetic": [0.7, 1.0],
    "motivational": [0.7, 1.0],
    "inspirational": [0.7, 1.0],
    "feel good": [0.7, 1.0],
    "happy hour": [0.7, 1.0],
    "party hits": [0.7, 1.0],
    "dance party": [0.7, 1.0],
    "workout mix": [0.7, 1.0],
    "study beats": [0.4, 0.7],
    "chillout": [0.3, 0.6],
    "lo-fi": [0.3, 0.6],
    "ambient": [0.2, 0.5],
    "instrumental": [0.3, 0.6],
    "piano": [0.3, 0.6],
    "guitar": [0.4, 0.7],
    "female vocals": [0.6, 0.9],
    "male vocals": [0.6, 0.9],
    "duets": [0.6, 0.8],
    "covers": [0.5, 0.8],
    "remixes": [0.5, 0.9],
    "mashups": [0.6, 0.9],
    "acoustic versions": [0.4, 0.7],
    "live performances": [0.5, 0.8],
    "unplugged": [0.4, 0.7],
    "road trip tunes": [0.7, 1.0],
    "summer vibes": [0.7, 1.0],
    "beach party": [0.7, 1.0],
    "poolside": [0.7, 1.0],
    "sunset": [0.7, 1.0],
    "sunrise": [0.7, 1.0],
    "rainy day": [0.0, 0.4],
    "snowy day": [0.0, 0.4],
    "autumn": [0.3, 0.6],
    "winter": [0.2, 0.5],
    "spring": [0.6, 0.9],
    "fall": [0.3, 0.7],
    "morning coffee": [0.4, 0.7],
    "evening chill": [0.3, 0.6],
    "night drive": [0.5, 0.8],
    "midnight": [0.3, 0.6],
    "late night": [0.4, 0.7],
    "early morning": [0.4, 0.7],
    "wake up": [0.6, 0.9],
    "get up": [0.6, 0.9],
    "rise and shine": [0.7, 1.0],
    "good morning": [0.7, 1.0],
    "good night": [0.2, 0.5],
    "bedtime": [0.0, 0.3],
    "dreamy": [0.4, 0.7],
    "sleepy": [0.0, 0.3],
    "meditation": [0.2, 0.5],
    "yoga": [0.3, 0.6],
    "spa": [0.3, 0.6],
    "zen": [0.3, 0.6],
    "mindfulness": [0.3, 0.6],
    "relaxation": [0.3, 0.6],
    "stress relief": [0.3, 0.6],
    "calm down": [0.2, 0.5],
    "unwind": [0.2, 0.5],
    "decompress": [0.2, 0.5],
    "chill beats": [0.3, 0.6],
    "smooth": [0.4, 0.7],
    "soulful": [0.5, 0.8],
    "groovy": [0.6, 0.9],
    "funky": [0.6, 0.9],
}

tempo_dict = {
    "happy": [120, 150],
    "sad": [60, 80],
    "angry": [130, 160],
    "nostalgic": [80, 100],
    "excited": [130, 160],
    "melancholic": [60, 80],
    "romantic": [70, 110],
    "uplifting": [120, 150],
    "relaxing": [60, 80],
    "chill": [60, 90],
    "vibes": [90, 120],
    "party": [120, 150],
    "workout": [130, 160],
    "study": [60, 80],
    "relax": [60, 80],
    "love": [70, 110],
    "summer": [110, 130],
    "road trip": [100, 130],
    "dance": [120, 140],
    "sleep": [50, 70],
    "focus": [80, 100],
    "morning": [80, 100],
    "evening": [60, 90],
    "acoustic": [60, 80],
    "indie": [80, 110],
    "pop": [110, 130],
    "rock": [110, 140],
    "hip-hop": [90, 110],
    "jazz": [70, 120],
    "classical": [50, 100],
    "edm": [120, 150],
    "throwback": [80, 110],
    "hits": [110, 140],
    "favorites": [100, 130],
    "discover": [80, 120],
    "new releases": [90, 130],
    "top 40": [110, 130],
    "best of": [110, 130],
    "calm": [50, 70],
    "mellow": [60, 80],
    "upbeat": [120, 140],
    "energetic": [130, 160],
    "motivational": [130, 160],
    "inspirational": [130, 160],
    "feel good": [120, 150],
    "happy hour": [120, 140],
    "party hits": [120, 150],
    "dance party": [120, 150],
    "workout mix": [130, 160],
    "study beats": [60, 80],
    "chillout": [60, 80],
    "lo-fi": [60, 80],
    "ambient": [50, 70],
    "instrumental": [60, 80],
    "piano": [60, 80],
    "guitar": [80, 110],
    "female vocals": [100, 130],
    "male vocals": [100, 130],
    "duets": [90, 110],
    "covers": [90, 120],
    "remixes": [120, 140],
    "mashups": [120, 140],
    "acoustic versions": [60, 80],
    "live performances": [90, 120],
    "unplugged": [60, 80],
    "road trip tunes": [100, 130],
    "summer vibes": [110, 130],
    "beach party": [120, 150],
    "poolside": [110, 130],
    "sunset": [80, 100],
    "sunrise": [80, 100],
    "rainy day": [60, 80],
    "snowy day": [60, 80],
    "autumn": [80, 100],
    "winter": [50, 70],
    "spring": [100, 130],
    "fall": [80, 110],
    "morning coffee": [80, 100],
    "evening chill": [60, 80],
    "night drive": [90, 110],
    "midnight": [60, 80],
    "late night": [80, 100],
    "early morning": [80, 100],
    "wake up": [100, 130],
    "get up": [100, 130],
    "rise and shine": [120, 150],
    "good morning": [120, 150],
    "good night": [50, 70],
    "bedtime": [40, 60],
    "dreamy": [60, 80],
    "sleepy": [40, 60],
    "meditation": [40, 60],
    "yoga": [60, 80],
    "spa": [60, 80],
    "zen": [60, 80],
    "mindfulness": [60, 80],
    "relaxation": [60, 80],
    "stress relief": [60, 80],
    "calm down": [40, 60],
    "unwind": [40, 60],
    "decompress": [40, 60],
    "chill beats": [60, 80],
    "smooth": [80, 100],
    "soulful": [90, 120],
    "groovy": [100, 130],
    "funky": [100, 130],
}


# Function to calculate weighted ranges based on similarity
def calculate_weighted_range(input_word, word_dict, model):
    total_similarity = 0
    weighted_range = [0, 0]

    for dict_word, value_range in word_dict.items():
        try:
            similarity = model.similarity(input_word, dict_word)
            weighted_range[0] += similarity * value_range[0]
            weighted_range[1] += similarity * value_range[1]
            total_similarity += similarity
        except KeyError:
            # Skip words not in the model vocabulary
            continue

    if total_similarity > 0:
        weighted_range[0] /= total_similarity
        weighted_range[1] /= total_similarity
        return [round(weighted_range[0], 2), round(weighted_range[1], 2)]
    else:
        return None


def get_valence_from_input(user_input):
    """
    This function maps user input to a valence range using the predefined valence_dict.
    It checks if any of the keywords in the valence_dict are in the user input and
    returns the corresponding valence range.

    Args:
    user_input (str): The input string from the user.

    Returns:
    tuple: A tuple representing the valence range (min, max), or None if no keyword is found.
    """
    # Convert input to lowercase to make it case-insensitive
    user_input = user_input.lower()

    # Iterate through the valence_dict to find any matching keywords in the user input
    for keyword, valence_range in valence_dict.items():
        if keyword in user_input:
            return valence_range

    # If no keyword was found, return None
    return None


def get_tempo_from_input(user_input):
    """
    This function maps user input to a tempo range using the predefined tempo_dict.
    It checks if any of the keywords in the tempo_dict are in the user input and
    returns the corresponding tempo range.

    Args:
    user_input (str): The input string from the user.

    Returns:
    tuple: A tuple representing the tempo range (min_bpm, max_bpm), or None if no keyword is found.
    """
    # Convert input to lowercase to make it case-insensitive
    user_input = user_input.lower()

    # Iterate through the tempo_dict to find any matching keywords in the user input
    for keyword, tempo_range in tempo_dict.items():
        if keyword in user_input:
            return tempo_range

    # If no keyword was found, return None
    return None


# Function to calculate weighted valence
def get_weighted_valence(input_word, valence_dict, model):
    # Store similarities and valence contributions
    similarities = []
    weighted_valences = []

    for word, valence in valence_dict.items():
        try:
            similarity = model.similarity(input_word, word)
            if similarity > 0:  # Ignore negative or zero similarities
                similarities.append(similarity)
                weighted_valences.append(np.array(valence) * similarity)
        except KeyError:
            # Skip words not in word2vec vocabulary
            continue

    if not similarities:
        print(f"No similar words found for '{input_word}'.")
        return None

    # Normalize similarities to sum to 1
    similarities = np.array(similarities)
    normalized_weights = similarities / similarities.sum()

    # Compute weighted average of valences
    weighted_average_valence = sum(
        w * v for w, v in zip(normalized_weights, weighted_valences)
    )

    print(f"Input '{input_word}' assigned weighted valence {weighted_average_valence}.")
    return weighted_average_valence


def main():
    # Load the pre-trained word2vec model
    word2vec = api.load("word2vec-google-news-300")

    # Ask user for input
    user_input = input("Please enter a mood or genre: ")

    # Get valence and tempo ranges based on the input
    valence_range = calculate_weighted_range(user_input, valence_dict, word2vec)
    tempo_range = calculate_weighted_range(user_input, tempo_dict, word2vec)

    # Print results
    if valence_range:
        print(
            f"Valence range for '{user_input}': {valence_range[0]} to {valence_range[1]}"
        )
    else:
        print(f"No valence information found for '{user_input}'")

    if tempo_range:
        print(
            f"Tempo range for '{user_input}': {tempo_range[0]} to {tempo_range[1]} BPM"
        )
    else:
        print(f"No tempo information found for '{user_input}'")


if __name__ == "__main__":
    main()
