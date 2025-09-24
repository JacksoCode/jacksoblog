import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(value="This is plain text")
        node2 = HTMLNode(value="This is plain text")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = HTMLNode(value="This is plain text")
        node2 = HTMLNode(tag="p", value="This has an extra tag")
        self.assertNotEqual(node, node2)

    def test_eq_tag_prop(self):
        node = HTMLNode(tag="a", props={"href": "https://www.boot.dev"})
        node2 = HTMLNode(tag="a", props={"href": "https://www.boot.dev"})
        self.assertEqual(node, node2)

    def test_children(self):
        bold_children = [
            HTMLNode("Read"),
            HTMLNode("b", "carefully"),
        ]

        node = HTMLNode(tag="strong", children=bold_children)
        node2 = HTMLNode(tag="strong", children=bold_children)
        self.assertEqual(node, node2)

    def test_children_props(self):
        a_children = [
            HTMLNode(tag=None, value="The"),
            HTMLNode(tag="b", value="link"),
        ]
        node = HTMLNode(
            tag="a", children=a_children, props={"href": "https://boot.dev"}
        )
        node2 = HTMLNode(
            tag="a", children=a_children, props={"href": "https://boot.dev"}
        )
        self.assertEqual(node, node2)
