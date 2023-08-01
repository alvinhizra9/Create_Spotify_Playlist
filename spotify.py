import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv

load_dotenv()

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET = os.getenv("SPOTIFY_SECRET")
REDIRECT_URL = os.getenv("REDIRECT_URL")
SPOTIFY_ID = os.getenv("SPOTIFY_ID")

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-public",
        redirect_uri=REDIRECT_URL,
        client_id=SPOTIFY_CLIENT_ID,
        client_secret=SPOTIFY_SECRET,
    )
)


def create_playlist(albums: list[str]) -> None:
    """
    Creates and returns a playlist with Spotify songs. It is used to check if
    there is a playlist with Spotify popularity > 70

    @param albums - List of albums to check

    @return Playlist of Spotify songs that are too high to be played in
    Spotify or None if
    """
    name = input("Enter playlist name: ")
    description = input("Enter playlist description: ")
    my_playlist = sp.user_playlist_create(
        user=SPOTIFY_ID, name=name, public=True, description=description
    )
    playlist = []

    # Add tracks to the playlist.
    for index, album in enumerate(albums[::-1]):
        album = sp.search(q=album, type="album")
        offset = -1
        tracks_number = 50

        while tracks_number >= 50:
            offset += 1
            album_tracks = sp.album_tracks(
                album_id=album["albums"]["items"][0]["id"], offset=offset
            )
            for track in album_tracks["items"]:
                song = sp.track(track_id=track["id"])
                # Add track id to playlist if popularity is more than 70
                if song["popularity"] > 70:
                    playlist.append(track["id"])

            tracks_number = album["albums"]["items"][0]["total_tracks"]

            # Add playlist if it is more than 50 or reach last album.
            if len(playlist) > 50 or index == len(albums) - 1:
                sp.playlist_add_items(
                    playlist_id=my_playlist["id"],
                    position=0,
                    items=playlist,
                )
                playlist = []
