import csv
from model.song import Song

class FileManager:
    def __init__(self, file_path):
        self.file_path = file_path

    def load_songs(self):
        songs = []
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
                songs.append(song)
        return songs
