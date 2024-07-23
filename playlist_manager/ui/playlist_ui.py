import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.playlist_manager import PlaylistManager
import tkinter as tk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
import random

class PlaylistManagerApp:
    def __init__(self, root):
        self.root = root
        self.style = Style(theme='cosmo')  # Elegir un tema de ttkbootstrap
        self.root.title("Playlist Manager")

        # Inicializar el gestor de listas de reproducción
        self.manager = PlaylistManager()

        self.create_widgets()
        self.update_song_listbox()

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
            song_details = {"name": song, "artist": "Unknown", "year": 2021, "duration": 300, "popularity": 50}
            self.manager.agregar_cancion(song, song_details)
            self.update_song_listbox()

    def remove_song(self):
        selected_song_index = self.song_listbox.curselection()
        if selected_song_index:
            song = self.song_listbox.get(selected_song_index)
            self.manager.eliminar_cancion(song)
            self.update_song_listbox()

    def shuffle_songs(self):
        shuffled_songs = self.manager.reproduccion_aleatoria()
        self.song_listbox.delete(0, tk.END)
        for song in shuffled_songs:
            self.song_listbox.insert(tk.END, song["name"])

    def sort_songs(self):
        criterion = self.sort_options.get()
        sorted_songs = self.manager.obtener_canciones(criterion)
        self.song_listbox.delete(0, tk.END)
        for song in sorted_songs:
            self.song_listbox.insert(tk.END, song["name"])

    def update_song_listbox(self):
        self.song_listbox.delete(0, tk.END)
        songs = self.manager.obtener_canciones()
        for song in songs:
            self.song_listbox.insert(tk.END, f"{song['name']} by {song['artist']}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PlaylistManagerApp(root)
    root.mainloop()
