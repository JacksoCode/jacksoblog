import os
from os.path import isfile
import shutil

directory = os.getcwd()


def static_to_public(content):
    to_copy = []
    files = os.listdir(content)
    for file in files:
        path = f"{content}/{file}"
        if os.path.isfile(path):
            to_copy.append(path)
        else:
            to_copy.append(path)
            to_copy.extend(static_to_public(path))
    return to_copy


print(static_to_public(f"{directory}/static"))
