from typing import List
import unittest

from textnode import TextNode, TextTypes
from utils import BlockType, Utils

class TestUtils(unittest.TestCase):
    def test_text_node_to_html(self):
        text_text_node = TextNode(text="Hello world", type=TextTypes.TEXT, url=None)
        bold_text_node = TextNode(text="Hello world", type=TextTypes.BOLD, url=None)
        itlics_text_node = TextNode(text="Hello world", type=TextTypes.ITALIC, url=None)
        image_text_node = TextNode(text="Hello world", type=TextTypes.IMAGE, url="www.google.com/this-is-a-image")
        code_text_node = TextNode(text="Hello world", type=TextTypes.CODE, url=None)
        link_text_node = TextNode(text="Hello world", type=TextTypes.LINK, url="www.link.com")

        text_html_node = Utils.text_node_to_html_node(text_text_node)
        bold_html_node = Utils.text_node_to_html_node(bold_text_node)
        itlics_html_node = Utils.text_node_to_html_node(itlics_text_node)
        image_html_node = Utils.text_node_to_html_node(image_text_node)
        link_html_node = Utils.text_node_to_html_node(link_text_node)

        # print(text_html_node)
        # print(bold_html_node)
        # print(itlics_html_node)
        # print(image_html_node)
        # print(link_html_node)


    def test_split_node_delimiters(self):
        node = TextNode(". Hello \n . world", TextTypes.TEXT)
        new_nodes = Utils.split_nodes_delimiter([node], "**", TextTypes.BOLD)
        for node in new_nodes:
            print(node)

    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected_result =  [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        self.assertEqual(expected_result, Utils.extract_markdown_images(text))

    def test_extract_markdown_link(self):
        text = "[Back Home](/)"
        expected_result =  [("Back Home", "/")]
        self.assertEqual(expected_result,Utils.extract_markdown_links(text))

    def test_split_nodes_images(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            TextTypes.TEXT,
        )
        new_nodes = Utils.split_nodes_images([node])
        # for node in new_nodes:
        #     print(node)

    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another link [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png), howdy",
            TextTypes.TEXT,
        )
        new_nodes = Utils.split_nodes_links([node])
        # for node in new_nodes:
        #     print(node)

    def test_text_to_textnodes(self):
        text = ". First item\n. Second item\n. Third item"

        final = Utils.text_to_textnodes(text)
        # print("TEXT_TO_TEXTNODES")
        # for node in final:
        #     print(node)

    def test_markdown_to_blocks(self):
        markdown = 'This is **bolded** paragraph\n\nThis is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line\n\n* This is a list\n* with items'
        result = Utils.markdown_to_blocks(markdown)
        expected_result = [
            "This is **bolded** paragraph",
            "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
            "* This is a list\n* with items"
        ]
        # print("result: ", result)
        self.assertEqual(result, expected_result)

    def block_to_block_type(self):
       quote_block = '```Hello world```'
       unordered_list_block = "* Hello \n* world"
       expected_quote_type = BlockType.QUOTE
       expected_list_type = BlockType.UNORDERED_LIST
       self.assertEqual(Utils.block_to_block_type(quote_block), expected_quote_type)
       self.assertEqual(Utils.block_to_block_type(unordered_list_block), expected_list_type)


    def test_block_to_html_node(self):
        quote_block = '```Hello world```'
        unordered_list_block = "1. Hello\n2. world"
        # quote_html_node = Utils.block_to_html_node(block=quote_block, block_type=BlockType.QUOTE)
        ordered_list_node = Utils.block_to_html_node(block=unordered_list_block, block_type=BlockType.ORDERED_LIST)
        print(ordered_list_node)

    def test_markdown_to_html_node(self):
        markdown = "![LOTR image artistmonkeys](/images/rivendell.png)"
        res = Utils.markdown_to_html_node(markdown=markdown)
        content = res.to_html()
        # print(content)

    def test_extract_title(self):
        markdown = "# The Unparalleled Majesty of \"The Lord of the Rings\"\n\n[Back Home](/)"
        expected_res = "Example Markdown File"
        # self.assertEqual(Utils.extract_title(markdown=markdown), expected_res)
