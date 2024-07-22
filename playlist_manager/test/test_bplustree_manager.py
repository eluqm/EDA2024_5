import unittest
from util.bplustree_manager import BPlusTree, BPlusTreeNode

class TestBPlusTree(unittest.TestCase):
    def setUp(self):
        self.tree = BPlusTree(3)  # c crea un árbol B+ con orden 3

if __name__ == '__main__':
    unittest.main()

def test_insert_and_search(self):
    self.tree.insert(10, "value10")
    self.tree.insert(20, "value20")
    self.tree.insert(5, "value5")

    self.assertEqual(self.tree.search(10), "value10")
    self.assertEqual(self.tree.search(20), "value20")
    self.assertEqual(self.tree.search(5), "value5")
    self.assertIsNone(self.tree.search(15))