from textnode import TextNode, TextType


def main():
    temp = TextNode("This is some anchor text", TextType.LINKS, "https://www.boots.dev")
    print(temp)


if __name__ == "__main__":
    main()
