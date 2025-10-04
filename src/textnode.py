from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINKS = "link"
    IMAGES = "image"


class TextNode:
    def __init__(self, text, TextType, url=None):
        self.text = text
        self.text_type = TextType
        self.url = url

    def __eq__(self, other):
        if not isinstance(other, TextNode):
            return NotImplemented
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        return f"TextNode('{self.text}', '{self.text_type.value}', {self.url})"


def text_node_to_html_node(node):
    if node.text_type is None:
        raise Exception("HTML error: no text type passed")
    if node.text_type == TextType.TEXT:
        return LeafNode(tag=None, value=node.text)
    if node.text_type == TextType.BOLD:
        return LeafNode(tag="b", value=node.text)
    if node.text_type == TextType.ITALIC:
        return LeafNode(tag="i", value=node.text)
    if node.text_type == TextType.CODE:
        return LeafNode(tag="code", value=node.text)
    if node.text_type == TextType.LINKS:
        return LeafNode(tag="a", value=node.text, props={"href": node.url})
    if node.text_type == TextType.IMAGES:
        return LeafNode(tag="img", value="", props={"src": node.url, "alt": node.text})
