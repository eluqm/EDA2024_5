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
        songs = file_manager.search_songs_by_name(song_name)
        if songs:
            print("Se encontraron las siguientes canciones:")
            for idx, song in enumerate(songs):
                print(f"{idx + 1}. {song.track_name} by {song.artist_name} ({song.year})")
            seleccion = int(input("Seleccione el número de la canción que desea agregar: ")) - 1
            if 0 <= seleccion < len(songs):
                song = songs[seleccion]
                hashmap.insert(song.song_id, song)
                print(f"Se agregó la canción: {song.track_name} by {song.artist_name}")
            else:
                print("Selección inválida.")
        else:
            print("No se encontraron canciones con ese nombre.")

def eliminar_cancion():
    song_name = input("Ingrese el nombre de la canción que desea eliminar: ").strip()
    song_ids = trie.search(song_name)
    if song_ids:
        print("Se encontraron las siguientes canciones:")
        for idx, song_id in enumerate(song_ids):
            song = file_manager.get_song_by_id(song_id)
            print(f"{idx + 1}. {song.track_name} by {song.artist_name} ({song.year})")
        seleccion = int(input("Seleccione el número de la canción que desea eliminar: ")) - 1
        if 0 <= seleccion < len(song_ids):
            song_id = song_ids[seleccion]
            hashmap.delete(song_id)
            print(f"Se eliminó la canción con ID: {song_id}")
        else:
            print("Selección inválida.")
    else:
        print("No se encontraron canciones con ese nombre.")


def mostrar_playlist():
    keys = hashmap.get_all_keys()
    for key in keys:
        song = hashmap.get(key)
        print(f"{song.track_name} by {song.artist_name}")

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
        eliminar_cancion()
    elif opcion == '5':
        print("Saliendo...")
        break
    else:
        print("Opción inválida. Intente de nuevo.")