import os

def list_directory(path='.', show_all=False, recursive=False):
    """
    Lists the contents of a directory with optional flags.

    :param path: Directory path to list.
    :param show_all: Whether to include hidden files.
    :param recursive: Whether to list directories recursively.
    :return: List of directory contents.
    """
    result = []
    if recursive:
        for root, dirs, files in os.walk(path):
            entries = dirs + files if show_all else [entry for entry in dirs + files if not entry.startswith('.')]
            result.append({"path": root, "entries": entries})
    else:
        entries = os.listdir(path)
        if not show_all:
            entries = [entry for entry in entries if not entry.startswith('.')]
        result.append({"path": path, "entries": entries})
    return result
