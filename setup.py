from setuptools import setup, find_packages

setup(
    name="ls_tool",
    version="1.0.0",
    description="A Python-based implementation of the ls command",
    author="Madhumitha Aravelli",
    author_email="madhumithaaravelli@gmail.com",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "ls-tool=ls_tool.cli:main",
        ],
    },
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
