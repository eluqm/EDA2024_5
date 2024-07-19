# playlist_manager/main.py

from util.file_manager import FileManager
from util.bplustree_manager import BPlusTree
from util.hashmap_manager import HashMap
from util.memory_manager import MemoryManager

file_path = 'data/spotify_data.csv'
memory_manager = MemoryManager(max_cache_size=500)  # Tamaño de la caché ajustable
file_manager = FileManager(file_path, memory_manager)

trie = file_manager.trie
hashmap = HashMap()
#bplustree = BPlusTree()

# Cargar canciones desde el archivo CSV
file_manager.load_songs()

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

def mostrar_playlist():
    keys = hashmap.get_all_keys()
    for key in keys:
        song = hashmap.get(key)
        print(f"{song.track_name} by {song.artist_name}")

def ordenar_playlist(criterio, orden):
    pass
def eliminar_cancion():
    song_name = input("Ingrese el nombre de la canción que desea eliminar: ").strip()
    songs = file_manager.search_songs_by_name(song_name)
    if songs:
        print("Se encontraron las siguientes canciones:")
        for idx, song in enumerate(songs):
            print(f"{idx + 1}. {song.track_name} by {song.artist_name} ({song.year})")
        seleccion = int(input("Seleccione el número de la canción que desea eliminar: ")) - 1
        if 0 <= seleccion < len(songs):
            song_id = songs[seleccion].song_id
            hashmap.delete(song_id)
            #bplustree.delete(song_id)  # También eliminamos del B+ Tree
            print(f"Se eliminó la canción con ID: {song_id}")
        else:
            print("Selección inválida.")
    else:
        print("No se encontraron canciones con ese nombre.")

# Interacción con el usuario
while True:
    print("\nOpciones:")
    print("1. Buscar y agregar canciones")
    print("2. Mostrar lista de reproducción")
    print("3. Ordenar lista de reproducción")
    print("4. Eliminar canción de la lista de reproducción")
    print("5. Salir")
    opcion = input("Seleccione una opción: ").strip()

    if opcion == '1':
        buscar_y_agregar_cancion()
    elif opcion == '2':
        mostrar_playlist()
    elif opcion == '3':
        print("Opciones de ordenación:")
        print("1. Por popularidad")
        print("2. Por año")
        print("3. Por duración")
        criterio_opcion = input("Seleccione un criterio: ").strip()
        if criterio_opcion == '1':
            criterio = "popularidad"
        elif criterio_opcion == '2':
            criterio = "año"
        elif criterio_opcion == '3':
            criterio = "duración"
        else:
            print("Criterio inválido.")
            continue

        orden = input("Seleccione el orden (ascendente/descendente): ").strip().lower()
        if orden not in ["ascendente", "descendente"]:
            print("Orden inválido.")
            continue

        ordenar_playlist(criterio, orden)
    elif opcion == '4':
        eliminar_cancion()
    elif opcion == '5':
        print("Saliendo...")
        break
    else:
        print("Opción inválida. Intente de nuevo.")
