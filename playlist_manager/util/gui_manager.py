import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from PIL import Image, ImageTk
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

        self.album_frame = ttk.Frame(self.root)
        self.album_frame.pack(pady=20)

        # Usar PIL para cargar y convertir la imagen
        self.album_cover_image = Image.open('img/album_cover.jpg')  # Ruta actualizada
        self.album_cover_image = self.album_cover_image.resize((300, 300), Image.ANTIALIAS)
        self.album_cover_photo = ImageTk.PhotoImage(self.album_cover_image)
        self.album_cover = tk.Label(self.album_frame, image=self.album_cover_photo, bg='black')
        self.album_cover.pack()

        self.album_title = tk.Label(self.root, text="Album Title", fg='white', bg='black', font=("Helvetica", 16))
        self.album_title.pack()

        self.add_button = tk.Button(self.root, text="Agregar Canción", command=self.agregar_cancion, bg='green', fg='white')
        self.add_button.pack(pady=10)

        self.songs_frame = ttk.Frame(self.root)
        self.songs_frame.pack(fill="both", expand=True)

        self.songs_list = tk.Listbox(self.songs_frame, bg='black', fg='white')
        self.songs_list.pack(side="left", fill="both", expand=True)

        self.scrollbar = ttk.Scrollbar(self.songs_frame)
        self.scrollbar.pack(side="right", fill="y")

        self.songs_list.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.songs_list.yview)

        self.delete_button = tk.Button(self.root, text="Eliminar Canción", command=self.eliminar_cancion, bg='red', fg='white')
        self.delete_button.pack(pady=10)

        self.order_button = tk.Button(self.root, text="Ordenar Playlist", command=self.ordenar_playlist, bg='blue', fg='white')
        self.order_button.pack(pady=10)

    def agregar_cancion(self):
        song_name = simpledialog.askstring("Agregar Canción", "Ingrese el nombre de la canción:")
        if song_name:
            songs = self.playlist_manager.file_manager.search_songs_by_name(song_name)
            if songs:
                song = songs[0]
                self.playlist_manager.agregar_cancion(song)
                self.songs_list.insert("end", f"{song.track_name} - {song.artist_name}")
                messagebox.showinfo("Éxito", f"Se agregó la canción: {song.track_name}")
            else:
                messagebox.showwarning("Sin Resultados", "No se encontraron canciones con ese nombre.")

    def eliminar_cancion(self):
        selected_index = self.songs_list.curselection()
        if selected_index:
            song_name = self.songs_list.get(selected_index)
            self.songs_list.delete(selected_index)
            song_id = self.playlist_manager.hashmap.get_key_by_value(song_name.split(" - ")[0])
            self.playlist_manager.eliminar_cancion(song_id)
            messagebox.showinfo("Éxito", f"Se eliminó la canción: {song_name}")
        else:
            messagebox.showwarning("Selección Inválida", "Por favor seleccione una canción para eliminar.")

    def ordenar_playlist(self):
        attribute = simpledialog.askstring("Ordenar Playlist", "Seleccione el atributo (popularidad, año, duración):")
        if attribute not in ["popularidad", "año", "duración"]:
            messagebox.showerror("Error", "Atributo inválido.")
            return
        ordered_songs = self.playlist_manager.ordenar_playlist(attribute)
        self.songs_list.delete(0, "end")
        for song in ordered_songs:
            self.songs_list.insert("end", f"{song.track_name} - {song.artist_name}")

if __name__ == "__main__":
    root = tk.Tk()
    file_path = 'data/spotify_data.csv'
    bplustree_order = 3
    playlist_manager = PlaylistManager(bplustree_order, file_path)
    gui_manager = GUIManager(root, playlist_manager)
    root.mainloop()
