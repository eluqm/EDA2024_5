import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from util.trie import Trie
from util.hashmap_manager import HashMap
from util.bplustree_manager import BPlusTree
from util.memory_manager import MemoryManager
import random

class PlaylistManagerApp:
    def __init__(self, root):
        self.root = root
        self.style = Style(theme='cosmo')  # Elegir un tema de ttkbootstrap
        self.root.title("Playlist Manager")

        # Inicializar estructuras de datos
        self.trie = Trie()
        self.hash_map = HashMap()
        self.bplus_tree = BPlusTree(t=4)  # Elige un valor adecuado para t
        self.memory_manager = MemoryManager(max_cache_size=100)

        self.create_widgets()

    def create_widgets(self):
        # Sección de información de la canción actual
        self.current_song_frame = ttk.Frame(self.root, padding="10")
        self.current_song_frame.grid(row=0, column=0, columnspan=2, sticky="nsew")

        self.song_title_label = ttk.Label(self.current_song_frame, text="Name of the music", font=("Helvetica", 16))
        self.song_title_label.grid(row=0, column=0, sticky="w")

        self.artist_label = ttk.Label(self.current_song_frame, text="Artist", font=("Helvetica", 12))
        self.artist_label.grid(row=1, column=0, sticky="w")

        self.album_cover_label = ttk.Label(self.current_song_frame)
        self.album_cover_label.grid(row=0, column=1, rowspan=2, sticky="e")
        self.album_cover_label.config(image=tk.PhotoImage(file="img/album_cover.png"))  # Actualiza con la imagen correcta

        # Controles de reproducción
        self.play_controls_frame = ttk.Frame(self.current_song_frame, padding="10")
        self.play_controls_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.play_button = ttk.Button(self.play_controls_frame, text="▶", style="success.TButton")
        self.play_button.grid(row=0, column=1, padx=5)

        self.previous_button = ttk.Button(self.play_controls_frame, text="⏮", style="info.TButton")
        self.previous_button.grid(row=0, column=0, padx=5)

        self.next_button = ttk.Button(self.play_controls_frame, text="⏭", style="info.TButton")
        self.next_button.grid(row=0, column=2, padx=5)

        # Barra de progreso
        self.progress_frame = ttk.Frame(self.current_song_frame, padding="10")
        self.progress_frame.grid(row=3, column=0, columnspan=2, sticky="ew")

        self.start_time_label = ttk.Label(self.progress_frame, text="0:00")
        self.start_time_label.grid(row=0, column=0, sticky="w")

        self.end_time_label = ttk.Label(self.progress_frame, text="3:30")
        self.end_time_label.grid(row=0, column=2, sticky="e")

        self.progress_bar = ttk.Progressbar(self.progress_frame, length=200, style="info.Horizontal.TProgressbar")
        self.progress_bar.grid(row=0, column=1, padx=10)

        # Sección de la lista de reproducción y controles
        self.playlist_frame = ttk.Frame(self.root, padding="10")
        self.playlist_frame.grid(row=1, column=0, columnspan=2, sticky="nsew")

        self.add_song_label = ttk.Label(self.playlist_frame, text="Añadir canción:")
        self.add_song_label.grid(row=0, column=0, padx=5, pady=5)

        self.song_entry = ttk.Entry(self.playlist_frame)
        self.song_entry.grid(row=0, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self.playlist_frame, text="Agregar", command=self.add_song, style="success.TButton")
        self.add_button.grid(row=0, column=2, padx=5, pady=5)

        self.sort_label = ttk.Label(self.playlist_frame, text="Ordenar por:")
        self.sort_label.grid(row=1, column=0, padx=5, pady=5)

        self.sort_options = ttk.Combobox(self.playlist_frame, values=["Popularidad", "Año", "Duración"])
        self.sort_options.grid(row=1, column=1, padx=5, pady=5)

        self.sort_button = ttk.Button(self.playlist_frame, text="Ordenar", command=self.sort_songs, style="primary.TButton")
        self.sort_button.grid(row=1, column=2, padx=5, pady=5)

        self.song_listbox = tk.Listbox(self.playlist_frame, height=15, width=50)
        self.song_listbox.grid(row=2, column=0, columnspan=3, padx=10, pady=10)

        self.remove_button = ttk.Button(self.playlist_frame, text="Eliminar canción seleccionada", command=self.remove_song, style="danger.TButton")
        self.remove_button.grid(row=3, column=0, columnspan=3, pady=5)

    def add_song(self):
        song = self.song_entry.get()
        if song:
            song_id = len(self.hash_map.get_all_keys())  # Usar el número de canciones como ID
            self.trie.insert(song, song_id)
            self.hash_map.insert(song_id, song)
            self.bplus_tree.insert(song, song_id)
            self.memory_manager.add_to_cache(song_id, song)
            self.update_song_listbox()

    def remove_song(self):
        selected_song_index = self.song_listbox.curselection()
        if selected_song_index:
            song = self.song_listbox.get(selected_song_index)
            song_ids = self.trie.search(song)
            if song_ids:
                song_id = song_ids[0]  # Asumimos que hay solo un ID por canción
                self.trie.delete(song, song_id)
                self.hash_map.delete(song_id)
                self.bplus_tree.delete(song)
                self.memory_manager.clear_cache()
                self.update_song_listbox()

    def shuffle_songs(self):
        song_ids = self.hash_map.get_all_keys()
        random.shuffle(song_ids)
        self.song_listbox.delete(0, tk.END)
        for song_id in song_ids:
            song = self.hash_map.get(song_id)
            self.song_listbox.insert(tk.END, song)

    def sort_songs(self):
        criterion = self.sort_options.get()
        # Implementar lógica para ordenar canciones según el criterio seleccionado
        self.update_song_listbox()

    def update_song_listbox(self):
        self.song_listbox.delete(0, tk.END)
        for song_id in self.hash_map.get_all_keys():
            song = self.hash_map.get(song_id)
            self.song_listbox.insert(tk.END, song)

if __name__ == "__main__":
    root = tk.Tk()
    app = PlaylistManagerApp(root)
    root.mainloop()
