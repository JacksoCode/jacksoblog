from logging import raiseExceptions


class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplemented

    def props_to_html(self):
        parts = []
        for key in sorted(self.props.key()):
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
