import tkinter as tk
from tkinter import simpledialog
from PIL import Image, ImageTk
from util.playlist_manager import PlaylistManager  # Ajustar la importación si es necesario

class GUIManager:
    def __init__(self, root, playlist_manager):
        self.root = root
        self.playlist_manager = playlist_manager
        self.create_widgets()

    def create_widgets(self):
        self.album_frame = tk.Frame(self.root, bg='black')
        self.album_frame.pack(padx=10, pady=10)
        
        self.album_cover_image = Image.open('playlist_manager/img/album_cover.jpg')
        self.album_cover_image = self.album_cover_image.resize((300, 300), Image.LANCZOS)
        self.album_cover_photo = ImageTk.PhotoImage(self.album_cover_image)
        self.album_cover = tk.Label(self.album_frame, image=self.album_cover_photo, bg='black')
        self.album_cover.pack()

        self.song_info_frame = tk.Frame(self.root, bg='white')
        self.song_info_frame.pack(padx=10, pady=10)

        self.song_title = tk.Label(self.song_info_frame, text="Name of the music", font=("Arial", 20), bg='white')
        self.song_title.pack()

        self.song_artist = tk.Label(self.song_info_frame, text="Artist", font=("Arial", 14), bg='white')
        self.song_artist.pack()

        self.controls_frame = tk.Frame(self.root, bg='white')
        self.controls_frame.pack(padx=10, pady=10)

        self.prev_button = tk.Button(self.controls_frame, text="Prev", command=self.prev_song)
        self.prev_button.pack(side='left', padx=5)

        self.play_button = tk.Button(self.controls_frame, text="Play", command=self.play_song)
        self.play_button.pack(side='left', padx=5)

        self.next_button = tk.Button(self.controls_frame, text="Next", command=self.next_song)
        self.next_button.pack(side='left', padx=5)

        self.playlist_frame = tk.Frame(self.root, bg='white')
        self.playlist_frame.pack(padx=10, pady=10)

        self.playlist_title = tk.Label(self.playlist_frame, text="My playlist", font=("Arial", 18), bg='white')
        self.playlist_title.pack()

        self.add_button = tk.Button(self.playlist_frame, text="Añadir", command=self.add_song)
        self.add_button.pack()

        self.playlist_listbox = tk.Listbox(self.playlist_frame)
        self.playlist_listbox.pack()

        self.populate_playlist()

    def populate_playlist(self):
        for key in self.playlist_manager.hashmap.get_all_keys():
            song = self.playlist_manager.hashmap.get(key)
            self.playlist_listbox.insert(tk.END, f"{song.track_name} - {song.artist_name}")

    def add_song(self):
        song_name = simpledialog.askstring("Agregar canción", "Ingrese el nombre de la canción:")
        if song_name:
            songs = self.playlist_manager.file_manager.search_songs_by_name(song_name)
            if songs:
                song = songs[0]  # Usar la primera canción encontrada para simplificar
                self.playlist_manager.agregar_cancion(song)
                self.playlist_listbox.insert(tk.END, f"{song.track_name} - {song.artist_name}")


