import unittest

from textnode import TextNode, TextTypes
class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node1 = TextNode("This is a text node", TextTypes.BOLD)
        node2 = TextNode("This is a text node", TextTypes.BOLD)
        self.assertEqual(node1, node2)

if __name__ == "__main__":
    unittest.main()
