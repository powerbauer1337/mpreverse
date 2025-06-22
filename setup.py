#!/usr/bin/env python3
"""Setup script for MarsPro Reverse Engineering Tools."""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="marspro-reverse-engineering",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Reverse engineering tools for MarsPro Android app and Home Assistant integration",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/your-repo/marspro-reverse-engineering",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "frida-tools>=14.0.0",
        "uv>=0.7.0",
        "mcp>=1.9.0",
        "aiohttp>=3.8.0",
        "bleak>=0.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "black>=22.0.0",
            "flake8>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "marspro-analyze=scripts.analyze:main",
            "marspro-frida=scripts.frida_hooks:main",
        ],
    },
) 