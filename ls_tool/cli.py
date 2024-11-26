import argparse
import sys
import os
import json
from pathlib import Path
from datetime import datetime
from termcolor import colored
import fnmatch
import pwd
import grp

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ls_tool.core import list_directory, get_file_checksum

# Helper function to list Python files recursively
def list_python_files_recursive(path):
    python_files = []
    for root, _, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

# Helper function to list test files
def list_test_files(path):
    tests_path = os.path.join(path, "tests")
    if not os.path.exists(tests_path):
        return []
    return [f for f in os.listdir(tests_path) if f.startswith('test_') and f.endswith('.py')]

# Helper function to list virtual environment directories
def list_virtual_environments(path):
    env_dirs = ['venv', '.env', '.venv']  # common virtual environment names
    return [d for d in os.listdir(path) if d in env_dirs and os.path.isdir(os.path.join(path, d))]

# Helper function to list dependency files
def list_dependency_files(path):
    dependency_files = ['requirements.txt', 'Pipfile', 'Pipfile.lock', 'environment.yml']
    return [f for f in os.listdir(path) if f in dependency_files]

#Helper function to convert file size to human readable size format
def human_readable_size(size):
    """Convert size in bytes to a human-readable format."""
    for unit in ["B", "K", "M", "G", "T", "P"]:
        if size < 1024:
            return f"{size:.1f}{unit}"
        size /= 1024
    return f"{size:.1f}P"

#Helper function to colorize files based on file type
def print_colored_output(entry, args):
    for item in entry['entries']:
        if args.checksum and item['type'] == 'file':
            checksum = get_file_checksum(os.path.join(entry['path'], item['name']))
            print(f"  {colored(item['name'], 'cyan')} | Checksum: {checksum}")
        elif args.permissions:
            print(f"  {colored(item['name'], 'yellow')} - {item['type']} - {item['size']} bytes - Permissions: {item['permissions']}")
        elif item['type'] == 'directory':
            print(f"  {colored(item['name'], 'blue')} - {item['type']} - {item['size']} bytes")
        elif item['type'] == 'file':
            print(f"  {colored(item['name'], 'green')} - {item['type']} - {item['size']} bytes")


def print_long_listing(entry, path, args):
    """Print long listing details for an entry."""
    for item in entry['entries']:
        if item['type'] == 'file' or item['type'] == 'directory':
            size = human_readable_size(item['size']) if args.human else f"{item['size']} bytes"
            permissions = item['permissions']
            mtime = datetime.fromtimestamp(item['mtime']).strftime('%Y-%m-%d %H:%M:%S')
            print(f"{permissions} {size} {mtime} {item['name']}")
        else:
            print(f"{item['name']} - {item['type']}")

# Helper function for recursive depth
def list_directory_with_depth(path, max_depth, current_depth=0):
    """List files and directories up to a certain depth."""
    if current_depth > max_depth:
        return []
    entries = []
    for entry in os.scandir(path):
        entries.append(entry.path)
        if entry.is_dir(follow_symlinks=False):
            entries.extend(
                list_directory_with_depth(entry.path, max_depth, current_depth + 1)
            )
    return entries


