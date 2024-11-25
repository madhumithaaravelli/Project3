import os
import stat
import hashlib

def get_file_permissions(filepath):
    """
    Get file permissions in a human-readable format.
    :param filepath: Path to the file.
    :return: File permissions as a string (e.g., '-rw-r--r--').
    """
    mode = os.stat(filepath).st_mode
    return stat.filemode(mode)

def get_file_checksum(filepath, algorithm="md5"):
    """
    Computes the checksum of a file.
    :param filepath: Path to the file.
    :param algorithm: Hashing algorithm (md5, sha256, etc.).
    :return: Checksum value as a string.
    """
    hash_func = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            hash_func.update(chunk)
    return hash_func.hexdigest()


def list_directory(path='.', show_all=False, recursive=False, sort_by=None):
    """
    Lists the contents of a directory with optional flags.

    :param path: Directory path to list.
    :param show_all: Whether to include hidden files.
    :param recursive: Whether to list directories recursively.
    :param sort_by: Sort entries by 'size' or 'mtime' (modification time).
    :return: List of directory contents.
    """
    result = []
    if recursive:
        for root, dirs, files in os.walk(path):
            entries = dirs + files if show_all else [entry for entry in dirs + files if not entry.startswith('.')]
            entry_details = [
                {
                    "name": entry,
                    "size": os.path.getsize(os.path.join(root, entry)),
                    "mtime": os.path.getmtime(os.path.join(root, entry)),
                    "type": "directory" if os.path.isdir(os.path.join(root, entry)) else "file",
                    "permissions": get_file_permissions(os.path.join(root, entry))
                }
                for entry in entries
            ]
            if sort_by == 'size':
                entry_details.sort(key=lambda x: x["size"])
            elif sort_by == 'mtime':
                entry_details.sort(key=lambda x: x["mtime"])
            result.append({"path": root, "entries": entry_details})
    else:
        entries = os.listdir(path)
        if not show_all:
            entries = [entry for entry in entries if not entry.startswith('.')]
        entry_details = [
            {
                "name": entry,
                "size": os.path.getsize(os.path.join(path, entry)),
                "mtime": os.path.getmtime(os.path.join(path, entry)),
                "type": "directory" if os.path.isdir(os.path.join(path, entry)) else "file",
                "permissions": get_file_permissions(os.path.join(path, entry))
            }
            for entry in entries
        ]
        if sort_by == 'size':
            entry_details.sort(key=lambda x: x["size"])
        elif sort_by == 'mtime':
            entry_details.sort(key=lambda x: x["mtime"])
        result.append({"path": path, "entries": entry_details})

    return result
