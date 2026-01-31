#!/usr/bin/env python3
"""
GAIA Framework - Setup Script
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="gaia",
    version="0.5.0",
    author="GAIA Contributors",
    author_email="",
    description="GAIA - AI Collaborative Problem Solving Framework",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/gaia-framework",
    packages=find_packages(exclude=["tests*", "examples*"]),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development",
        "Topic :: Utilities",
    ],
    python_requires=">=3.10",
    install_requires=[
        "click>=8.1.0",
        "pydantic>=2.0.0",
        "pyyaml>=6.0",
        "requests>=2.28.0",
        "rich>=13.0.0",
        "questionary>=2.0.0",
        "networkx>=3.0",
    ],
    extras_require={
        "web": [
            "fastapi>=0.100.0",
            "uvicorn>=0.23.0",
        ],
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "ruff>=0.1.0",
            "mypy>=1.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "gaia=gaia_cli.commands:cli",
        ],
    },
)
