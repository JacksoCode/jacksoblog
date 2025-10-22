from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from markdowntoblocks import BlockType, markdown_to_blocks, block_to_block_type


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING:
            pass
        if block_type == BlockType.CODE:
            pass
        if block_type == BlockType.QUOTE:
            pass
        if block_type == BlockType.UNORDERED_LIST:
            pass
        if block_type == BlockType.ORDERED_LIST:
            pass
        if block_type == BlockType.PARAGRAGH:
            pass
