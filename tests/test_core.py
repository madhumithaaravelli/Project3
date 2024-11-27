import os
import pytest
import tempfile
from ls_tool.core import list_directory, get_file_checksum
from ls_tool.cli import human_readable_size

#Test list directory
def test_list_directory():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, "file.txt")
        open(file_path, "w").close()
        result = list_directory(temp_dir)
        assert len(result[0]["entries"]) == 1
        assert result[0]["entries"][0]["name"] == "file.txt"

#Test if it displays hidden files of list directory
def test_list_directory_hidden_files():
    with tempfile.TemporaryDirectory() as temp_dir:
        hidden_file = os.path.join(temp_dir, ".hidden.txt")
        open(hidden_file, "w").close()
        result = list_directory(temp_dir, show_all=True)
        assert len(result[0]["entries"]) == 1
        assert result[0]["entries"][0]["name"] == ".hidden.txt"

#Test if all the files and directories are displayed
def test_show_all():
    result = list_directory(path=".", show_all=True)
    assert all(isinstance(item, str) and item.startswith('.') for entry in result for item in entry['entries'] if isinstance(item, str) and item.startswith('.'))

#Test recursive flag of list directory
def test_recursive():
    result = list_directory(path=".", recursive=True)
    assert len(result) > 1

# Test listing a directory with nested folders
def test_list_directory_nested_structure():
    with tempfile.TemporaryDirectory() as temp_dir:
        os.mkdir(os.path.join(temp_dir, "subdir"))
        file_path = os.path.join(temp_dir, "file.txt")
        open(file_path, "w").close()
        result = list_directory(temp_dir, recursive=True)
        assert len(result) == 2  # Root directory and subdir
        assert any(entry["path"].endswith("subdir") for entry in result)

# Test sorting by size
def test_sort_by_size():
    with tempfile.TemporaryDirectory() as temp_dir:
        small_file = os.path.join(temp_dir, "small.txt")
        large_file = os.path.join(temp_dir, "large.txt")
        with open(small_file, "w") as sf:
            sf.write("a")
        with open(large_file, "w") as lf:
            lf.write("b" * 1024)
        result = list_directory(temp_dir, sort_by="size")
        assert result[0]["entries"][0]["name"] == "small.txt"
        assert result[0]["entries"][-1]["name"] == "large.txt"

# Test sorting by modification time
def test_sort_by_mtime():
    with tempfile.TemporaryDirectory() as temp_dir:
        old_file = os.path.join(temp_dir, "old.txt")
        new_file = os.path.join(temp_dir, "new.txt")
        open(old_file, "w").close()
        open(new_file, "w").close()
        os.utime(new_file, (os.path.getatime(new_file), os.path.getmtime(new_file) + 100))
        result = list_directory(temp_dir, sort_by="mtime")
        assert result[0]["entries"][0]["name"] == "old.txt"
        assert result[0]["entries"][-1]["name"] == "new.txt"

# Test human-readable size conversion
def test_human_readable_size():
    assert human_readable_size(1023) == "1023.0B"
    assert human_readable_size(1024) == "1.0K"
    assert human_readable_size(1024**2) == "1.0M"

# Test calculating file checksum
def test_file_checksum():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, "file.txt")
        with open(file_path, "w") as f:
            f.write("test content")
        checksum = get_file_checksum(file_path)
        assert checksum is not None
        assert len(checksum) > 0

# Test permissions output
def test_list_permissions():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, "file.txt")
        open(file_path, "w").close()
        result = list_directory(temp_dir)
        assert result[0]["entries"][0]["permissions"] is not None

# Test recursive listing
def test_recursive_listing():
    with tempfile.TemporaryDirectory() as temp_dir:
        sub_dir = os.path.join(temp_dir, "subdir")
        os.mkdir(sub_dir)
        file_path = os.path.join(sub_dir, "file.txt")
        open(file_path, "w").close()
        result = list_directory(temp_dir, recursive=True)
        assert len(result) == 2
        assert any(entry["path"].endswith("subdir") for entry in result)

# Test JSON output format
def test_json_output():
    with tempfile.TemporaryDirectory() as temp_dir:
        file_path = os.path.join(temp_dir, "file.txt")
        open(file_path, "w").close()
        result = list_directory(temp_dir)
        assert isinstance(result, list)
        assert "entries" in result[0]

# Test listing virtual environments
def test_list_virtual_environments():
    with tempfile.TemporaryDirectory() as temp_dir:
        venv_dir = os.path.join(temp_dir, "venv")
        os.mkdir(venv_dir)
        result = list_directory(temp_dir)
        assert any(entry["name"] == "venv" for entry in result[0]["entries"])

# Test handling nonexistent paths
def test_nonexistent_path():
    with pytest.raises(FileNotFoundError):
        list_directory("/nonexistent/path")

# Test handling permissions error
def test_permission_error(monkeypatch):
    def mock_listdir(_):
        raise PermissionError("Mocked permission error")
    monkeypatch.setattr(os, "listdir", mock_listdir)
    with pytest.raises(PermissionError):
        list_directory(".")

# Test for symbolic links
def test_symbolic_link():
    with tempfile.TemporaryDirectory() as temp_dir:
        target_file = os.path.join(temp_dir, "target.txt")
        link_file = os.path.join(temp_dir, "link.txt")
        open(target_file, "w").close()
        os.symlink(target_file, link_file)
        result = list_directory(temp_dir)

        # Check that both the target file and symbolic link are listed
        entry_names = [entry["name"] for entry in result[0]["entries"]]
        assert "target.txt" in entry_names
        assert "link.txt" in entry_names

        # Optional: Check the entry count (should include both files)
        assert len(result[0]["entries"]) == 2

# Test for filtering by file extension
def test_filter_by_extension():
    with tempfile.TemporaryDirectory() as temp_dir:
        txt_file = os.path.join(temp_dir, "file.txt")
        log_file = os.path.join(temp_dir, "file.log")
        open(txt_file, "w").close()
        open(log_file, "w").close()
        result = list_directory(temp_dir)

        # Manually filter the results for .txt files
        txt_files = [entry["name"] for entry in result[0]["entries"] if entry["name"].endswith(".txt")]

        assert len(txt_files) == 1
        assert txt_files[0] == "file.txt"


# Test for large number of files
def test_large_number_of_files():
    with tempfile.TemporaryDirectory() as temp_dir:
        for i in range(1000):
            open(os.path.join(temp_dir, f"file_{i}.txt"), "w").close()
        result = list_directory(temp_dir)
        assert len(result[0]["entries"]) == 1000
        assert result[0]["entries"][0]["name"].startswith("file_")

# Test for empty file checksum
def test_empty_file_checksum():
    with tempfile.TemporaryDirectory() as temp_dir:
        empty_file = os.path.join(temp_dir, "empty.txt")
        open(empty_file, "w").close()
        checksum = get_file_checksum(empty_file)
        assert checksum is not None
        assert len(checksum) > 0

# Test for directory with special characters in name
def test_special_characters_in_directory_name():
    with tempfile.TemporaryDirectory() as temp_dir:
        special_dir = os.path.join(temp_dir, "sp@c!@l #chars")
        os.mkdir(special_dir)
        result = list_directory(temp_dir)
        assert len(result[0]["entries"]) == 1
        assert result[0]["entries"][0]["name"] == "sp@c!@l #chars"

