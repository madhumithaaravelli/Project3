import argparse
from ls_tool.core import list_directory
import json

def main():
    parser = argparse.ArgumentParser(description="Custom ls command tool.")
    parser.add_argument("path", nargs="?", default=".", help="Directory path to list")
    parser.add_argument("-a", "--all", action="store_true", help="Include hidden files")
    parser.add_argument("-R", "--recursive", action="store_true", help="List directories recursively")
    parser.add_argument("-j", "--json", action="store_true", help="Output in JSON format")
    
    args = parser.parse_args()
    
    try:
        result = list_directory(args.path, show_all=args.all, recursive=args.recursive)
        if args.json:
            print(json.dumps(result, indent=4))
        else:
            for entry in result:
                print(f"Directory: {entry['path']}")
                for item in entry['entries']:
                    print(f"  {item}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
