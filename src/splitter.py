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
        if "![" not in node.text:
            new_nodes.append(node)
        else:
            buffer_nodes = []
            image_extr = extract_markdown_images(node.text)
            split_text = re.split(r"!\[.*?\]\(.*?\)", node.text)
            filter_split = list(filter(None, split_text))
            for i in range(len(image_extr)):
                buffer_nodes.append(TextNode(filter_split[i], TextType.TEXT))
                buffer_nodes.append(
                    TextNode(image_extr[i][0], TextType.IMAGES, image_extr[i][1])
                )
            new_nodes.extend(buffer_nodes)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if "https:" not in node.text:
            new_nodes.append(node)
        else:
            buffer_nodes = []
            link_extr = extract_markdown_links(node.text)
            split_text = re.split(r"\[.*?\]\(.*?\)", node.text)
            filter_split = list(filter(None, split_text))
            for i in range(len(link_extr)):
                buffer_nodes.append(TextNode(filter_split[i], TextType.TEXT))
                buffer_nodes.append(
                    TextNode(link_extr[i][0], TextType.LINKS, link_extr[i][1])
                )
            new_nodes.extend(buffer_nodes)
    return new_nodes
