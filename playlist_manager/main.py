import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from util.playlist_manager import PlaylistManager
from util.gui_manager import GUIManager

if __name__ == "__main__":
    root = tk.Tk()
    file_path = 'data/spotify_data.csv'
    playlist_manager = PlaylistManager(3, file_path)
    gui_manager = GUIManager(root, playlist_manager)
    root.mainloop()