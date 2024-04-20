
from textnode import TextNode


class HTMLNode:
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("Not Implemented")
    def props_to_html(self) -> str:
        item = f""
        if self.props == None:
            return item
        for prop in self.props:
            item += f"{prop}=\"{self.props[prop]}\" "

        return item[:-1:]

    def __repr__(self) -> str:
        repr = f"(tag= \"{self.tag}\", value=\"{self.value}\""
        if self.children  != None:
            repr += f" children = ["
            for child in self.children:
                repr += f" {child.__repr__()}"
            repr += f"]"
        repr += f" {self.props_to_html()})"
        return repr

class LeafNode(HTMLNode):
    def __init__(self, tag = None, value = None, props = None):
        if value == None:
            raise ValueError("Value is required")
        super().__init__(tag= tag, value = value, props = props)

    def to_html(self):
        result = f""
        if self.tag != None:
            if self.props != None:
                result = f"<{self.tag} {self.props_to_html()}>"
            else:
                result = f"<{self.tag}>"

        result = f"{result}{self.value}"
        if self.tag != None:
            result = f"{result}</{self.tag}>"
        return result


class ParentNode(HTMLNode):
    def __init__(self ,tag = None, children = None, props = None):
        super().__init__(tag = tag, value = None, children=children, props=props)

    def to_html(self):
        if self.tag == None:
            raise ValueError("Tag is not provided")
        if self.children == None or len(self.children) == 0:
            raise ValueError("Children is necessary")

        result = f""
        if self.tag != None:
            result = f"<{self.tag}>"
        for child in self.children:
            result = f"{result}{child.to_html()}"

        if self.tag != None:
            result = f"{result}</{self.tag}>"
        return result
