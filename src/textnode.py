from enum import Enum
from typing import Optional


class TextTypes(Enum):
    TEXT="text",
    BOLD="bold",
    ITALIC="italic",
    CODE="code",
    LINK="link",
    IMAGE="image"
class TextNode:
  def __init__(self, text: str, type: TextTypes,  url: Optional[str] = None):
    self.text = text
    self.text_type = type
    self.url = url

  def __eq__(self, other):
    return self.text == other.text and self.text_type == other.text_type and self.url == other.url

  def __repr__(self):
    return f"TextNode(\"{self.text}\", {self.text_type}, {self.url})"
