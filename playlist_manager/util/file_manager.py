# playlist_manager/util/file_manager.py

import csv
from model.song import Song
from util.trie import Trie

class FileManager:
    def __init__(self, file_path):
        self.file_path = file_path
        self.trie = Trie()
        self.songs = {}
        self.load_songs()

    def load_songs(self):
        with open(self.file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # Saltar la cabecera
            for row in reader:
                song_id, artist_name, track_name, track_id, popularity, year, genre, danceability, energy, key, loudness, mode, speechiness, acousticness, instrumentalness, liveness, valence, tempo, duration_ms, time_signature = row
                song = Song(
                    song_id, artist_name, track_name, track_id, int(popularity),
                    int(year), genre, float(danceability), float(energy), int(key),
                    float(loudness), int(mode), float(speechiness),
                    float(acousticness), float(instrumentalness),
                    float(liveness), float(valence), float(tempo),
                    int(duration_ms), int(time_signature)
                )
                self.trie.insert(track_name, song_id)
                self.songs[song_id] = song

    def get_song_by_id(self, song_id):
        return self.songs.get(song_id)

