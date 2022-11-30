# https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-features
# https://developer.spotify.com/documentation/web-api/reference/#/operations/get-audio-analysis

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

sp = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(
        client_id="ca4037574604402aa16cc9ead70aa2e3",
        client_secret="9b7ab94755874ebc8179da11926f68c3"
    )
)

name = input("Enter name of song: ")
results = sp.search(name, limit=5)

for i, track in enumerate(results["tracks"]["items"]):
    print(f"[{i}] {track['name']} by {track['artists'][0]['name']}")

id = int(input("Enter number: "))
id = results["tracks"]["items"][id]["id"]

results = sp.audio_features(id)
for feature in ["danceability", "energy", "key", "loudness", "mode", \
    "speechiness", "acousticness", "instrumentalness", "liveness", "valence", \
    "tempo"]:
    print(f"\t{feature}= {results[0][feature]}")