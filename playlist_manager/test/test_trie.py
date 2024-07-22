# playlist_manager/tests/test_trie.py
TrieTest
# playlist_manager/tests/test_trie.py

import unittest
from util.trie import Trie

class TestTrie(unittest.TestCase):
    def setUp(self):
        self.trie = Trie()
        self.trie.insert("song1", "id1")
        self.trie.insert("song2", "id2")
        self.trie.insert("song3", "id3")
        self.trie.insert("another_song", "id4")

    def test_search(self):
        self.assertEqual(self.trie.search("song1"), ["id1"])
        self.assertEqual(self.trie.search("song2"), ["id2"])
        self.assertEqual(self.trie.search("song3"), ["id3"])
        self.assertEqual(self.trie.search("another_song"), ["id4"])
        self.assertEqual(self.trie.search("nonexistent_song"), [])

    def test_starts_with(self):
        self.assertEqual(set(self.trie.starts_with("song")), {"id1", "id2", "id3"})
        self.assertEqual(self.trie.starts_with("another"), ["id4"])
        self.assertEqual(self.trie.starts_with("nonexistent"), [])

if _name_ == '_main_':
    unittest.main()