# Project3


[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![npm-build](https://github.com/deepr41/WolfJobs/actions/workflows/build-checker.yml/badge.svg)](https://github.com/deepr41/WolfJobs/actions/workflows/build-checker.yml)
[![npm-build](https://github.com/deepr41/WolfJobs/actions/workflows/build-test-upload.yml/badge.svg)](https://github.com/deepr41/WolfJobs/actions/workflows/build-test-upload.yml)
[![PEP8](https://img.shields.io/badge/code%20style-pep8-orange.svg)](https://www.python.org/dev/peps/pep-0008/)
[![Issues](https://img.shields.io/github/issues/deepr41/wolfjobs)](https://GitHub.com/deepr41/Wolfjobs/)
[![Issues Closed](https://img.shields.io/github/issues-closed/deepr41/wolfjobs)](https://GitHub.com/deepr41/Wolfjobs/)
![last commit](https://img.shields.io/github/last-commit/deepr41/Wolfjobs)
![Lines of code](https://tokei.rs/b1/github/deepr41/wolfjobs)
[![Repo-size](https://img.shields.io/github/repo-size/deepr41/Wolfjobs)](https://GitHub.com/deepr41/Wolfjobs/)
[![file_count](https://img.shields.io/github/directory-file-count/deepr41/Wolfjobs)](https://GitHub.com/deepr41/Wolfjobs/)
[![language_count](https://img.shields.io/github/languages/count/deepr41/Wolfjobs)](https://GitHub.com/deepr41/Wolfjobs/)
[![Downloads](https://img.shields.io/github/downloads/deepr41/WolfJobs/total)](https://GitHub.com/deepr41/Wolfjobs/)
[![Top Language](https://img.shields.io/github/languages/top/deepr41/wolfjobs)](https://GitHub.com/deepr41/Wolfjobs/)
[![DOI](https://zenodo.org/badge/429097663.svg)](https://zenodo.org/badge/latestdoi/429097663)
[![Release](https://img.shields.io/github/v/release/deepr41/wolfjobs)](https://gitHub.com/deepr41/Wolfjobs)
[![codecov](https://codecov.io/gh/deepr41/WolfJobs/graph/badge.svg?token=RH472ZM4PT)](https://codecov.io/gh/deepr41/WolfJobs)

# Python LS Tool

This is a Python-based tool that replicates the core functionality of the Unix `ls` command. It supports multiple flags for listing files and directories with various options.

## Features

- List files in the current directory
- `-l`: Long listing format (file permissions, size, modification time)
- `-a`: Show hidden files
- `-h`: Human-readable file sizes
- `-S`: Sort by size
- `-t`: Sort by modification time
- `-r`: Reverse order
- `-d`: List directories themselves
- `-1`: List one entry per line

## Installation

Clone the repository:
```bash
git clone https://github.com/yourusername/python-ls-tool.git
cd python-ls-tool
pip install -r requirements.txt
