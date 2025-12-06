from stat2pub import stat_to_pub
from gencontent import generate_pages_recursive
import sys


def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    stat_to_pub("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)
    print()
    print("====================")
    print("Generation complete!")
    print("====================")


if __name__ == "__main__":
    main()
