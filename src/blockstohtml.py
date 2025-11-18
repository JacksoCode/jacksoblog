from htmlnode import ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from splitter import text_to_textnode
from markdowntoblocks import BlockType, markdown_to_blocks, block_to_block_type


def text_to_children(text):
    text_node = text_to_textnode(text)
    return [text_node_to_html_node(tn) for tn in text_node]


def markdown_to_html_node(markdown):
    block_markdown = markdown_to_blocks(markdown)
    block_type = block_to_block_type(block_markdown)
    parent_div_node = ParentNode("div", [])
    children = []

    for i in range(len(block_type)):
        if block_type[i] == BlockType.HEADING:
            parts = block_markdown[i].split(" ", 1)
            hashes = parts[0]
            level = min(len(hashes), 6)
            text = parts[1].strip() if len(parts) > 1 else ""
            node = ParentNode(f"h{level}", text_to_children(text))
            children.append(node)

        elif block_type[i] == BlockType.CODE:
            lines = block_markdown[i].split("\n")
            code_text = "\n".join(lines[1:-1])
            if not code_text.endswith("\n"):
                code_text = code_text + "\n"
            code_textnode = TextNode(code_text, TextType.TEXT)
            code_to_htmlnode = text_node_to_html_node(code_textnode)
            code_node = ParentNode("code", [code_to_htmlnode])
            node = ParentNode("pre", [code_node])
            children.append(node)

        elif block_type[i] == BlockType.QUOTE:
            parts = block_markdown[i].split("\n")
            remove_lessthan = [
                part[2:] if part.startswith("> ") else part for part in parts
            ]
            text = "\n".join(remove_lessthan)
            node = ParentNode("blockquote", text_to_children(text))
            children.append(node)

        elif block_type[i] == BlockType.UNORDERED_LIST:
            parts = block_markdown[i].split("\n")
            remove_dash = [
                part[2:] if part.startswith("- ") else part for part in parts
            ]
            line_nodes = [
                ParentNode("li", text_to_children(text.strip())) for text in remove_dash
            ]
            node = ParentNode("ul", line_nodes)
            children.append(node)

        elif block_type[i] == BlockType.ORDERED_LIST:
            parts = block_markdown[i].split("\n")
            remove_dot = [part[3:] if part.index(". ") else part for part in parts]
            line_nodes = [
                ParentNode("li", text_to_children(text.lstrip())) for text in remove_dot
            ]
            node = ParentNode("ol", line_nodes)
            children.append(node)

        elif block_type[i] == BlockType.PARAGRAGH:
            parts = block_markdown[i].split("\n")
            text = " ".join(part.strip() for part in parts).strip()
            node = ParentNode("p", text_to_children(text))
            children.append(node)

    parent_div_node.children = children
    return parent_div_node
