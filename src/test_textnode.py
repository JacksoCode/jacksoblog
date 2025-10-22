import unittest


from textnode import TextNode, TextType, text_node_to_html_node


from splitter import (
    split_nodes_delimiter,
    split_nodes_images,
    split_nodes_link,
    text_to_textnode,
)

from regex_extractor import extract_markdown_images, extract_markdown_links

from markdowntoblocks import block_to_block_type, markdown_to_blocks, BlockType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("this is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_not_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.BOLD, "https://www.google.com")
        self.assertNotEqual(node, node2)

    # text node to html node test
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        node = TextNode("This is a bold node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold node")

    def test_italic(self):
        node = TextNode("This is an italic node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic node")

    def test_img(self):
        node = TextNode("a cute bear", TextType.IMAGES, url="https://img/bear.png")
        html = text_node_to_html_node(node)
        self.assertEqual(html.tag, "img")
        self.assertEqual(html.value, "")
        self.assertEqual(
            html.props, {"src": "https://img/bear.png", "alt": "a cute bear"}
        )

    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("code block", TextType.CODE))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

    def test_split_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0], TextNode("This is text with a ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("bold", TextType.BOLD))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

    def test_split_italic(self):
        node = TextNode("This is text with an _italic_ word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes[0], TextNode("This is text with an ", TextType.TEXT))
        self.assertEqual(new_nodes[1], TextNode("italic", TextType.ITALIC))
        self.assertEqual(new_nodes[2], TextNode(" word", TextType.TEXT))

    def test_split_not_text(self):
        node = TextNode("a bold word", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes[0], TextNode("a bold word", TextType.BOLD))

    def test_split_low_delim(self):
        with self.assertRaises(Exception):
            node = TextNode("a **bold word", TextType.TEXT)
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a ![link](https://www.boot.dev)"
        )
        self.assertListEqual([("link", "https://www.boot.dev")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_images([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGES, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGES, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINKS, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINKS, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            new_nodes,
        )

    def test_text_to_text_node_all(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnode(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_text_node_no_bold(self):
        text = "This is text with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnode(text)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_text_node_no_ital(self):
        text = "This is **text** with no italic word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnode(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with no italic word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_text_node_no_code(self):
        text = "This is **text** with an _italic_ word and no code block and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        new_nodes = text_to_textnode(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and no code block and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_text_node_no_image(self):
        text = "This is **text** with an _italic_ word and a `code block` and no obi wan image and a [link](https://boot.dev)"
        new_nodes = text_to_textnode(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and no obi wan image and a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_text_node_no_link_and_end_text(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and no link to boots."
        new_nodes = text_to_textnode(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and no link to boots.", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_text_node_image_first(self):
        text = "![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) image first then **text** with an _italic_ word and a `code block` and a [link](https://boot.dev)"
        new_nodes = text_to_textnode(text)
        self.assertListEqual(
            [
                TextNode(
                    "obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" image first then ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
            ],
            new_nodes,
        )

    def test_text_to_text_node_jumble(self):
        text = "Random order `code block` and a [link](https://boot.dev) and _italic_ text then an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) then end **boldly**!"
        new_nodes = text_to_textnode(text)
        self.assertListEqual(
            [
                TextNode("Random order ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text then an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" then end ", TextType.TEXT),
                TextNode("boldly", TextType.BOLD),
                TextNode("!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_text_node_two_images(self):
        text = "This is an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and another![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and some trailing text"
        new_nodes = text_to_textnode(text)
        self.assertListEqual(
            [
                TextNode("This is an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and another", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and some trailing text", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_text_node_jumble_with_extra_image(self):
        text = "Random order `code block` and a [link](https://boot.dev) and _italic_ text then an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and another ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) then end **boldly**!"
        new_nodes = text_to_textnode(text)
        self.assertListEqual(
            [
                TextNode("Random order ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text then an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" then end ", TextType.TEXT),
                TextNode("boldly", TextType.BOLD),
                TextNode("!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_text_to_text_node_jumble_with_extra_link(self):
        text = "Random order `code block` and a [link](https://boot.dev) and another [link](https://boot.dev) then some _italic_ text then an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) then end **boldly**!"
        new_nodes = text_to_textnode(text)
        self.assertListEqual(
            [
                TextNode("Random order ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("link", TextType.LINKS, "https://boot.dev"),
                TextNode(" then some ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text then an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGES, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" then end ", TextType.TEXT),
                TextNode("boldly", TextType.BOLD),
                TextNode("!", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_extra_indents(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items



Then here is more stuff after too many new lines
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
                "Then here is more stuff after too many new lines",
            ],
        )

    def test_markdown_to_blocks_classifiers(self):
        md = """
### This is a heading 

``` 
This is a code block beep boop 
```

This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

> This is a quote

- This is an unordered list
- with items

1. This is an ordered list
2. with items 
"""
        blocks = markdown_to_blocks(md)
        block_types = block_to_block_type(blocks)
        self.assertEqual(
            block_types,
            [
                BlockType.HEADING,
                BlockType.CODE,
                BlockType.PARAGRAGH,
                BlockType.PARAGRAGH,
                BlockType.QUOTE,
                BlockType.UNORDERED_LIST,
                BlockType.ORDERED_LIST,
            ],
        )


if __name__ == "__main__":
    unittest.main()
