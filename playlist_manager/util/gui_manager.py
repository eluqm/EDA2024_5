import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from util.playlist_manager import PlaylistManager

class GUIManager:
    def __init__(self, root, playlist_manager):
        self.root = root
        self.playlist_manager = playlist_manager
        self.create_widgets()

    def create_widgets(self):
        self.root.title("Gestor de Lista de Reproducción")
        self.root.geometry("600x800")
        self.root.configure(bg='black')

        # Album Cover and Title
        self.album_frame = ttk.Frame(self.root, padding="10")
        self.album_frame.grid(row=0, column=0, sticky="ew", pady=20)

        self.album_cover = tk.Label(self.album_frame, image=tk.PhotoImage(file='path/to/album_cover.png'), bg='black')
        self.album_cover.grid(row=0, column=0, padx=5, pady=5)

        self.album_title = tk.Label(self.album_frame, text="Album Title", font=("Helvetica", 20), fg='white', bg='black')
        self.album_title.grid(row=1, column=0, padx=5, pady=5)

        self.play_button = ttk.Button(self.album_frame, text="Play", command=self.play_album)
        self.play_button.grid(row=2, column=0, padx=5, pady=5)

        # Playlist TreeView
        self.playlist_frame = ttk.Frame(self.root, padding="10")
        self.playlist_frame.grid(row=1, column=0, sticky="nsew")

        self.tree_playlist = ttk.Treeview(self.playlist_frame, columns=("track", "artist"), show="headings", height=15)
        self.tree_playlist.heading("track", text="Song Title")
        self.tree_playlist.heading("artist", text="Artist")
        self.tree_playlist.grid(row=0, column=0, sticky="nsew")

        self.scroll_playlist = ttk.Scrollbar(self.playlist_frame, orient=tk.VERTICAL, command=self.tree_playlist.yview)
        self.tree_playlist.configure(yscroll=self.scroll_playlist.set)
        self.scroll_playlist.grid(row=0, column=1, sticky="ns")

        # Control Buttons
        self.control_frame = ttk.Frame(self.root, padding="10")
        self.control_frame.grid(row=2, column=0, sticky="ew")

        self.button_add = ttk.Button(self.control_frame, text="Agregar Canción", command=self.buscar_cancion)
        self.button_add.grid(row=0, column=0, padx=5, pady=5)

        self.button_delete = ttk.Button(self.control_frame, text="Eliminar Canción", command=self.eliminar_cancion)
        self.button_delete.grid(row=0, column=1, padx=5, pady=5)

        self.button_order = ttk.Button(self.control_frame, text="Ordenar Playlist", command=self.ordenar_playlist)
        self.button_order.grid(row=0, column=2, padx=5, pady=5)


    def buscar_cancion(self):
        song_name = simpledialog.askstring("Buscar Canción", "Ingrese el nombre de la canción:")
        if song_name:
            songs = self.playlist_manager.file_manager.search_songs_by_name(song_name)
            if songs:
                self.show_search_results(songs)
            else:
                messagebox.showwarning("Sin Resultados", "No se encontraron canciones con ese nombre.")
        else:
            messagebox.showwarning("Entrada Inválida", "Por favor ingrese el nombre de una canción.")

    def show_search_results(self, songs):
        result_window = tk.Toplevel(self.root)
        result_window.title("Resultados de la Búsqueda")
        result_window.geometry("400x300")

        tree_results = ttk.Treeview(result_window, columns=("track", "artist"), show="headings")
        tree_results.heading("track", text="Song Title")
        tree_results.heading("artist", text="Artist")
        tree_results.grid(row=0, column=0, sticky="nsew")

        scroll_results = ttk.Scrollbar(result_window, orient=tk.VERTICAL, command=tree_results.yview)
        tree_results.configure(yscroll=scroll_results.set)
        scroll_results.grid(row=0, column=1, sticky="ns")

        for song in songs:
            tree_results.insert("", "end", values=(song.track_name, song.artist_name))

        button_add = ttk.Button(result_window, text="Agregar a la Playlist", command=lambda: self.agregar_cancion(tree_results, songs, result_window))
        button_add.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    def agregar_cancion(self, tree, songs, window):
        selected_item = tree.selection()
        if selected_item:
            item = tree.item(selected_item)
            track_name = item['values'][0]
            song = next(song for song in songs if song.track_name == track_name)
            self.playlist_manager.agregar_cancion(song)
            self.actualizar_playlist()
            window.destroy()
            messagebox.showinfo("Éxito", f"Se agregó la canción: {song.track_name} by {song.artist_name}")
        else:
            messagebox.showwarning("Selección Inválida", "Por favor seleccione una canción para agregar.")

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
        attribute = simpledialog.askstring("Ordenar Playlist", "Seleccione el atributo (popularidad, año, duración):")
        if attribute not in ["popularidad", "año", "duración"]:
            messagebox.showerror("Error", "Atributo inválido.")
            return
        ordered_songs = self.playlist_manager.ordenar_playlist(attribute)
        self.actualizar_playlist(ordered_songs)

    def actualizar_playlist(self, songs=None):
        for item in self.tree_playlist.get_children():
            self.tree_playlist.delete(item)
        songs = songs or [self.playlist_manager.hashmap.get(key) for key in self.playlist_manager.hashmap.get_all_keys()]
        for song in songs:
            self.tree_playlist.insert("", "end", values=(song.track_name, song.artist_name))

