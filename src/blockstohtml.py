from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from splitter import text_to_textnode
from markdowntoblocks import BlockType, markdown_to_blocks, block_to_block_type


def text_to_children(text):
    text_node = text_to_textnode(text)
    html_nodes = []
    for node in text_node:
        new_nodes = text_node_to_html_node(node)
        html_nodes.append(new_nodes)
    return html_nodes


def markdown_to_html_node(markdown):
    block_markdown = markdown_to_blocks(markdown)
    block_type = block_to_block_type(block_markdown)
    parent_div_node = HTMLNode(tag="div")
    children = []
    for i in range(len(block_type)):
        if block_type[i] == BlockType.HEADING:
            parts = block_markdown[i].split(" ", 1)
            hashes = parts[0]
            level = min(len(hashes), 6)
            text = parts[1].strip() if len(parts) > 1 else ""
            node = HTMLNode(tag=f"h{level}", children=text_to_children(text))
            children.append(node)
        elif block_type[i] == BlockType.CODE:
            lines = block_markdown[i].split("\n")
            code_text = "\n".join(lines[1:-1])
            code_textnode = TextNode(code_text, TextType.TEXT)
            code_to_htmlnode = text_node_to_html_node(code_textnode)
            code_node = HTMLNode(tag="code", children=[code_to_htmlnode])
            node = HTMLNode(tag="pre", children=[code_node])
            children.append(node)
        elif block_type[i] == BlockType.QUOTE:
            parts = block_markdown[i].split("\n")
            remove_lessthan = [
                part[2:] if part.startswith("> ") else part for part in parts
            ]
            text = "\n".join(remove_lessthan)
            node = HTMLNode(tag="blockquote", children=text_to_children(text))
            children.append(node)
        elif block_type[i] == BlockType.UNORDERED_LIST:
            parts = block_markdown[i].split("\n")
            remove_dash = [
                part[2:] if part.startswith("- ") else part for part in parts
            ]
            line_nodes = [
                HTMLNode(tag="li", children=text_to_children(text.strip()))
                for text in remove_dash
            ]
            node = HTMLNode(tag="ul", children=line_nodes)
            children.append(node)
        elif block_type[i] == BlockType.ORDERED_LIST:
            parts = block_markdown[i].split("\n")
            remove_dot = [part[3:] if part.index(". ") else part for part in parts]
            remmy = [rd.lstrip() for rd in remove_dot]
            print(remmy)
            line_nodes = [
                HTMLNode(tag="li", children=text_to_children(text.lstrip()))
                for text in remove_dot
            ]
            node = HTMLNode(tag="ol", children=line_nodes)
            children.append(node)
        elif block_type[i] == BlockType.PARAGRAGH:
            pass
    parent_div_node.children = children
    return parent_div_node


print(
    markdown_to_html_node(
        """
### This is a heading

```
This is a code block
beep boop
```

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

> This is a quote
> This is another quote
> And maybe another

- This is an unordered list
- with items

1. This is an ordered list
2. with items
3. yourtyht
4. and ordered
5. like hey
6. what a wondferful
7. kind 8. of day
8. where we can
9. work and play
10. together
11. not together
12. but to hether
"""
    )
)
