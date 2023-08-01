from rolling_stone import get_albums
from spotify import create_playlist

if __name__ == "__main__":
    albums = get_albums()
    create_playlist(albums)
