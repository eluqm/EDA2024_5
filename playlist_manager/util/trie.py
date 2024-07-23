# playlist_manager/util/trie.py

class TrieNode:
    def __init__(self):
        self.children = {}
        self.song_ids = []

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, song_name, song_id):
        node = self.root
        for char in song_name:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.song_ids.append(song_id)

    def search(self, song_name):
        node = self.root
        for char in song_name:
            if char not in node.children:
                return []
            node = node.children[char]
        return node.song_ids

    def starts_with(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._collect_all_ids(node)

    def _collect_all_ids(self, node):
        ids = []
        if node.song_ids:
            ids.extend(node.song_ids)
        for child in node.children.values():
            ids.extend(self._collect_all_ids(child))
        return ids
    
    def delete(self, song_name, song_id):
            def _delete(node, song_name, depth):
                if depth == len(song_name):
                    if song_id in node.song_ids:
                        node.song_ids.remove(song_id)
                    return len(node.song_ids) == 0 and len(node.children) == 0
                char = song_name[depth]
                if char in node.children and _delete(node.children[char], song_name, depth + 1):
                    del node.children[char]
                    return len(node.song_ids) == 0 and len(node.children) == 0
                return False

            _delete(self.root, song_name, 0)