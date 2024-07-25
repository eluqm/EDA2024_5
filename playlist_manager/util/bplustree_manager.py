class BPlusTreeNode:
    def __init__(self, t, leaf=False):
        self.t = t
        self.leaf = leaf
        self.keys = []  # Tuples of (key, value)
        self.children = []
        self.next = None

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
        # Inserción del primer elemento de la segunda mitad como clave en el padre
        parent.keys.insert(index, node.keys[t - 1])

        # Dividir las llaves y los hijos
        new_node.keys = node.keys[t:]
        node.keys = node.keys[:t - 1]

        if not node.leaf:
            new_node.children = node.children[t:]
            node.children = node.children[:t]
        else:
            new_node.next = node.next
            node.next = new_node

    def _insert_non_full(self, node, key, value):
        print("Current keys in node:", node.keys)  # Verificar el contenido
        if node.leaf:
            index = len(node.keys) - 1
            node.keys.append((None, None))
            while index >= 0 and key < node.keys[index][0]:
                node.keys[index + 1] = node.keys[index]
                index -= 1
            node.keys[index + 1] = (key, value)
        else:
            index = len(node.keys) - 1
            while index >= 0 and key < node.keys[index][0]:
                index -= 1
            index += 1
            if len(node.children[index].keys) == 2 * self.t - 1:
                self._split_child(node, index)
                if key > node.keys[index][0]:
                    index += 1
            self._insert_non_full(node.children[index], key, value)

    def delete(self, key):
        def _delete(node, key):
            if node.leaf:
                for i, (k, v) in enumerate(node.keys):
                    if k == key:
                        node.keys.pop(i)
                        return True
                return False
            else:
                for i, (k, v) in enumerate(node.keys):
                    if key < k:
                        return _delete(node.children[i], key)
                return _delete(node.children[-1], key)
        
        _delete(self.root, key)

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

    def get_all_items(self):
        current = self.root
        while not current.leaf:
            current = current.children[0]

        all_items = []
        while current:
            all_items.extend(current.keys)
            current = current.next
        return all_items

    def display(self, node=None, level=0):
        if node is None:
            node = self.root
        print('Level', level, 'Keys:', node.keys)
        if not node.leaf:
            for child in node.children:
                self.display(child, level + 1)
