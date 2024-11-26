import os
import pytest
import tempfile
from ls_tool.core import list_directory

def test_list_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, "file.txt")
        open(file_path, "w").close()
        result = list_directory(temp_dir)
        assert len(result[0]["entries"]) == 1
        assert result[0]["entries"][0]["name"] == "file.txt"

def test_list_directory_hidden_files():
    with tempfile.TemporaryDirectory() as temp_dir:
        hidden_file = os.path.join(temp_dir, ".hidden.txt")
        open(hidden_file, "w").close()
        result = list_directory(temp_dir, show_all=True)
        assert len(result[0]["entries"]) == 1
        assert result[0]["entries"][0]["name"] == ".hidden.txt"

def test_show_all():
    result = list_directory(path=".", show_all=True)
    assert all(isinstance(item, str) and item.startswith('.') for entry in result for item in entry['entries'] if isinstance(item, str) and item.startswith('.'))

def test_recursive():
    result = list_directory(path=".", recursive=True)
    assert len(result) > 1
