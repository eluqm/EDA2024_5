import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from util.playlist_manager import PlaylistManager
from model.song import Song
import tkinter as tk
from tkinter import ttk
from ttkbootstrap import Style
from ttkbootstrap.constants import *
from PIL import Image, ImageTk

class PlaylistManagerApp:
    def __init__(self, root):
        self.root = root
        self.style = Style(theme='cyborg')  # Elegir un tema de ttkbootstrap
        self.root.title("Playlist Manager")
        self.root.geometry("1000x600")  # Tamaño de la ventana

        # Inicializar el gestor de listas de reproducción
        file_path = 'data/spotify_data.csv'
        self.manager = PlaylistManager(file_path)
        self.create_widgets()
        self.update_song_listbox()

    def create_widgets(self):
        # Frame para la canción actual
        self.current_song_frame = ttk.LabelFrame(self.root, text="Now Playing", padding="10")
        self.current_song_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=10, pady=10)

        self.song_title_label = ttk.Label(self.current_song_frame, text="Name of the music", font=("Helvetica", 16, "bold"))
        self.song_title_label.grid(row=0, column=0, sticky="w")

        self.artist_label = ttk.Label(self.current_song_frame, text="Artist", font=("Helvetica", 12, "italic"))
        self.artist_label.grid(row=1, column=0, sticky="w")

        self.album_cover_label = ttk.Label(self.current_song_frame)
        self.album_cover_label.grid(row=0, column=1, rowspan=2, sticky="e")
        self.load_album_cover("../img/album_cover.jpg")  # Actualiza con la imagen correcta

        # Controles de reproducción
        self.play_controls_frame = ttk.Frame(self.current_song_frame, padding="10")
        self.play_controls_frame.grid(row=2, column=0, columnspan=2, sticky="ew")

        self.previous_button = ttk.Button(self.play_controls_frame, text="⏮", style="info.TButton")
        self.previous_button.grid(row=0, column=0, padx=5)

        self.play_button = ttk.Button(self.play_controls_frame, text="▶", style="success.TButton")
        self.play_button.grid(row=0, column=1, padx=5)

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

        # Frame para controles de búsqueda y ordenación
        self.controls_frame = ttk.LabelFrame(self.root, text="Controls", padding="10")
        self.controls_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        self.add_song_label = ttk.Label(self.controls_frame, text="Buscar y añadir canción:")
        self.add_song_label.grid(row=0, column=0, padx=5, pady=5)

        self.song_entry = ttk.Entry(self.controls_frame)
        self.song_entry.grid(row=0, column=1, padx=5, pady=5)

        self.add_button = ttk.Button(self.controls_frame, text="Buscar", command=self.search_song, style="success.TButton")
        self.add_button.grid(row=0, column=2, padx=5, pady=5)

        self.search_results_listbox = tk.Listbox(self.controls_frame, height=10, width=50)
        self.search_results_listbox.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
        self.search_results_listbox.bind("<Double-1>", self.add_selected_song)

        self.search_results_label = ttk.Label(self.controls_frame, text="Resultados de búsqueda:")
        self.search_results_label.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        self.sort_label = ttk.Label(self.controls_frame, text="Ordenar por:")
        self.sort_label.grid(row=3, column=0, padx=5, pady=5)

        self.sort_popularity_button = ttk.Button(self.controls_frame, text="Popularidad", command=lambda: self.sort_songs("popularidad"), style="primary.TButton")
        self.sort_popularity_button.grid(row=3, column=1, padx=5, pady=5)

        self.sort_year_button = ttk.Button(self.controls_frame, text="Año", command=lambda: self.sort_songs("año"), style="primary.TButton")
        self.sort_year_button.grid(row=3, column=2, padx=5, pady=5)

        self.sort_duration_button = ttk.Button(self.controls_frame, text="Duración", command=lambda: self.sort_songs("duración"), style="primary.TButton")
        self.sort_duration_button.grid(row=3, column=3, padx=5, pady=5)

        self.order_options = ttk.Combobox(self.controls_frame, values=["ascendente", "descendente"])
        self.order_options.grid(row=3, column=4, padx=5, pady=5)
        self.order_options.current(0)  # Valor predeterminado: ascendente

        # Frame para la lista de reproducción
        self.playlist_frame = ttk.LabelFrame(self.root, text="Playlist", padding="10")
        self.playlist_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)

        self.song_listbox = tk.Listbox(self.playlist_frame, height=15, width=50)
        self.song_listbox.grid(row=0, column=0, columnspan=4, padx=10, pady=10)
        self.song_listbox.bind("<<ListboxSelect>>", self.show_now_playing)  # Vincular el evento de selección

        self.remove_button = ttk.Button(self.playlist_frame, text="Eliminar canción seleccionada", command=self.remove_song, style="danger.TButton")
        self.remove_button.grid(row=1, column=0, columnspan=4, pady=5)

    def load_album_cover(self, path):
        try:
            image = Image.open(path)
            image = image.resize((100, 100), Image.LANCZOS)
            self.album_cover = ImageTk.PhotoImage(image)
            self.album_cover_label.config(image=self.album_cover)
            self.album_cover_label.image = self.album_cover
        except Exception as e:
            print(f"Error loading image: {e}")

    def add_song(self, song):
        self.manager.agregar_cancion(song)
        self.update_song_listbox()

    def search_song(self):
        song_name = self.song_entry.get().strip()
        if song_name:
            songs = self.manager.buscar_canciones_por_nombre(song_name)
            self.search_results_listbox.delete(0, tk.END)
            if songs:
                for song in songs:
                    self.search_results_listbox.insert(tk.END, f"{song.track_name} by {song.artist_name} ({song.year})")
                self.search_results_label.config(text=f"Resultados de búsqueda: {len(songs)} canciones encontradas")
            else:
                self.search_results_listbox.insert(tk.END, "No se encontraron canciones.")
                self.search_results_label.config(text="Resultados de búsqueda: 0 canciones encontradas")
        self.song_entry.delete(0, tk.END)

    def add_selected_song(self, event):
        selected_index = self.search_results_listbox.curselection()
        if selected_index:
            selected_song = self.search_results_listbox.get(selected_index)
            song_name, _ = selected_song.split(" by ")
            songs = self.manager.buscar_canciones_por_nombre(song_name)
            if songs:
                self.add_song(songs[0])

    def remove_song(self):
        selected_song_index = self.song_listbox.curselection()
        if selected_song_index:
            selected_song = self.song_listbox.get(selected_song_index)
            # Separamos el índice de la canción del nombre y el artista
            song_info = " ".join(selected_song.split(" ")[1:]).split(" by ")
            if len(song_info) == 2:
                song_name, artist = song_info
                songs = self.manager.buscar_canciones_por_nombre(song_name)
                if songs:
                    self.manager.eliminar_cancion(songs[0].song_id)
                    self.update_song_listbox()

    def shuffle_songs(self):
        shuffled_songs = self.manager.reproduccion_aleatoria()
        self.song_listbox.delete(0, tk.END)
        for index, song in enumerate(shuffled_songs, 1):
            self.song_listbox.insert(tk.END, f"{index}. {song.track_name} by {song.artist_name}")

    def sort_songs(self, criterion):
        order = self.order_options.get()
        sorted_songs = self.manager.ordenar_playlist(criterion, order)
        if sorted_songs:
            self.song_listbox.delete(0, tk.END)
            for index, song in enumerate(sorted_songs, 1):
                self.song_listbox.insert(tk.END, f"{index}. {song.track_name} by {song.artist_name}")

    def update_song_listbox(self):
        self.song_listbox.delete(0, tk.END)
        song_ids = self.manager.hashmap.get_all_keys()
        for index, song_id in enumerate(song_ids, 1):
            song = self.manager.hashmap.get(song_id)
            self.song_listbox.insert(tk.END, f"{index}. {song.track_name} by {song.artist_name}")

    def show_now_playing(self, event):
        selected_song_index = self.song_listbox.curselection()
        if selected_song_index:
            selected_song = self.song_listbox.get(selected_song_index)
            song_info = " ".join(selected_song.split(" ")[1:]).split(" by ")
            if len(song_info) == 2:
                song_name, artist = song_info
                songs = self.manager.buscar_canciones_por_nombre(song_name)
                if songs:
                    song = songs[0]
                    self.song_title_label.config(text=song.track_name)
                    self.artist_label.config(text=song.artist_name)
                    self.end_time_label.config(text=f"{song.duration_ms // 60000}:{(song.duration_ms // 1000) % 60:02d}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PlaylistManagerApp(root)
    root.mainloop()
