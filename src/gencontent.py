import os
from pathlib import Path
from blockstohtml import markdown_to_html_node


def extract_title(markdown):
    split_m = markdown.split("\n\n")
    for s in split_m:
        h1 = s.strip("\n")
        if h1.startswith("# "):
            no_hash = h1.replace("#", "")
            return "".join(no_hash.strip())
    raise Exception("No valid header found")


def generate_page(from_path, template_path, dest_path, basepath):
    print()
    print(f"Generating page from {from_path} to {dest_path} using {template_path}...")
    print()
    print("|||||||||||||||||||||||||||||||||||||||")

    from_file = open(from_path)
    from_contents = from_file.read()
    from_file.close()

    template_file = open(template_path)
    template_contents = template_file.read()
    template_file.close()

    title = extract_title(from_contents)
    node = markdown_to_html_node(from_contents)
    html = node.to_html()

    template_contents = template_contents.replace("{{ Title }}", title)
    template_contents = template_contents.replace("{{ Content }}", html)
    template_contents = template_contents.replace('href="/', f'href="{basepath}')
    template_contents = template_contents.replace('src="/', f'src="{basepath}')

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    to_file = open(dest_path, "w")
    to_file.write(template_contents)
    to_file.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    source = os.listdir(dir_path_content)
    relative_path = Path(dir_path_content)
    destination_path = Path(dest_dir_path)

    for file in source:
        file_path = relative_path / file
        new_path = destination_path / file
        if not os.path.isfile(file_path):
            generate_pages_recursive(file_path, template_path, new_path, basepath)
        else:
            generate_page(
                file_path, template_path, new_path.with_suffix(".html"), basepath
            )
