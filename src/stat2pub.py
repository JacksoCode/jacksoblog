import os
import shutil


def stat_to_pub(source, destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
        print()
        print("Old directory", destination, "deleted..")
        print()
        print("|||||||||||||||||||||||||||||||||||||||")
    os.mkdir(destination)
    print()
    print("New directory", destination, "created...")
    print()
    print("|||||||||||||||||||||||||||||||||||||||")
    copy_stat_contents(os.path.abspath(source), os.path.abspath(destination))
    print()
    print("=================")
    print("Copying complete!")
    print("=================")
    return "place holder string"


def copy_stat_contents(source, destination):
    source_list = os.listdir(source)

    for file in source_list:
        source_file = os.path.join(source, file)
        relative_path = os.path.relpath(source_file, source)
        destination_file = os.path.join(destination, relative_path)
        if not os.path.isfile(source_file):
            os.mkdir(destination_file)
            copy_stat_contents(source_file, destination_file)
            print()
            print("Directory", file, "added to", os.path.relpath(destination), "...")
            print()
            print("|||||||||||||||||||||||||||||||||||||||")
        else:
            shutil.copy(source_file, destination_file)
            print()
            print("Copying from", file, "to", os.path.relpath(destination), "...")
            print()
            print("|||||||||||||||||||||||||||||||||||||||")
