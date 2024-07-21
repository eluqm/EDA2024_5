from util.file_manager import FileManager
from util.hashmap_manager import HashMap
from util.bplustree_manager import BPlusTree
from util.memory_manager import MemoryManager

class PlaylistManager:
    def __init__(self, bplustree_order, file_path, max_cache_size=500):
        self.memory_manager = MemoryManager(max_cache_size)
        self.file_manager = FileManager(file_path, self.memory_manager)
        self.hashmap = HashMap()
        self.bplustree = BPlusTree(bplustree_order)
        self.file_manager.load_songs()

    def agregar_cancion(self, song):
        self.hashmap.insert(song.song_id, song)
        self.bplustree.insert(song.popularity, song)

    def eliminar_cancion(self, song_id):
        self.hashmap.delete(song_id)
        # Actualiza el método para usar Trie
        song = self.hashmap.get(song_id)
        if song:
            self.file_manager.trie.delete(song.track_name, song_id)

    def ordenar_playlist(self, attribute, order='ascendente'):
        songs = [self.hashmap.get(key) for key in self.hashmap.get_all_keys()]
        if attribute == 'popularidad':
            songs.sort(key=lambda song: song.popularity, reverse=(order == 'descendente'))
        elif attribute == 'año':
            songs.sort(key=lambda song: song.year, reverse=(order == 'descendente'))
        elif attribute == 'duración':
            songs.sort(key=lambda song: song.duration_ms, reverse=(order == 'descendente'))
        return songs
