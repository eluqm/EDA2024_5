# playlist_manager/util/playlist_manager.py
from util.file_manager import FileManager
from util.hashmap_manager import HashMap
from util.bplustree_manager import BPlusTree
from util.memory_manager import MemoryManager

class PlaylistManager:
    def __init__(self, file_path, max_cache_size=500):
        self.memory_manager = MemoryManager(max_cache_size)
        self.file_manager = FileManager(file_path, self.memory_manager)
        self.hashmap = HashMap()
        self.bplustree = BPlusTree(t=4)  
        self.file_manager.load_songs()
    def agregar_cancion(self, song):
        if self.hashmap.get(song.song_id) is None:
            self.hashmap.insert(song.song_id, song)
            print(f"Se agregó la canción: {song.track_name} by {song.artist_name}")
        else:
            print(f"La canción {song.track_name} by {song.artist_name} ya está en la lista de reproducción.")

    def mostrar_playlist(self):
        print("Lista de reproducción:")
        for song_id in self.hashmap.get_all_keys():
            song = self.hashmap.get(song_id)
            print(f"{song.track_name} by {song.artist_name}")

    def eliminar_cancion(self, song_id):
        self.hashmap.delete(song_id)
        print(f"Se eliminó la canción con ID: {song_id}")

    def buscar_canciones_por_nombre(self, song_name):
        return self.file_manager.search_songs_by_name(song_name)

    def ordenar_playlist(self, criterion, order='ascendente'):
        # Limpiar BPlusTree antes de insertar los datos
        self.bplustree = BPlusTree(t=4)
        
        # Extraer todas las canciones del HashMap e insertarlas en el BPlusTree
        all_songs = [self.hashmap.get(song_id) for song_id in self.hashmap.get_all_keys()]
        for song in all_songs:
            self.bplustree.insert(song.song_id, song)
        
        # Obtener las canciones ordenadas del BPlusTree
        all_items = self.bplustree.get_all_items()
        songs = [song for _, song in all_items]

        reverse = True if order == 'descendente' else False
        if criterion == "popularidad":
            songs.sort(key=lambda song: song.popularity, reverse=reverse)
        elif criterion == "año":
            songs.sort(key=lambda song: song.year, reverse=reverse)
        elif criterion == "duración":
            songs.sort(key=lambda song: song.duration_ms, reverse=reverse)

        return songs


    def reproduccion_aleatoria(self):
        import random
        song_ids = self.hashmap.get_all_keys()
        random.shuffle(song_ids)
        return [self.hashmap.get(song_id) for song_id in song_ids]
