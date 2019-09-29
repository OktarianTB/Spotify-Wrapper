class Artist:
    def __init__(self, name, artist_id, followers, genres, popularity, image, albums):
        self.name = name
        self.artist_id = artist_id
        self.followers = followers
        self.genres = genres
        self.popularity = popularity
        self.image = image
        self.albums = albums

    def __repr__(self):
        return f"Artist object for {self.name}"

    def get_data(self):
        return {"name": self.name, "genres": self.genres, "image_link": self.image,
                "popularity": self.popularity, "followers": self.followers, "albums": self.albums}
