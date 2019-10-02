from main import Spotify

CLIENT_ID = ""
CLIENT_SECRET = ""

spotify = Spotify(CLIENT_ID, CLIENT_SECRET)
artist_id = spotify.get_artist_id("The Weeknd")
album_starboy = spotify.get_albums_from_id(artist_id, True)[2]
tracks = spotify.get_tracks_of_album(album_starboy["id"])

for track in tracks:
    danceability = spotify.get_track_audio_features(track["id"])["danceability"]
    print(f"{track['name']}: {danceability}")