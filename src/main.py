from stat2pub import stat_to_pub
from gencontent import generate_pages_recursive


def main():
    stat_to_pub()
    generate_pages_recursive("content", "template.html", "public")
    print()
    print("====================")
    print("Generation complete!")
    print("====================")


if __name__ == "__main__":
    main()
