from argparse import _HelpAction
from enum import Enum
from typing import List, Tuple

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextTypes

import re

delemeter_to_text_type = {
    TextTypes.CODE : '`',
    TextTypes.BOLD : '**',
    TextTypes.ITALIC: "*",
}

class BlockType(Enum):
   PARAGRAPH="paragraph",
   HEADING = "heading",
   CODE = "code",
   QUOTE = "quote",
   UNORDERED_LIST= "unordered_list"
   ORDERED_LIST = "ordered_list"
class Utils:
    @staticmethod
    def text_node_to_html_node(text_node: TextNode):
        node: LeafNode
        if text_node.text_type == TextTypes.TEXT:
            node = LeafNode(tag=None, value=text_node.text, props=None)
        elif text_node.text_type == TextTypes.BOLD:
            node = LeafNode(tag="b", value=text_node.text, props=None)
        elif text_node.text_type == TextTypes.ITALIC:
            node = LeafNode(tag="i", value = text_node.text, props = None)
        elif text_node.text_type == TextTypes.CODE:
            node = LeafNode(tag="code", value = text_node.text, props=None)
        elif text_node.text_type == TextTypes.LINK:
            node = LeafNode(tag="a", value = text_node.text, props = {"href": text_node.url})
        elif text_node.text_type == TextTypes.IMAGE:
            node = LeafNode(tag="img", value="", props={"src": text_node.url, "alt": text_node.text})
        else:
            raise Exception("Invalid text_type")
        return node

    @staticmethod
    def split_nodes_delimiter(old_nodes:List[TextNode], delimiter:str, text_type:TextTypes) -> List[TextNode]:
        final_nodes: List[TextNode] = []
        for node in old_nodes:
            if node.text_type != TextTypes.TEXT:
                final_nodes.append(node)
                continue
            split_text =node.text.split(delimiter)
            if len(split_text) == 1:
                return [TextNode(text=split_text[0], type=TextTypes.TEXT)]
            for index in range(0, len(split_text)):
                if split_text[index] == "":
                    continue
                if index % 2 == 0:
                    final_nodes.append(TextNode(text=split_text[index], type=TextTypes.TEXT))
                elif index % 2 ==1:
                    final_nodes.append(TextNode(text=split_text[index], type=text_type))
        return final_nodes

    @staticmethod
    def  extract_markdown_images(text: str) -> List[Tuple[str, str]]:
        return re.findall(r"!\[(.*?)\]\((.*?)\)", text)

    @staticmethod
    def extract_markdown_links(text: str) -> List[Tuple[str, str]]:
        return re.findall(r"\[(.*?)\]\((.*?)\)", text)

    @staticmethod
    def split_nodes_images(nodes: List[TextNode]) -> List[TextNode]:
        final_nodes: List[TextNode] = []
        for node in nodes:
            if node.text_type != TextTypes.TEXT:
                final_nodes.append(node)
                continue
            texts = node.text
            images = Utils.extract_markdown_images(texts)
            for alt, link  in images:
                img_tag = f"![{alt}]({link})"
                pos =  texts.find(img_tag)
                pre = texts[0: pos]
                image = texts[pos:pos + len(img_tag)]
                post = texts[pos + len(img_tag):]
                if pre != "":
                    final_nodes.append(TextNode(text=pre, type=TextTypes.TEXT))
                final_nodes.append(TextNode(text=alt, type=TextTypes.IMAGE, url=link))
                texts = post

            if texts != "":
                final_nodes.append(TextNode(text=texts, type=TextTypes.TEXT))
        return final_nodes

    @staticmethod
    def split_nodes_links(nodes: List[TextNode]) -> List[TextNode]:
         final_nodes: List[TextNode] = []
         for node in nodes:
             if node.text_type != TextTypes.TEXT:
                 final_nodes.append(node)
                 continue
             texts = node.text
             links = Utils.extract_markdown_links(texts)
             for text, link  in links:
                img_tag = f"[{text}]({link})"
                pos =  texts.find(img_tag)
                pre = texts[0: pos]
                image = texts[pos:pos + len(img_tag)]
                post = texts[pos + len(img_tag):]
                if pre != "":
                    final_nodes.append(TextNode(text=pre, type=TextTypes.TEXT))
                final_nodes.append(TextNode(text=text, type=TextTypes.LINK, url=link))
                texts = post

             if texts != "":
                 final_nodes.append(TextNode(text=texts, type=TextTypes.TEXT))
         return final_nodes

    @staticmethod
    def text_to_textnodes(text):
        bold_nodes = Utils.split_nodes_delimiter(old_nodes=[TextNode(text=text, type=TextTypes.TEXT)], delimiter='**', text_type=TextTypes.BOLD)
        italic_nodes = Utils.split_nodes_delimiter(old_nodes= bold_nodes, delimiter='*', text_type=TextTypes.ITALIC)
        code_nodes = Utils.split_nodes_delimiter(old_nodes=italic_nodes, delimiter="`", text_type=TextTypes.CODE)
        image_nodes = Utils.split_nodes_images(code_nodes)
        final_nodes = Utils.split_nodes_links(image_nodes)
        return final_nodes

    @staticmethod
    def markdown_to_blocks(markdown: str) -> List[str]:
        block = f""
        final: List[str] = []
        markdown_lines = markdown.split("\n")
        for line in markdown.split("\n"):
            if line == "":
                if block != "":
                    final.append(block)
                block = f""
                continue
            line.strip(" ")
            if block != "":
                block += "\n"
            block += f"{line}"
        if block != "":
            final.append(block)
        return final

    @staticmethod
    def block_to_block_type(block: str) -> BlockType:
        block_lines = block.split("\n")
        if re.search(r'^#{1,6} .*', block) != None:
            return BlockType.HEADING
        if re.search(r'^```.*```$', block) != None:
            return BlockType.CODE
        if len(list(filter(lambda x: x[0] != ">", block_lines))) == 0:
            return BlockType.QUOTE
        if len(list(filter(lambda x: (x[0] != "*" and x[0] != "-") or x[1] != " ", block_lines))) == 0:
            return BlockType.UNORDERED_LIST
        filtered = list(filter(lambda x: len(re.findall(r"^[0-9]+\. .*", x)) > 0, block_lines))
        if len(filtered) == len(block_lines):
            return BlockType.ORDERED_LIST
        return BlockType.PARAGRAPH

    @staticmethod
    def block_to_html_node(block: str, block_type: BlockType) -> HTMLNode:
        if block_type == BlockType.HEADING:
            result = re.findall(r'(^#{1,6}) (.*)', block)
            tag: str = f"h{len(result[0][0])}"
            return LeafNode(tag=tag, value=result[0][1])
        elif block_type == BlockType.CODE:
           result =  re.findall(r'^```(.*)```$', block)
           return ParentNode(tag="pre",children=[LeafNode(tag="code", value=result[0][0])])
        elif block_type == BlockType.QUOTE:
           value =  "\n".join(map(lambda x: x[1:] ,block.split("\n")))
           return LeafNode(tag="blockquote", value=value)
        elif block_type == BlockType.UNORDERED_LIST:
            children = list(map(lambda x: LeafNode(tag="li", value=x[2:]),block.split("\n")))
            return ParentNode(tag="ul", children=children)
        elif block_type == BlockType.ORDERED_LIST:
            children = list(map(lambda x: LeafNode(tag="li", value=re.findall(r"^[0-9]\. (.*)", x)[0]),block.split("\n")))
            return ParentNode(tag="ol", children=children)
        else:
            return LeafNode(tag="p", value=block)

    @staticmethod
    def markdown_to_html_node(markdown: str) -> ParentNode:
        block_elems: List[HTMLNode] = []
        final_elems: List[HTMLNode] = []
        blocks = Utils.markdown_to_blocks(markdown=markdown)
        for block in blocks:
            block_type = Utils.block_to_block_type(block)
            html_node = Utils.block_to_html_node(block=block, block_type=block_type)
            block_elems.append(html_node)
        for block in block_elems:
            if block.tag != "p":
                final_elems.append(block)
            else:
                inline_elems = Utils.text_to_textnodes(block.value)
                html_inline_nodes: List[HTMLNode] =[]
                for elem in inline_elems:
                    node = Utils.text_node_to_html_node(elem)
                    html_inline_nodes.append(node)
                final_elems.append(ParentNode(tag="p", children=html_inline_nodes))
        return ParentNode(tag="div", children=final_elems)

    @staticmethod
    def extract_title(markdown: str) -> str:
        lines = markdown.split("\n")
        for line in lines:
            result = re.findall(r'^# (.*)', line)
            if len(result) > 0:
                return result[0]
        raise Exception("All pages need a single h1 header")
