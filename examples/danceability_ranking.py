from simple_spotify.main import Spotify

CLIENT_ID = "YOUR ID"
CLIENT_SECRET = "YOUR CLIENT SECRET"

spotify = Spotify(CLIENT_ID, CLIENT_SECRET)
artist_id = spotify.get_artist_id("The Weeknd")
top_tracks = spotify.get_artist_top_tracks_from_id(artist_id, True)
tracks_danceability = []

for track in top_tracks:
    features = spotify.get_track_audio_features(track["id"])
    danceability = features["danceability"]
    tracks_danceability.append((track["name"], danceability))

ranking = sorted(tracks_danceability, key=lambda tup: tup[1], reverse=True)
print(ranking)