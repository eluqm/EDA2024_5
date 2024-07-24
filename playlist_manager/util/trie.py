class TrieNode:
    def __init__(self):
        self.children = {}
        self.song_ids = []

class Trie:
    def __init__(self, prefix_length=5):
        self.root = TrieNode()
        self.prefix_length = prefix_length

    def insert(self, song_name, song_id):
        node = self.root
        for char in song_name[:self.prefix_length]:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.song_ids.append(song_id)

    def search(self, prefix):
        node = self.root
        for char in prefix[:self.prefix_length]:
            if char not in node.children:
                return []
            node = node.children[char]
        return node.song_ids

    def starts_with(self, prefix):
        node = self.root
        for char in prefix[:self.prefix_length]:
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
