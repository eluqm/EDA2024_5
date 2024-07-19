# playlist_manager/util/file_manager.py
import csv
from model.song import Song
from util.trie import Trie

class FileManager:
    def __init__(self, file_path, memory_manager, prefix_length=5):
        self.file_path = file_path
        self.memory_manager = memory_manager
        self.trie = Trie()
        self.song_index = {}
        self.prefix_length = prefix_length

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
                prefix = track_name[:self.prefix_length]
                self.trie.insert(prefix, song_id)
                self.song_index[song_id] = song

    def get_song_by_id(self, song_id):
        song = self.memory_manager.get_from_cache(song_id)
        if song is None:
            song = self.song_index.get(song_id)
            if song:
                self.memory_manager.add_to_cache(song_id, song)
        return song

    def search_songs_by_name(self, song_name):
        prefix = song_name[:self.prefix_length]
        song_ids = self.trie.search(prefix)
        songs = [self.get_song_by_id(song_id) for song_id in song_ids]
        return [song for song in songs if song and song.track_name.startswith(song_name)]