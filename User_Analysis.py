import time
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from tqdm import tqdm
from requests.exceptions import ReadTimeout
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import ptitprince as pt
import os

def login_to_spotify():
    print("*** Step 1) Connect to api ***")
    scope = "user-read-private playlist-read-private user-library-read user-library-modify user-top-read playlist-modify-public playlist-modify-private"
    spotify_object = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,
                                                           client_id=os.environ.get("CLIENT_ID"),
                                                           client_secret=os.environ.get("CLIENT_SECRET"),
                                                           redirect_uri=os.environ.get("REDIRECT_URI"),
                                                           cache_path='cache.txt'))
    return spotify_object



# Get the current user's profile
spotify_object = login_to_spotify()
user_profile = spotify_object.current_user()

# Find all 'The Ultimate Discover Weekly Playlist' playlists on spotify
results = spotify_object.search(q='The Ultimate Discover Weekly Playlist', type='playlist')['playlists']
playlist_id = None
for playlist in results['items']:
    # Access my 'The Ultimate Discover Weekly Playlist' playlist
    if playlist["description"] == "A playlist containing past discover weekly playlists":
        playlist_id = playlist["id"]

# Access all tracks in playlist
results = spotify_object.playlist_tracks(playlist_id)
tracks = results['items']
while results['next']:
    results = spotify_object.next(results)
    tracks.extend(results['items'])

track_features = []
for track in tqdm(tracks):
    print(track['track']['name'], track['added_at'])
    track_name = track['track']['name']
    track_added = track['added_at']
    track_popularity = track['track']['popularity']
    try:
        track_features.append([track_name, track_added, spotify_object.audio_features(track['track']['uri'])])
    except ReadTimeout:
        i = 1
        while i < 5:
            print(f'\nSpotify timed out... Retry No. {i} of 5... Waiting now for 30 seconds...')
            time.sleep(30)
            track_features.append([track_name, track_added, spotify_object.audio_features(track['track']['uri'])])
            i += 1

# Create an empty list to store the rows of the DataFrame
rows = []
# Iterate over the elements in the track_features list
for feature in track_features:
    try:
        # Create a new dictionary with keys for the name, added_at timestamp, and audio features
        data = {'name': feature[0], 'added_at': feature[1]}
        data.update(feature[2][0])
        # Append the data dictionary to the rows list
        rows.append(data)
    except:
        pass
# Create a DataFrame from the rows list
track_info_df = pd.DataFrame(rows)
print(track_info_df.columns)

# Generate Genres
track_genres = []
for track in tqdm(tracks):
    artist_id = track['track']['artists'][0]['id']
    try:
        artist_genres = spotify_object.artist(artist_id)['genres']
        track_genres.append([track['track']['name'], artist_genres])
    except ReadTimeout:
        i = 1
        while i < 5:
            print(f'\nSpotify timed out... Retry No. {i} of 5... Waiting now for 30 seconds...')
            time.sleep(30)
            artist_genres = spotify_object.artist(artist_id)['genres']
            track_genres.append([track['track']['name'], artist_genres])
            i += 1

# Add to DF
track_info_df['genres'] = [i[1] for i in track_genres]
# Convert the added_at column to datetime
track_info_df['added_at'] = pd.to_datetime(track_info_df['added_at'])

# Create a line chart of the danceability values over time
plt.scatter(track_info_df['added_at'], track_info_df['speechiness'])
plt.xlabel('Added At')
plt.ylabel('speechiness')
plt.show()

# Create a pivot table of audio features by added_at timestamp
pivot_table = pd.pivot_table(track_info_df, values=['danceability','energy','loudness','tempo','valence'],
                             index='added_at', columns='name')

# Create a line plot of the pivot table
sns.lineplot(data=track_info_df, x="added_at", y="acousticness")
plt.show()
