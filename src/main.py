from textnode import TextNode, TextType
from stat2pub import stat_to_pub


def main():
    copy = stat_to_pub()
    print(copy)


if __name__ == "__main__":
    main()
