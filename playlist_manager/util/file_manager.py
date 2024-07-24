import csv
from model.song import Song
from util.trie import Trie
from util.hashmap_manager import HashMap

class FileManager:
    def __init__(self, file_path, memory_manager, prefix_length=5):
        self.file_path = file_path
        self.memory_manager = memory_manager
        self.trie = Trie(prefix_length)
        self.song_index = HashMap()
        self.prefix_length = prefix_length

    def load_songs(self):
        with open(self.file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for i, row in enumerate(reader):
                try:
                    song_id = int(row['song_id']) if 'song_id' in row else i + 1
                    artist_name = row['artist_name']
                    track_name = row['track_name']
                    track_id = row['track_id']
                    popularity = int(row['popularity'])
                    year = int(row['year'])
                    genre = row['genre']
                    danceability = float(row['danceability'])
                    energy = float(row['energy'])
                    key = int(row['key'])
                    loudness = float(row['loudness'])
                    mode = int(row['mode'])
                    speechiness = float(row['speechiness'])
                    acousticness = float(row['acousticness'])
                    instrumentalness = float(row['instrumentalness'])
                    liveness = float(row['liveness'])
                    valence = float(row['valence'])
                    tempo = float(row['tempo'])
                    duration_ms = int(row['duration_ms'])
                    time_signature = int(row['time_signature'])

                    song = Song(
                        song_id, artist_name, track_name, track_id, popularity, year, genre,
                        danceability, energy, key, loudness, mode, speechiness,
                        acousticness, instrumentalness, liveness, valence, tempo, duration_ms, time_signature
                    )
                    prefix = track_name[:self.prefix_length]
                    self.trie.insert(prefix, song_id)
                    self.song_index.insert(song_id, song)
                except KeyError as e:
                    print(f"Missing expected column in CSV: {e}")
                except ValueError as e:
                    print(f"Invalid data format in CSV: {e}")

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
