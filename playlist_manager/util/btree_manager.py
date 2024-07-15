# playlist_manager/util/btree_manager.py
class BTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t
        self.leaf = leaf
        self.keys = []
        self.children = []

class BTree:
    def __init__(self, t):
        self.root = BTreeNode(t, True)
        self.t = t

    # Agregar métodos de inserción, búsqueda, y división
    # Placeholder para la implementación
