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

def human_readable_size(size):
    """
    Converts a file size in bytes to a human-readable format.
    :param size: File size in bytes.
    :return: Human-readable file size as a string (e.g., '1.2 KB').
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} PB"

def get_entry_details(root, entries, human_readable=False):
    """
    Helper function for list_directory to fetch detailed entry information.
    :param root: Root directory path.
    :param entries: List of directory entries.
    :param human_readable: Whether to format sizes in human-readable format.
    :return: List of detailed entry information.
    """
    details = []
    for entry in entries:
        entry_path = os.path.join(root, entry)
        size = os.path.getsize(entry_path)
        details.append({
            "name": entry,
            "size": human_readable_size(size) if human_readable else size,
            "mtime": os.path.getmtime(entry_path),
            "type": "directory" if os.path.isdir(entry_path) else "file",
            "permissions": get_file_permissions(entry_path)
        })
    return details

def list_directory(path='.', show_all=False, recursive=False, sort_by=None, reverse=False, human_readable=False):
    """
    Lists the contents of a directory with optional flags.

    :param path: Directory path to list.
    :param show_all: Whether to include hidden files.
    :param recursive: Whether to list directories recursively.
    :param sort_by: Sort entries by 'size' or 'mtime' (modification time).
    :param reverse: Whether to reverse the sort order.
    :param human_readable: Whether to format sizes in human-readable format.
    :return: List of directory contents.
    """
    result = []
    if recursive:
        for root, dirs, files in os.walk(path):
            entries = dirs + files if show_all else [entry for entry in dirs + files if not entry.startswith('.')]
            entry_details = get_entry_details(root, entries, human_readable)
            if sort_by == 'size':
                entry_details.sort(key=lambda x: x["size"] if not human_readable else float(x["size"].split()[0]), reverse=reverse)
            elif sort_by == 'mtime':
                entry_details.sort(key=lambda x: x["mtime"], reverse=reverse)
            result.append({"path": root, "entries": entry_details})
    else:
        entries = os.listdir(path)
        if not show_all:
            entries = [entry for entry in entries if not entry.startswith('.')]
        entry_details = get_entry_details(path, entries, human_readable)
        if sort_by == 'size':
            entry_details.sort(key=lambda x: x["size"] if not human_readable else float(x["size"].split()[0]), reverse=reverse)
        elif sort_by == 'mtime':
            entry_details.sort(key=lambda x: x["mtime"], reverse=reverse)
        result.append({"path": path, "entries": entry_details})

    return result
