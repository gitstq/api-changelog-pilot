#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APIChangelog-Pilot 安装配置
"""

from setuptools import setup, find_packages
from pathlib import Path

# 读取README
readme_file = Path(__file__).parent / "README.md"
long_description = ""
if readme_file.exists():
    long_description = readme_file.read_text(encoding="utf-8")

# 读取版本
version_file = Path(__file__).parent / "changelog_pilot" / "__init__.py"
version = "1.0.0"
if version_file.exists():
    content = version_file.read_text()
    for line in content.split("\n"):
        if "__version__" in line:
            version = line.split("=")[1].strip().strip('"').strip("'")
            break

setup(
    name="api-changelog-pilot",
    version=version,
    author="gitstq",
    author_email="",
    description="🛫 智能API变更日志生成与版本追踪引擎",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gitstq/api-changelog-pilot",
    license="MIT",
    
    # 包配置
    packages=find_packages(exclude=["tests", "tests.*", "examples", "docs"]),
    package_data={
        "changelog_pilot": ["py.typed"],
    },
    include_package_data=True,
    
    # Python版本要求
    python_requires=">=3.7",
    
    # 入口点
    entry_points={
        "console_scripts": [
            "api-changelog-pilot=changelog_pilot.__main__:main",
            "changelog-pilot=changelog_pilot.__main__:main",
            "apichangelog=changelog_pilot.__main__:main",
        ],
    },
    
    # 分类
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control :: Git",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
        "Natural Language :: English",
        "Natural Language :: Chinese (Simplified)",
    ],
    
    # 关键字
    keywords=[
        "api",
        "changelog",
        "version",
        "git",
        "semantic-versioning",
        "conventional-commits",
        "release",
        "automation",
        "cli",
        "tui",
    ],
    
    # 项目依赖
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=3.0.0",
            "flake8>=5.0.0",
            "black>=22.0.0",
            "mypy>=0.990",
        ],
        "yaml": [
            "PyYAML>=5.4.0",
        ],
    },
)
