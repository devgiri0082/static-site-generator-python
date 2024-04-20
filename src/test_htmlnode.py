import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        htmlnode = HTMLNode(tag="p", value="Hello world", props={"href": "https://www.google.com",
            "target": "_blank"})
        self.assertEqual('href="https://www.google.com" target="_blank"', htmlnode.props_to_html())
    def test_repr(self):
        child_node = HTMLNode(tag="h", value="I am a child node")
        htmlnode = HTMLNode(tag="p", value="Hello world",  children=[child_node], props={"href": "https://www.google.com",
                    "target": "_blank"})
        # print(htmlnode)
    def test_leaf_node(self):
        leaf1 = LeafNode("p", "This is a paragraph of text.")
        leaf2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual("<p>This is a paragraph of text.</p>", leaf1.to_html())
        self.assertEqual('<a href="https://www.google.com">Click me!</a>', leaf2.to_html())

    def test_parent_node(self):
        parent_node_1 = ParentNode(tag= "p", children=[
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ])
        parent_node_2 = ParentNode(tag= "p", children=[
            LeafNode("b", "Bold text"),
            ParentNode("p", children=[
                LeafNode(None, "Hello from Nesting"),
                LeafNode("b", "Dev")
            ]),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ])
        self.assertEqual("<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>", parent_node_1.to_html())
        # print(parent_node_2.to_html())
        self.assertEqual("<p><b>Bold text</b><p>Hello from Nesting<b>Dev</b></p><i>italic text</i>Normal text</p>", parent_node_2.to_html())

if __name__ == "__main__":
    unittest.main()
