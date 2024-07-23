import csv
from util.trie import Trie
from util.hashmap_manager import HashMap
from util.bplustree_manager import BPlusTree
from util.memory_manager import MemoryManager

class PlaylistManager:
    def __init__(self, t=4, max_cache_size=100):
        self.trie = Trie()
        self.hash_map = HashMap()
        self.bplus_tree = BPlusTree(t)
        self.memory_manager = MemoryManager(max_cache_size)
        self.load_songs_from_csv("data/spotify_data.csv")

    def load_songs_from_csv(self, file_path):
        with open(file_path, newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                song_name = row['track_name']
                song_details = {
                    "song_id": int(row['song_id']),
                    "name": row['track_name'],
                    "artist": row['artist_name'],
                    "track_id": row['track_id'],
                    "popularity": int(row['popularity']),
                    "year": int(row['year']),
                    "genre": row['genre'],
                    "danceability": float(row['danceability']),
                    "energy": float(row['energy']),
                    "key": int(row['key']),
                    "loudness": float(row['loudness']),
                    "mode": int(row['mode']),
                    "speechiness": float(row['speechiness']),
                    "acousticness": float(row['acousticness']),
                    "instrumentalness": float(row['instrumentalness']),
                    "liveness": float(row['liveness']),
                    "valence": float(row['valence']),
                    "tempo": float(row['tempo']),
                    "duration": int(row['duration_ms']),
                    "time_signature": int(row['time_signature'])
                }
                self.agregar_cancion(song_name, song_details)

    def agregar_cancion(self, song_name, song_details):
        song_id = song_details["song_id"]
        self.trie.insert(song_name, song_id)
        self.hash_map.insert(song_id, song_details)
        self.bplus_tree.insert(song_name, song_id)
        self.memory_manager.add_to_cache(song_id, song_details)
        return song_id

    def eliminar_cancion(self, song_name):
        song_ids = self.trie.search(song_name)
        if song_ids:
            song_id = song_ids[0]  # Asumimos que hay solo un ID por canción
            self.trie.delete(song_name, song_id)
            self.hash_map.delete(song_id)
            self.bplus_tree.delete(song_name)
            self.memory_manager.clear_cache()

    def cambiar_orden(self, posicion_actual, nueva_posicion):
        # Obtener la lista actual de canciones
        song_ids = self.hash_map.get_all_keys()
        if 0 <= posicion_actual < len(song_ids) and 0 <= nueva_posicion < len(song_ids):
            song_id = song_ids.pop(posicion_actual)
            song_ids.insert(nueva_posicion, song_id)
            # Actualizar la HashMap y el BPlusTree según el nuevo orden
            for index, song_id in enumerate(song_ids):
                song_details = self.hash_map.get(song_id)
                self.bplus_tree.insert(song_details['name'], index)
                self.memory_manager.add_to_cache(song_id, song_details)

    def obtener_canciones(self, criterion=None):
        if criterion is None:
            # Devolver todas las canciones en el orden actual
            song_ids = self.hash_map.get_all_keys()
            return [self.hash_map.get(song_id) for song_id in song_ids]
        elif criterion == "popularidad":
            # Implementar lógica para ordenar por popularidad
            pass
        elif criterion == "año":
            # Implementar lógica para ordenar por año
            pass
        elif criterion == "duración":
            # Implementar lógica para ordenar por duración
            pass

    def reproduccion_aleatoria(self):
        import random
        song_ids = self.hash_map.get_all_keys()
        random.shuffle(song_ids)
        return [self.hash_map.get(song_id) for song_id in song_ids]

# Ejemplo de uso:
if __name__ == "__main__":
    manager = PlaylistManager()
    print(manager.obtener_canciones())
    manager.eliminar_cancion("Shape of You")
    print(manager.obtener_canciones())
