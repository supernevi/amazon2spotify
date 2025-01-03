from itertools import islice
from typing import List

import config
import Progressbar
import spotipy
from spotipy import util
from AmazonMusicUtils import Playlist

scope = "playlist-modify-public"

token = util.prompt_for_user_token(username=config.spotify_user_id, scope=scope, client_id=config.spotify_client_id,
                                   client_secret=config.spotify_client_secret, redirect_uri='http://localhost:8080/')
sp = spotipy.Spotify(auth=token)

def import_playlist(playlist : Playlist):
    if len(playlist.name) == 0:
        print("no playlist name given")
        return
    
    if len(playlist.song_list) == 0:
        print("no songs given")
        return

    track_uris = get_track_uris(songs=playlist.song_list)

    print("creating playlist '{}'".format(playlist.name))
    playlist_id = playlist_create(playlist.name)
    if playlist_id is None:
        print("Failed to create spotifiy playlist with name '{}'".format(playlist.name))
    else:
        playlist_add_items(playlist_id, track_uris)
        print("{} of {} songs successfully imported".format(len(track_uris), len(playlist.song_list)))

def playlist_add_items(playlist_id : str, track_uris : List[str]):
    # max size of track URIs in spotify API is 100
    chunked_track_uris = chunk(track_uris, 100)

    for chunked_list in chunked_track_uris:
        sp.playlist_add_items(playlist_id = playlist_id, items = chunked_list)

def chunk(it, size):
    it = iter(it)
    return iter(lambda: tuple(islice(it, size)), ())

def get_track_uris(songs):
    track_uris = []

    print("starting determining songs in spotify")
    for index, current_song in enumerate(songs):
        Progressbar.show_progress(step=index+1, total_steps=len(songs), title="Determine songs in Spotify")

        search_string_spotify = current_song.Artist + " - " + current_song.Title
        results = sp.search(q=search_string_spotify, limit=1, type='track')

        if results['tracks']['total'] == 0:
            print("\nNo track found with '{}'".format(search_string_spotify))
            continue
        else:
            track_uris.append(results['tracks']['items'][0]['uri'])

    print("\n")
    return track_uris

def get_playlist_id(username, playlist_name):
    playlist_id = None
    playlists = sp.user_playlists(username)
    for playlist in playlists['items']:
        if playlist['name'] == playlist_name:
            playlist_id = playlist['id']
    return playlist_id

def playlist_create(playlist_name : str) -> str:
    response = sp.user_playlist_create(user=config.spotify_user_id, name=playlist_name)
    return response["id"]
