from stat2pub import stat_to_pub
from gencontent import generate_page


def main():
    stat_to_pub()
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()