def main():
    parser = argparse.ArgumentParser(description="Custom ls command tool.")
    parser.add_argument("path", nargs="?", default=".", help="Directory path to list")
    parser.add_argument("-a", "--all", action="store_true", help="Include hidden files")
    parser.add_argument("-R", "--recursive", action="store_true", help="List directories recursively")
    parser.add_argument("-j", "--json", action="store_true", help="Output in JSON format")
    parser.add_argument("-e", "--env", action="store_true", help="List Python virtual environments")
    parser.add_argument("-p", "--python", action="store_true", help="List Python files only")
    parser.add_argument("-t", "--tests", action="store_true", help="List test files")
    parser.add_argument("-d", "--dependencies", action="store_true", help="List dependency files")
    parser.add_argument("-s", "--sort", choices=["size", "mtime"], help="Sort by size or modification time")
    parser.add_argument("-P", "--permissions", action="store_true", help="Display file permissions")
    parser.add_argument("-c", "--checksum", action="store_true", help="Display file checksum")
    parser.add_argument("-l", "--long", action="store_true", help="Use a long listing format")
    parser.add_argument("-H", "--human", action="store_true", help="Display sizes in human-readable format")
    parser.add_argument("--reverse", action="store_true", help="Reverse the sorting order")
    parser.add_argument("-F", "--classify", action="store_true", help="Append file type indicators")
    parser.add_argument("--color", action="store_true", help="Colorize output based on file type")
    parser.add_argument("--depth", type=int, help="Limit recursion depth (e.g., --depth 2)")
    parser.add_argument("--exclude", type=str, help="Exclude files matching a pattern (e.g., '*.tmp')")
    parser.add_argument("--user", action="store_true", help="Display the owning user of each file")
    parser.add_argument("--group", action="store_true", help="Display the owning group of each file")

    args = parser.parse_args()

    try:
        if args.recursive and args.depth:
            print(f"Listing up to depth {args.depth} recursively...")
            entries = list_directory_with_depth(args.path, args.depth)
            print("\n".join(entries))
            return

        result = list_directory(
            path=args.path,
            show_all=args.all,
            recursive=args.recursive,
        )

        if args.python:
            print("Python Files:")
            python_files = list_python_files_recursive(args.path)
            if python_files:
                print("\n".join(python_files))
            else:
                print("No Python files found.")
        elif args.tests:
            print("Test Files:")
            test_files = list_test_files(args.path)
            if test_files:
                print("\n".join(test_files))
            else:
                print("No test files found.")
        elif args.env:
            print("Virtual Environments:")
            envs = list_virtual_environments(args.path)
            if envs:
                print("\n".join(envs))
            else:
                print("No virtual environments found.")
        elif args.dependencies:
            print("Dependency Files:")
            dependencies = list_dependency_files(args.path)
            if dependencies:
                print("\n".join(dependencies))
            else:
                print("No dependency files found.")
        else:
            # Default behavior for directory listing
            result = list_directory(
                path=args.path,
                show_all=args.all,
                recursive=args.recursive,
                sort_by=args.sort,
                reverse=args.reverse,
                append_type_symbol=args.classify
            )
            if args.json:
                print(json.dumps(result, indent=4))
            else:
                for entry in result:
                    print(f"Directory: {entry['path']}")
                    if args.long:
                        print_long_listing(entry, entry['path'], args)
                    elif args.color:
                        print_colored_output(entry, args)
                    else:
                        for item in entry['entries']:
                            if args.checksum and item['type'] == 'file':
                                checksum = get_file_checksum(os.path.join(entry['path'], item['name']))
                                print(f"  {item['name']} | Checksum: {checksum}")
                            elif args.permissions:
                                print(f"  {item['name']} - {item['type']} - {item['size']} bytes - Permissions: {item['permissions']}")
                            elif args.human:
                                size = human_readable_size(item['size']) if args.human else f"{item['size']} bytes"
                                print(f"  {item['name']} - {item['type']} - {size}")
                            elif args.user:
                                stat_info = os.stat(os.path.join(".", item['name']))
                                owner = pwd.getpwuid(stat_info.st_uid).pw_name
                                print(f"{item['name']} | Owner: {owner}")
                            elif args.group:
                                stat_info = os.stat(os.path.join(".", item['name']))
                                group = grp.getgrgid(stat_info.st_gid).gr_name
                                print(f"  {item['name']} | Group: {group}")
                            elif args.exclude and fnmatch.fnmatch(item['name'], args.exclude):
                                continue
                            else:
                                print(f"  {item['name']} - {item['type']} - {item['size']} bytes")
    except FileNotFoundError as e:
        print(f"Error: Path not found - {e}")
    except PermissionError as e:
        print(f"Error: Permission denied - {e}")
    except Exception as e:
        print(f"Unexpected Error: {e}")


if __name__ == "__main__":
    main()
