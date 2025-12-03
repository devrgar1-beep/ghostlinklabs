#!/usr/bin/env python3
"""
Setup script for GhostLink Hybrid Triad
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ghostlink",
    version="0.1.0",
    author="GhostLink Team",
    author_email="team@ghostlink.localhost",
    description="GhostLink AI Ecosystem - Absorptive Architecture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ghostlink/hybrid-triad",
    packages=find_packages(where="implementation"),
    package_dir={"": "implementation"},
    include_package_data=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "ghostlink=core_runtime.main:main",
            "ghostlink-api=api.main:main",
            "ghostlink-cli=interfaces.cli:cli",
        ],
    },
)
