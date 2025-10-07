from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        count_delim = node.text.count(delimiter)
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        elif count_delim < 2:
            raise Exception("Invalid Markdown syntax")
        else:
            node_split = node.text.split(delimiter)
            new_nodes.append(TextNode(node_split[0], TextType.TEXT))
            new_nodes.append(TextNode(node_split[1], text_type))
            new_nodes.append(TextNode(node_split[2], TextType.TEXT))
    return new_nodes
