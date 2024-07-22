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

def test_split(self):
    for i in range(10):
        self.tree.insert(i, f"value{i}")
    
    # verifica que el arbol se ha dividido
    self.assertGreater(len(self.tree.root.children), 1)
    self.assertLessEqual(len(self.tree.root.keys), 2 * self.tree.t - 1)

def test_insert_duplicate(self):
    self.tree.insert(10, "value10")
    self.tree.insert(10, "new_value10")
    self.assertEqual(self.tree.search(10), "new_value10")

def test_insert_many(self):
    for i in range(100):
        self.tree.insert(i, f"value{i}")

    for i in range(100):
        self.assertEqual(self.tree.search(i), f"value{i}")

def test_delete(self):
    for i in range(10):
        self.tree.insert(i, f"value{i}")

    self.tree.delete(5)
    self.assertIsNone(self.tree.search(5))
    self.assertEqual(self.tree.search(4), "value4")
    self.assertEqual(self.tree.search(6), "value6") 

def test_range_search(self):
    for i in range(20):
        self.tree.insert(i, f"value{i}")

    result = self.tree.range_search(5, 15)
    self.assertEqual(len(result), 11)
    self.assertEqual(result[0][0], 5)
    self.assertEqual(result[-1][0], 15)

def test_tree_structure(self):
    for i in range(20):
        self.tree.insert(i, f"value{i}")

    def check_node(node):
        if not node.leaf:
            self.assertLessEqual(len(node.keys), 2 * self.tree.t - 1)
            self.assertGreaterEqual(len(node.keys), self.tree.t - 1)
            for child in node.children:
                check_node(child)
        else:
            self.assertLessEqual(len(node.keys), 2 * self.tree.t - 1)

    check_node(self.tree.root)

def test_empty_tree(self):
    self.assertIsNone(self.tree.search(10))
    self.assertEqual(self.tree.range_search(0, 10), [])