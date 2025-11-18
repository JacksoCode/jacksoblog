import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

from blockstohtml import markdown_to_html_node


class TestHTMLNode(unittest.TestCase):
    # Test for HTMLNode
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

    # Test for LeafNode

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode(
            tag="a", value="whats a link", props={"href": "https://boot.dev"}
        )
        self.assertEqual(node.to_html(), '<a href="https://boot.dev">whats a link</a>')

    def test_leaf_to_html_b(self):
        node = LeafNode("b", "Bold me baby!")
        self.assertEqual(node.to_html(), "<b>Bold me baby!</b>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(tag=None, value="Maidenless AND tagless... pathetic")
        self.assertEqual(node.to_html(), "Maidenless AND tagless... pathetic")

    # Test for ParentNode

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_children_with_link(self):
        child_node = LeafNode("b", "child")
        parent_node = ParentNode("a", [child_node], {"href": "https://boot.dev"})
        self.assertEqual(
            parent_node.to_html(), '<a href="https://boot.dev"><b>child</b></a>'
        )

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_grandchildren_with_link(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        grand_parent_node = ParentNode("a", [parent_node], {"href": "https://boot.dev"})
        self.assertEqual(
            grand_parent_node.to_html(),
            '<a href="https://boot.dev"><div><span><b>grandchild</b></span></div></a>',
        )

    def test_to_html_with_no_children(self):
        with self.assertRaisesRegex(ValueError, "invalid HTML: no children"):
            no_child_node = ParentNode("b", children=None)
            no_child_node.to_html()

    def test_to_html_with_no_tag(self):
        with self.assertRaisesRegex(ValueError, "invalid HTML: no tag"):
            no_tag_node = ParentNode(tag=None, children="tagless")
            no_tag_node.to_html()

    def test_to_html_with_granchildren_no_chld(self):
        with self.assertRaisesRegex(ValueError, "invalid HTML: no tag"):
            grandchild_node = LeafNode("b", "grandchild")
            no_tag_child_node = ParentNode(None, [grandchild_node])
            parent_node = ParentNode("b", [no_tag_child_node])
            parent_node.to_html()

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )
