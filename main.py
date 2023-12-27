from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

CLIENT_ID = os.environ["CLIENTID"]
CLIENT_SECRET_KEY = os.environ["CLIENTKEY"]
REDIRECT_URI = "https://example.com"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri=REDIRECT_URI,
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET_KEY,
        show_dialog=True,
    )
)

user_id = sp.current_user()["id"]

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get("https://www.billboard.com/charts/hot-100/" + date)

year = date.split("-")[0]
soup = BeautifulSoup(response.text, 'html.parser')
song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

uri_list = []

for song in song_names:
    result = sp.search(q=f"track:{song}, year:{year}", type="track")

    try:
        uri = result["tracks"]["items"][0]["uri"]
        uri_list.append(uri)

    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False,
                                   collaborative=False, description=None)

sp.playlist_add_items(playlist_id=playlist["id"], items=uri_list)
