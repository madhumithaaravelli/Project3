import argparse
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ls_tool.core import list_directory
import json

# Helper function to list Python files
def list_python_files_recursive(path):
    python_files = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                python_files.append(os.path.join(root, file))
    return python_files

# Helper function to list test files
def list_test_files(path):
    return [f for f in os.listdir(path+"/tests") if f.startswith('test_') and f.endswith('.py')]

# Helper function to list virtual environment directories
def list_virtual_environments(path):
    env_dirs = ['venv', '.env', '.venv']  # common virtual environment names
    return [d for d in os.listdir(path) if d in env_dirs]

# Helper function to list dependency files
def list_dependency_files(path):
    dependency_files = ['requirements.txt', 'Pipfile', 'Pipfile.lock', 'environment.yml']
    return [f for f in os.listdir(path) if f in dependency_files]

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

    
    args = parser.parse_args()
    
    try:
        result = list_directory(args.path, show_all=args.all, recursive=args.recursive)
        if args.env:
            print("Virtual Environments:")
            envs = list_virtual_environments(args.path)
            if envs:
                print("\n".join(envs))
            else:
                print("No virtual environments found.")
        elif args.python:
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
        elif args.dependencies:
            print("Dependency Files:")
            dependencies = list_dependency_files(args.path)
            if dependencies:
                print("\n".join(dependencies))
            else:
                print("No dependency files found.")
        elif args.json:
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
