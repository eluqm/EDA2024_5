# playlist_manager/main.py

from util.file_manager import FileManager
from util.bplustree_manager import BPlusTree
from util.hashmap_manager import HashMap

file_path = 'data/spotify_data.csv'
file_manager = FileManager(file_path)
file_manager.load_songs()

trie = file_manager.trie
hashmap = HashMap()
#bplustree = BPlusTree(3)

# Funciones
def buscar_y_agregar_cancion():
    while True:
        song_name = input("Ingrese el nombre de la canción que desea agregar (o 'terminar' para finalizar): ").strip()
        if song_name.lower() == 'terminar':
            break
        song_ids = trie.search(song_name)
        if song_ids:
            for song_id in song_ids:
                song = file_manager.get_song_by_id(song_id)
                if song:
                    hashmap.insert(song_id, song)
                    print(f"Se agregó la canción: {song.track_name}")
                else:
                    print(f"No se encontró la canción con ID {song_id}")
        else:
            print("No se encontraron canciones con ese nombre.")

def mostrar_playlist():
  pass

def ordenar_playlist():
  pass

# Interacción con el usuario
while True:
    print("\nOpciones:")
    print("1. Buscar y agregar canciones")
    print("2. Mostrar lista de reproducción")
    print("3. Ordenar lista de reproducción")
    print("4. Salir")
    opcion = input("Seleccione una opción: ").strip()

    if opcion == '1':
        buscar_y_agregar_cancion()
    elif opcion == '2':
        mostrar_playlist()
    elif opcion == '3':
        ordenar_playlist()
    elif opcion == '4':
        print("Saliendo...")
        break
    else:
        print("Opción inválida. Intente de nuevo.")
