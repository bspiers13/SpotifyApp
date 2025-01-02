# Warning: Playlist Generator no longer works due to the removal of audio_features from Spotify's API

## This project will include other Spotify tools, however they are still under development

---

# Playlist Generator using Sentiment Analysis

This project allows users to generate Spotify playlists based on a specific theme, using sentiment analysis to select songs that match the desired mood.
The app integrates with Spotify to fetch saved songs and playlists including the audio_features of each song, analyze the theme provided by the user, and create a new playlist on the user's Spotify account based on the analysis.

---

## Features

- Fetches user's saved songs and playlists from Spotify.
- Analyzes a user-provided theme using sentiment analysis.
- Filters songs based on sentiment to match the theme.
- Creates and adds the newly generated playlist to the user's Spotify account.

---

## Requirements

- Python 3.11
- `spotipy` library
- `textblob` library
- `gensim` library
- `flask` web framework
- Spotify Developer account for API credentials

---

## Setup

### 1. Clone the repository

### 2. Get API credentials from Spotify Dev account, and store them as SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET in .env within the directory

### 3. Run main.py

### 4. Open 127.0.0.1:5000 in your browser
