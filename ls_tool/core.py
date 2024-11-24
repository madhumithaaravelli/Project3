import os
import stat

def list_directory(path='.', show_all=False, recursive=False, sort_by=None):
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
            if sort_by == 'size':
                entries.sort(key=lambda x: os.path.getsize(os.path.join(root, x)))
            elif sort_by == 'mtime':
                entries.sort(key=lambda x: os.path.getmtime(os.path.join(root, x)))
            result.append({"path": root, "entries": entries})
    else:
        entries = os.listdir(path)
        if not show_all:
            entries = [entry for entry in entries if not entry.startswith('.')]
        if sort_by == 'size':
            entries.sort(key=lambda x: os.path.getsize(os.path.join(path, x)))
        elif sort_by == 'mtime':
            entries.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)))
        result.append({"path": path, "entries": entries})
    result.append({
    "path": path,
    "entries": [
        {"name": entry, "permissions": get_file_permissions(os.path.join(path, entry))}
        for entry in entries
    ]
    })

def get_file_permissions(filepath):
    mode = os.stat(filepath).st_mode
    return stat.filemode(mode)

