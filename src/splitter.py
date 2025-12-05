from textnode import TextNode, TextType
import re
from regex_extractor import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif len(node.text.split(delimiter)) % 2 == 0:
            raise ValueError("Invalid markdown syntax")
        else:
            node_split = node.text.split(delimiter)
            buffer_nodes = []
            for i in range(len(node_split)):
                if node_split[i] == "":
                    continue
                if i % 2 == 0:
                    buffer_nodes.append(TextNode(node_split[i], TextType.TEXT))
                else:
                    buffer_nodes.append(TextNode(node_split[i], text_type))
            new_nodes.extend(buffer_nodes)
    return new_nodes


def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        image_extr = extract_markdown_images(node.text)
        if not image_extr:
            new_nodes.append(node)
        else:
            buffer_nodes = []
            image_extr = extract_markdown_images(node.text)
            split_text = re.split(r"!\[.*?\]\(.*?\)", node.text)
            for i in range(len(image_extr)):
                buffer_nodes.append(TextNode(split_text[i], TextType.TEXT))
                buffer_nodes.append(
                    TextNode(image_extr[i][0], TextType.IMAGES, image_extr[i][1])
                )
            buffer_nodes.append(TextNode(split_text[-1], TextType.TEXT))
            filter_buffer = [item for item in buffer_nodes if item.text != ""]
            new_nodes.extend(filter_buffer)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        link_extr = extract_markdown_links(node.text)
        if not link_extr:
            new_nodes.append(node)
        else:
            buffer_nodes = []
            split_text = re.split(r"\[.*?\]\(.*?\)", node.text)
            for i in range(len(link_extr)):
                buffer_nodes.append(TextNode(split_text[i], TextType.TEXT))
                buffer_nodes.append(
                    TextNode(link_extr[i][0], TextType.LINKS, link_extr[i][1])
                )
            buffer_nodes.append(TextNode(split_text[-1], TextType.TEXT))
            filter_buffer = [item for item in buffer_nodes if item.text != ""]
            new_nodes.extend(filter_buffer)
    return new_nodes


def text_to_textnode(text):
    new_nodes = []
    old_text = TextNode(text, TextType.TEXT)
    bold_check = split_nodes_delimiter([old_text], "**", TextType.BOLD)
    italic_check = split_nodes_delimiter(bold_check, "_", TextType.ITALIC)
    code_check = split_nodes_delimiter(italic_check, "`", TextType.CODE)
    image_check = split_nodes_images(code_check)
    link_check = split_nodes_link(image_check)
    new_nodes.extend(link_check)
    return new_nodes
