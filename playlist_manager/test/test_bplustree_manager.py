from bplustree_manager import BPlusTree

# Crear instancia de BPlusTree
bplustree = BPlusTree(t=3)

# Agregar canciones (simplificado sin usar PlaylistManager)
canciones = [
    {'id': '1', 'title': 'Song A', 'artist': 'Artist 1', 'duration_ms': 200000, 'popularity': 90, 'year': 2020},
    {'id': '2', 'title': 'Song B', 'artist': 'Artist 2', 'duration_ms': 180000, 'popularity': 85, 'year': 2019},
    {'id': '3', 'title': 'Song C', 'artist': 'Artist 3', 'duration_ms': 220000, 'popularity': 95, 'year': 2021},
]

for cancion in canciones:
    bplustree.insert(cancion['id'], cancion)

# Verificar que los elementos están insertados correctamente
all_items = bplustree.get_all_items()
all_items_output = [(key, value['title']) for key, value in all_items]

# Ordenar canciones por popularidad
songs = [value for key, value in all_items]
songs.sort(key=lambda song: song['popularity'])

# Imprimir las canciones ordenadas para verificar
sorted_songs_output = [f"{song['title']} by {song['artist']} with popularity {song['popularity']}" for song in songs]

all_items_output, sorted_songs_output

def test_empty_tree(self):
    self.assertIsNone(self.tree.search(10))
    self.assertEqual(self.tree.range_search(0, 10), [])
