# playlist_manager/util/gui_manager.py

import tkinter as tk
from tkinter import ttk, messagebox
from util.playlist_manager import PlaylistManager

class GUIManager:
    def __init__(self, root, playlist_manager):
        self.root = root
        self.playlist_manager = playlist_manager
        self.create_widgets()

    def create_widgets(self):
        self.root.title("Gestor de Lista de Reproducción")
        self.root.geometry("600x400")

        self.search_frame = ttk.Frame(self.root, padding="10")
        self.search_frame.grid(row=0, column=0, sticky="ew")

        self.label_search = ttk.Label(self.search_frame, text="Buscar Canción:")
        self.label_search.grid(row=0, column=0, padx=5, pady=5)

        self.entry_search = ttk.Entry(self.search_frame)
        self.entry_search.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        self.button_search = ttk.Button(self.search_frame, text="Buscar y Agregar", command=self.buscar_y_agregar_cancion)
        self.button_search.grid(row=0, column=2, padx=5, pady=5)

        self.playlist_frame = ttk.Frame(self.root, padding="10")
        self.playlist_frame.grid(row=1, column=0, sticky="nsew")

        self.tree_playlist = ttk.Treeview(self.playlist_frame, columns=("track", "artist", "year"), show="headings")
        self.tree_playlist.heading("track", text="Canción")
        self.tree_playlist.heading("artist", text="Artista")
        self.tree_playlist.heading("year", text="Año")
        self.tree_playlist.grid(row=0, column=0, sticky="nsew")

        self.scroll_playlist = ttk.Scrollbar(self.playlist_frame, orient=tk.VERTICAL, command=self.tree_playlist.yview)
        self.tree_playlist.configure(yscroll=self.scroll_playlist.set)
        self.scroll_playlist.grid(row=0, column=1, sticky="ns")

        self.button_delete = ttk.Button(self.root, text="Eliminar Canción", command=self.eliminar_cancion)
        self.button_delete.grid(row=2, column=0, padx=5, pady=5, sticky="ew")

        self.button_order = ttk.Button(self.root, text="Ordenar Playlist", command=self.ordenar_playlist)
        self.button_order.grid(row=3, column=0, padx=5, pady=5, sticky="ew")

    def buscar_y_agregar_cancion(self):
        song_name = self.entry_search.get().strip()
        if song_name:
            songs = self.playlist_manager.file_manager.search_songs_by_name(song_name)
            if songs:
                selected_song = songs[0]  # Por simplicidad, agregamos la primera canción encontrada
                self.playlist_manager.agregar_cancion(selected_song)
                self.actualizar_playlist()
                messagebox.showinfo("Éxito", f"Se agregó la canción: {selected_song.track_name} by {selected_song.artist_name}")
            else:
                messagebox.showwarning("Sin Resultados", "No se encontraron canciones con ese nombre.")
        else:
            messagebox.showwarning("Entrada Inválida", "Por favor ingrese el nombre de una canción.")

    def eliminar_cancion(self):
        selected_item = self.tree_playlist.selection()
        if selected_item:
            song_id = self.tree_playlist.item(selected_item)["values"][0]
            self.playlist_manager.eliminar_cancion(song_id)
            self.actualizar_playlist()
            messagebox.showinfo("Éxito", f"Se eliminó la canción con ID: {song_id}")
        else:
            messagebox.showwarning("Selección Inválida", "Por favor seleccione una canción para eliminar.")

    def ordenar_playlist(self):
        attribute = "popularity"  # Aquí puedes solicitar al usuario el atributo por el cual desea ordenar
        ordered_songs = self.playlist_manager.get_songs_ordered_by(attribute)
        self.actualizar_playlist(ordered_songs)

    def actualizar_playlist(self, songs=None):
        for item in self.tree_playlist.get_children():
            self.tree_playlist.delete(item)
        songs = songs or [self.playlist_manager.hashmap.get(key) for key in self.playlist_manager.hashmap.get_all_keys()]
        for song in songs:
            self.tree_playlist.insert("", "end", values=(song.song_id, song.track_name, song.artist_name, song.year))

if __name__ == "__main__":
    root = tk.Tk()
    file_path = 'data/spotify_data.csv'
    playlist_manager = PlaylistManager(3, file_path)
    gui_manager = GUIManager(root, playlist_manager)
    root.mainloop()
