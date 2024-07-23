# playlist_manager/playlist_manager.py

from util.file_manager import FileManager
from util.hashmap_manager import HashMap
from util.memory_manager import MemoryManager

class PlaylistManager:
    def __init__(self, file_path, max_cache_size=500):
        self.memory_manager = MemoryManager(max_cache_size)
        self.file_manager = FileManager(file_path, self.memory_manager)
        self.hashmap = HashMap()
        self.file_manager.load_songs()

    def agregar_cancion(self, song):
        self.hashmap.insert(song.song_id, song)
        print(f"Se agregó la canción: {song.track_name} by {song.artist_name}")

    def mostrar_playlist(self):
        keys = self.hashmap.get_all_keys()
        for key in keys:
            song = self.hashmap.get(key)
            print(f"{song.track_name} by {song.artist_name}")

    def eliminar_cancion(self, song_id):
        self.hashmap.delete(song_id)
        print(f"Se eliminó la canción con ID: {song_id}")

    def buscar_canciones_por_nombre(self, song_name):
        return self.file_manager.search_songs_by_name(song_name)

    def ordenar_playlist(self, criterio, orden):
        # Implementar la lógica para ordenar la playlist basada en el criterio y orden dados
        pass
