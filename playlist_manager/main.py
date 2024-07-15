# playlist_manager/main.py
from util.file_manager import FileManager
from util.btree_manager import BTree
from util.hashmap_manager import HashMap

file_path = 'data/spotify_data.csv'
file_manager = FileManager(file_path)
songs = file_manager.load_songs()

# Crear B-Tree y HashMap
btree = BTree(t=3)
hashmap = HashMap(size=10000)

# Insertar canciones en B-Tree y HashMap
for song in songs:
  #   btree.insert(song.popularity, song)
    hashmap.insert(song.song_id, song)

# Ejemplo de búsqueda
#song_by_popularity = btree.search(85)  # Buscar canción por popularidad
song_by_id = hashmap.get('2')  # Buscar canción por ID
print(song_by_id)