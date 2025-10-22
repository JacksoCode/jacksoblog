from markdowntoblocks import BlockType, markdown_to_blocks, block_to_block_type


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to_html mehtod not implemented")

    def props_to_html(self):
        if not self.props:
            return ""
        parts = []
        for key in sorted(self.props.keys()):
            value = self.props[key]
            parts.append(f'{key}="{str(value)}"')
        return (" " + " ".join(parts)) if parts else ""

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return NotImplemented
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.props == other.props
            and self.children == other.children
        )

    def __repr__(self):
        child_tags = []
        if self.children:
            child_tags = [c.tag for c in self.children[:3]]
        return (
            f"HTMLNode(tag={self.tag!r}, "
            f"value={self.value!r}, "
            f"children_count={len(self.children) if self.children else 0}, "
            f"children_preview={child_tags}, "
            f"props={self.props!r})"
        )


class LeafNode(HTMLNode):
    # tag and value are required for LeafNode
    # props remains optional
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return str(self.value)
        props_str = super().props_to_html()
        return f"<{self.tag}{props_str}>{self.value}</{self.tag}>"

    def repr(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"


class ParentNode(HTMLNode):
    # tag and children are required for ParentNode
    # props remains optional
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        props_str = super().props_to_html()
        child = None
        for c in self.children:
            child = c.to_html()
        return f"<{self.tag}{props_str}>{child}</{self.tag}>"

    def repr(self):
        return f"ParentNode({self.tag}, {self.children}, {self.props})"


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
