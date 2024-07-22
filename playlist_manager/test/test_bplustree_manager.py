import unittest
from util.bplustree_manager import BPlusTree, BPlusTreeNode

class TestBPlusTree(unittest.TestCase):
    def setUp(self):
        self.tree = BPlusTree(3)  # Crear un árbol B+ con orden 3

if __name__ == '__main__':
    unittest.main()