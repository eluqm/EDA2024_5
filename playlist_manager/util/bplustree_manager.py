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
            temp = BPlusTreeNode(self.t)
            self.root = temp
            temp.children.append(root)
            self._split_child(temp, 0)
            self._insert_non_full(temp, key, value)
        else:
            self._insert_non_full(root, key, value)
    
    def _split_child(self, parent, index):
        t = self.t
        node = parent.children[index]
        new_node = BPlusTreeNode(t, node.leaf)
        parent.children.insert(index + 1, new_node)
        parent.keys.insert(index, node.keys[t-1])
        new_node.keys = node.keys[t:(2*t-1)]
        node.keys = node.keys[0:(t-1)]

        if not node.leaf:
            new_node.children = node.children[t:(2*t)]
            node.children = node.children[0:(t-1)]
        else:
            new_node.next = node.next
            node.next = new_node
    

    def _insert_non_full(self, node, key, value):
        if node.leaf:
            index = len(node.keys) - 1
            node.keys.append((None, None))
            while index >= 0 and key < node.keys[index][0]:
                node.keys[index + 1] = node.keys[index]
                index -= 1
            node.keys[index + 1] = (key, value)
        else:
            index = len(node.keys) - 1
            while index >= 0 and key < node.keys[index]:
                index -= 1
            index += 1
            if len(node.children[index].keys) == 2 * self.t - 1:
                self._split_child(node, index)
                if key > node.keys[index]:
                    index += 1
            self._insert_non_full(node.children[index], key, value)

    def search(self, key):
        return self._search(self.root, key)
        
    def _search(self, node, key):
        index = 0
        while index < len(node.keys) and key > node.keys[index][0]:
            index += 1
        if index < len(node.keys) and key == node.keys[index][0]:
            return node.keys[index][1]
        if node.leaf:
            return None
        return self._search(node.children[index], key)

