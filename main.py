import requests
import json
from requests.auth import HTTPBasicAuth
from artist import Artist

CLIENT_ID = ""
CLIENT_SECRET = ""


class Spotify:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = self._get_access_token()

    def __repr__(self):
        return "Spotify API Wrapper"

    def _get_access_token(self):
        token_url = 'https://accounts.spotify.com/api/token'
        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        data = {'grant_type': 'client_credentials'}
        request_token = requests.post(token_url, data, auth=auth)
        if request_token:
            if request_token.ok:
                return json.loads(request_token.text)['access_token']
        print(f"Token Access Failed.")
        exit()

    def _make_request(self, url, parameters=None):
        headers = {'Authorization': 'Bearer ' + self.token}
        data = requests.get(url, headers=headers, params=parameters)
        if data.ok:
            return data
        print(f"Request failed to {url}. Error type: {data.status_code}")
        return None

    def get_artist_object(self, artist_id):
        artist_info = self.get_artist_info_from_id(artist_id)
        artist_albums = self.get_albums_from_id(artist_id)
        if artist_info and artist_albums:
            artist = Artist(artist_info["name"], artist_id, artist_info["followers"], artist_info["genres"],
                            artist_info["popularity"], artist_info["image_link"], artist_albums)
            return artist
        print("Unable to create artist object.")
        return None

    def get_artist_id(self, search_query, limit=1):
        artist_id_data = self._make_request("https://api.spotify.com/v1/search",
                                            {"query": search_query, "type": "artist", "limit": limit})
        if artist_id_data:
            artist_id_json = artist_id_data.json()
            if artist_id_json["artists"]["total"] == 0:
                print("No artist was found.")
                return None
            return artist_id_json["artists"]["items"][0]["id"]
        print("Request failed. No artist id was obtained.")
        return None

    def get_artist_info_from_name(self, artist_name):
        artist_id = self.get_artist_id(artist_name)
        if artist_id:
            return self.get_artist_info_from_id(artist_id)
        return None

    def get_artist_info_from_id(self, artist_id):
        artist_info_data = self._make_request(f"https://api.spotify.com/v1/artists/{artist_id}")
        if artist_info_data:
            artist_info_json = artist_info_data.json()
            followers = artist_info_json["followers"]["total"]
            genres = artist_info_json["genres"]
            image_link = artist_info_json["images"][0]["url"]
            popularity = artist_info_json["popularity"]
            name = artist_info_json["name"]
            return {"name": name, "genres": genres, "image_link": image_link,
                    "popularity": popularity, "followers": followers}
        print("Request failed. No artist information was obtained.")
        return None

    def get_albums_from_id(self, artist_id, get_just_id=False):
        artist_albums_data = self._make_request(f"https://api.spotify.com/v1/artists/{artist_id}/albums")
        if artist_albums_data:
            artist_albums = []
            for album in artist_albums_data.json()["items"]:
                album_id = album["id"]
                if get_just_id:
                    artist_albums.append(album_id)
                else:
                    artist_name = album["artists"][0]["name"]
                    album_name = album["name"]
                    release_date = album["release_date"]
                    total_tracks = album["total_tracks"]
                    album_cover = album["images"][0]["url"]
                    artist_albums.append({"artist": artist_name, "id": album_id, "name": album_name,
                                          "release_date": release_date, "total_tracks": total_tracks,
                                          "cover": album_cover})
            return artist_albums
        print("Request failed. No albums were obtained.")
        return None

    def get_albums_from_name(self, artist_name, get_just_id=False):
        artist_id = self.get_artist_id(artist_name)
        if artist_id:
            return self.get_albums_from_id(artist_id, get_just_id)
        return None

    def get_artist_top_tracks_from_id(self, artist_id, get_just_id=False):
        top_tracks_data = self._make_request(f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks",
                                             {"market": "US"})
        if top_tracks_data:
            artist_tracks = []
            for track in top_tracks_data.json()["tracks"]:
                track_id = track["id"]
                if get_just_id:
                    artist_tracks.append(track_id)
                else:
                    track_name = track["name"]
                    album_name = track["album"]["name"]
                    is_explicit = track["explicit"]
                    duration = track["duration_ms"]
                    track_artists = []
                    for artist in track["artists"]:
                        track_artists.append({"name": artist["name"], "id": artist["id"]})
                    artist_tracks.append({"id": track_id, "track_name": track_name, "artists": track_artists,
                                          "album_name": album_name, "is_explicit": is_explicit, "duration": duration})
            return artist_tracks
        return None

    def get_artist_top_tracks_from_name(self, artist_name):
        artist_id = self.get_artist_id(artist_name)
        if artist_id:
            return self.get_artist_top_tracks_from_id(artist_id)
        return None


spotify = Spotify(CLIENT_ID, CLIENT_SECRET)
