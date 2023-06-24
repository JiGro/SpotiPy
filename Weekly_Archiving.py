#Spotify's Developer Page: https://developer.spotify.com/documentation/web-api/quick-start/
#Spotify's Developer Console: https://developer.spotify.com/console/

import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

def get_playlist_tracks(username,playlist_id):
    results = spotify_client.user_playlist_tracks(username,
                                                  playlist_id)
    tracks = results['items']
    while results['next']:
        results = spotify_client.next(results)
        tracks.extend(results['items'])
    return tracks

def establish_spotify_api_connection():
    print("*** Step 1) Connect to api ***")
    CLIENT_ID = os.environ.get("CLIENT_ID")
    CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
    scope = "user-read-private playlist-read-private user-library-read user-library-modify user-top-read playlist-modify-public playlist-modify-private"

    spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                               client_id=CLIENT_ID,
                                                               client_secret=CLIENT_SECRET,
                                                               redirect_uri='http://localhost:8888',
                                                               cache_path='cache.txt'))
    return spotify_client


spotify_client = establish_spotify_api_connection()

# Necessary variables
username = spotify_client.current_user()['id']
archive_playlist_name = "The Ultimate Discover Weekly Playlist"
archive_playlist_description = "A playlist containing past discover weekly playlists"
archive_id = None


print("*** Step 2) Extract Discover Weekly details and identify track ids ***")
# Since hidden, extract discover weekly id manually from Spotify webplayer
discover_weekly_id = "37i9dQZEVXcOrp8OvX9U5e"
playlists = spotify_client.current_user_playlists()["items"]
discover_weekly_tracks = []
discover_weekly_details = spotify_client.playlist(discover_weekly_id,
                                                  fields="tracks,next")
tracks = discover_weekly_details['tracks']
for track in tracks["items"]:
    discover_weekly_tracks.append(track["track"]["id"])

print("*** Step 3) Get Archive Playlist ID ***")
for playlist in playlists:
    name = playlist["name"]
    if name == archive_playlist_name:
        archive_id = playlist["id"]
        print("*** Playlist ID found ***")
        break
if archive_id is None:
    archive_playlist = spotify_client.user_playlist_create(user=username,
                                                           name=archive_playlist_name,
                                                           description=archive_playlist_description)
    archive_id = archive_playlist["id"]

print("*** Step 4) Get archive playlist tracks ***")
archive_details = get_playlist_tracks(username, archive_id)
archive_tracks = []
for track in archive_details:
    archive_tracks.append(track["track"]["id"])

print("*** Step 5) Add tracks to archive playlist ***")
try:
    for track in discover_weekly_tracks:
        if track not in archive_tracks:
            track_lst = []
            track_lst.append(track)
            spotify_client.playlist_add_items(archive_id, track_lst)
            print("*** Track passed duplicate check: Not in Archive Playlist. Track added to Playlist ***")
        else:
            print("*** Track NOT ADDED. DUPLICATE ***")
except:
    print("*** No tracks in Archive Playlist (Archive list is empty) ***")
    spotify_client.playlist_add_items(archive_id, discover_weekly_tracks)