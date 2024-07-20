import tkinter as tk
from util.playlist_manager import PlaylistManager
from util.gui_manager import GUIManager

def main():
    root = tk.Tk()
    file_path = 'data/spotify_data.csv'  # Asegúrate de que esta ruta sea correcta
    bplustree_order = 3  # Ajusta el orden del B+ tree según sea necesario

    # Crear instancia de PlaylistManager con el orden del B+ tree y la ruta del archivo CSV
    playlist_manager = PlaylistManager(bplustree_order, file_path)

    # Crear instancia de GUIManager con la ventana principal y el PlaylistManager
    gui_manager = GUIManager(root, playlist_manager)

    # Iniciar el bucle principal de Tkinter
    root.mainloop()

if __name__ == "__main__":
    main()
