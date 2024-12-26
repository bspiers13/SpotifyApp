from textblob import TextBlob
import gensim.downloader as api
import numpy as np
from gensim.models import KeyedVectors
import json
import os


def load_combined_dict():
    app_directory = os.path.dirname(os.path.abspath(__file__))
    json_path = os.path.join(app_directory, "combined_dict.json")

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


def analyse_input(input):
    # Split the input into individual words
    input_words = input.split()

    print("Loading word2vec model...")

    # Load word2vec model
    word2vec = api.load("word2vec-google-news-300")

    # Initialize variables to aggregate the weighted ranges
    total_weighted_range = [0, 0, 0, 0]
    total_similarity = 0

    # Process each word in the input
    for word in input_words:
        weighted_range = calculate_weighted_range(word, load_combined_dict(), word2vec)
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


def main():
    # Ask user for input
    user_input = input("Please enter a mood or genre: ").lower()

    analyse_input(user_input)


if __name__ == "__main__":
    main()
