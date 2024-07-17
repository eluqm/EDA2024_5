# playlist_manager/util/bplustree_manager.py

class BPlusTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t  # Grado mínimo (t) del B++ Tree
        self.leaf = leaf  # Verifica si es un nodo hoja
        self.keys = []  # Lista de claves
        self.children = []  # Lista de hijos
        self.next = None  # Apunta al siguiente nodo hoja

class BPlusTree:
    def __init__(self, t):
        self.root = BPlusTreeNode(t, True)
        self.t = t

    def insert(self, key, value):
        root = self.root
        if len(root.keys) == 2 * self.t - 1:

