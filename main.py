import requests
import json
from requests.auth import HTTPBasicAuth

CLIENT_ID = ""
CLIENT_SECRET = ""


class Spotify:
    def __init__(self, client_id, client_secret):
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = self.access_token()

    def __repr__(self):
        return "Spotify API Wrapper"

    def access_token(self):
        token_url = 'https://accounts.spotify.com/api/token'
        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        data = {'grant_type': 'client_credentials'}
        request_token = requests.post(token_url, data, auth=auth)
        if request_token:
            if request_token.ok:
                return json.loads(request_token.text)['access_token']
        print(f"Token Access Failed.")
        exit()

    def make_request(self, url, parameters=None):
        headers = {'Authorization': 'Bearer ' + self.token}
        data = requests.get(url, headers=headers, params=parameters)
        if data.ok:
            return data
        print(f"Request failed to {url}. Error type: {data.status_code}")
        return None

    def get_artist_id(self, search_query, limit=1):
        artist_id_data = self.make_request("https://api.spotify.com/v1/search",
                                      {"query": search_query, "type": "artist", "limit": limit})
        if artist_id_data:
            artist_id_json = artist_id_data.json()
            if artist_id_json["artists"]["total"] == 0:
                print("No artist was found.")
                return None
            return artist_id_json["artists"]["items"][0]["id"]
        print("Request failed. No artist id was obtained.")
        return None

    def get_artist_info(self, artist_name):
        artist_id = self.get_artist_id(artist_name)
        if artist_id:
            artist_info_data = self.make_request(f"https://api.spotify.com/v1/artists/{artist_id}")
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


spotify = Spotify(CLIENT_ID, CLIENT_SECRET)

