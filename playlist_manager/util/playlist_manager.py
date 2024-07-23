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

    def agregar_cancion(self, song_name, song_details):
        song_id = len(self.hash_map.get_all_keys())  # Usar el número de canciones como ID
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
    manager.agregar_cancion("Song1", {"name": "Song1", "artist": "Artist1", "year": 2021, "duration": 300, "popularity": 90})
    manager.agregar_cancion("Song2", {"name": "Song2", "artist": "Artist2", "year": 2020, "duration": 200, "popularity": 80})
    print(manager.obtener_canciones())
    manager.eliminar_cancion("Song1")
    print(manager.obtener_canciones())
