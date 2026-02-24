from enum import Enum
from htmlnode import HTMLNode, LeafNode

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other):
        if self.text == other.text and self.text_type == other.text_type and self.url == other.url:
            return True
        else:
            return False

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"

    def text_node_to_html_node(text_node):
        if text_node.text_type.value == "text":
            conv = LeafNode(None, text_node.text, None)
            return conv
        if text_node.text_type.value == "bold":
            conv = LeafNode("b", text_node.text, None)
            return conv
        if text_node.text_type.value == "italic":
            conv = LeafNode("i", text_node.text, None)
            return conv
        if text_node.text_type.value == "code":
            conv = LeafNode("code", text_node.text, None)
            return conv
        if text_node.text_type.value == "link":
            conv = LeafNode("a", text_node.text, {"href": ""})
            return conv
        if text_node.text_type.value == "image":
            conv = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
            return conv
