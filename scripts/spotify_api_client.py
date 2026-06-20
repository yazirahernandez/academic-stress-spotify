import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv

load_dotenv()

class SpotifyClient:
    def __init__(self):
        self.client_id = os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
        self.client = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
            client_id=self.client_id,
            client_secret=self.client_secret
        ))
    
    def get_audio_features(self, track_id):
        """Fetch audio features for a track"""
        return self.client.audio_features(track_id)
    
    def get_track_info(self, track_id):
        """Fetch track information"""
        return self.client.track(track_id)

# TODO: Implement full integration
