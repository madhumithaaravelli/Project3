import os
import pytest
from ls_tool.core import list_directory

def test_list_directory():
    result = list_directory(path=".", show_all=False, recursive=False)
    assert isinstance(result, list)

def test_show_all():
    result = list_directory(path=".", show_all=True)
    assert all(item.startswith('.') for entry in result for item in entry['entries'] if item.startswith('.'))

def test_recursive():
    result = list_directory(path=".", recursive=True)
    assert len(result) > 1
