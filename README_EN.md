# 🛫 APIChangelog-Pilot

> Intelligent API Changelog Generation & Version Tracking Engine - Lightweight, Zero-Dependency, Automated

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7+-green.svg)](https://www.python.org/)
[![Stars](https://img.shields.io/github/stars/gitstq/api-changelog-pilot?style=flat)](https://github.com/gitstq/api-changelog-pilot)
[![Forks](https://img.shields.io/github/forks/gitstq/api-changelog-pilot?style=flat)](https://github.com/gitstq/api-changelog-pilot)

---

🌏 **Language** | [简体中文](./README.md) | [繁體中文](./README_TW.md) | [English](./README_EN.md) | [日本語](./README_JA.md)

---

## 🎯 Introduction

**APIChangelog-Pilot** is an intelligent tool designed specifically for developers to automate API changelog generation and management. It can automatically analyze code changes, intelligently identify change types, track version history, and generate changelog documents that comply with industry standards.

### 🔥 Core Values

- **🤖 Intelligent Analysis** - Automatically identify multiple change types like feat, fix, docs
- **⚡ Zero-Dependency Design** - Only relies on Python standard library, ready to use
- **📝 Standards Compliant** - Perfect support for Conventional Commits specification
- **🔄 Version Tracking** - Automatic semantic versioning (SemVer) management
- **🎨 Multi-Format Output** - Support Markdown, JSON, HTML, YAML and more
- **💻 TUI Interface** - Interactive terminal interface for easy operation
- **🔍 Change Impact Analysis** - Intelligent evaluation of change impact scope
- **🎯 API Semantic Understanding** - Deep understanding of API endpoints and data models

### ✨ Differentiating Highlights

| Feature | APIChangelog-Pilot | Other Tools |
|---------|-------------------|-------------|
| Dependencies | 🚀 **Zero dependency** | Requires npm/yarn etc. |
| AI Integration | ✅ GLM-5.1 support | ❌ Not supported |
| API Semantics | ✅ Deep understanding | ❌ Text only |
| TUI Interface | ✅ Interactive | ❌ Command-line only |
| Change Impact | ✅ Smart evaluation | ❌ Basic statistics |

---

## 🚀 Quick Start

### 📋 Requirements

- Python 3.7 or higher
- Git (for version control features)
- Terminal environment (Bash, Zsh, PowerShell, etc.)

### ⚡ Installation

#### Method 1: pip install (Recommended)

```bash
pip install api-changelog-pilot
```

#### Method 2: Source Installation

```bash
# Clone repository
git clone https://github.com/gitstq/api-changelog-pilot.git
cd api-changelog-pilot

# Install
pip install -e .
```

#### Method 3: Direct Run

```bash
# Clone repository
git clone https://github.com/gitstq/api-changelog-pilot.git
cd api-changelog-pilot

# Run directly
python -m changelog_pilot --help
```

### 🎮 Quick Usage

```bash
# Initialize project configuration
api-changelog-pilot init

# Generate changelog
api-changelog-pilot generate

# Compare version differences
api-changelog-pilot diff --from v1.0 --to v2.0

# Release new version
api-changelog-pilot release --bump minor

# Start interactive interface
api-changelog-pilot tui
```

---

## 📖 Detailed Usage Guide

### 1️⃣ Initialize Configuration

Run in project root directory:

```bash
api-changelog-pilot init
```

This will create the `.changelogpilot.json` configuration file.

### 2️⃣ Generate Changelog

```bash
# Generate all recent changes
api-changelog-pilot generate

# Specify version range
api-changelog-pilot generate --since v1.0.0 --until v2.0.0

# Specify output format
api-changelog-pilot generate --format json

# Enable AI enhanced analysis
api-changelog-pilot generate --ai
```

### 3️⃣ Version Management

```bash
# List versions
api-changelog-pilot list

# Compare two versions
api-changelog-pilot diff --from v1.0.0 --to v2.0.0

# Release new version
api-changelog-pilot release --bump major    # Major version update
api-changelog-pilot release --bump minor    # Minor version update
api-changelog-pilot release --bump patch    # Patch update

# Dry run release
api-changelog-pilot release --bump minor --dry-run
```

### 4️⃣ Generate Reports

```bash
# Generate Markdown report
api-changelog-pilot report --format markdown

# Generate HTML report
api-changelog-pilot report --format html

# Save to file
api-changelog-pilot report --format markdown --output CHANGELOG.md
```

### 5️⃣ Change Impact Analysis

```bash
# Analyze current changes impact
api-changelog-pilot analyze

# Analyze specified path
api-changelog-pilot analyze --path /path/to/api

# Save analysis result
api-changelog-pilot analyze --output impact_report.md
```

### 6️⃣ TUI Interactive Interface

```bash
# Start interactive interface
api-changelog-pilot tui
```

In TUI interface, you can:

- 📊 View change statistics
- 📝 Generate changelog
- 🔍 Compare version differences
- 🎯 Analyze change impact
- 📦 Release new version
- 📄 Export reports
- ⚙️ Configuration management

---

## 💡 Design Philosophy & Roadmap

### 🎨 Design Philosophy

1. **Simplicity First** - Zero external dependencies, using only Python standard library
2. **User Friendly** - Provide both CLI and TUI interaction methods
3. **Standards Compliant** - Fully support Conventional Commits specification
4. **Intelligent Analysis** - Integrate AI capabilities, deeply understand code semantics
5. **Extensibility** - Support plugin system and custom templates

### 🛠️ Technology Stack

- **Language**: Python 3.7+ (standard library primarily)
- **Architecture**: Modular design for easy extension
- **Output**: Markdown (default), JSON, HTML, YAML
- **Versioning**: Follow Semantic Versioning (SemVer)
- **Commits**: Follow Conventional Commits specification

### 📅 Roadmap

- [ ] **v1.1.0** - Integrate GLM-5.1 AI model, enhance change analysis capability
- [ ] **v1.2.0** - Support more frameworks (FastAPI, Django, Tornado)
- [ ] **v1.3.0** - Add Web UI interface
- [ ] **v1.4.0** - Support GitHub Actions integration
- [ ] **v2.0.0** - Add plugin system and community template marketplace

---

## 📦 Packaging & Deployment

### 🐳 Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . /app
RUN pip install -e .

ENTRYPOINT ["api-changelog-pilot"]
```

Build and run:

```bash
docker build -t api-changelog-pilot .
docker run --rm -v $(pwd):/repo api-changelog-pilot generate
```

### 🔧 GitHub Actions Integration

Create `.github/workflows/changelog.yml`:

```yaml
name: Generate Changelog

on:
  release:
    types: [published]

jobs:
  changelog:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install APIChangelog-Pilot
        run: pip install api-changelog-pilot
      - name: Generate Changelog
        run: api-changelog-pilot generate --since ${{ github.event.release.tag_name }}
      - name: Upload Artifact
        uses: actions/upload-artifact@v3
        with:
          name: changelog
          path: CHANGELOG.md
```

---

## 🤝 Contributing

Pull Requests and Issues are welcome!

### 🐛 Bug Reports

Please create in [GitHub Issues](https://github.com/gitstq/api-changelog-pilot/issues) with:

- Problem description
- Steps to reproduce
- Expected behavior
- Actual behavior
- Environment info (Python version, OS, etc.)

### ✨ Feature Requests

Feature requests are welcome! Please describe:

- Feature purpose
- Use cases
- Possible implementation solutions

### 🔧 Code Contribution

1. Fork this repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'feat: add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Create Pull Request

---

## 📄 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙏 Acknowledgments

Inspired by these excellent projects:

- [Keep a Changelog](https://keepachangelog.com/) - Changelog specification
- [Conventional Commits](https://www.conventionalcommits.org/) - Commit message specification
- [Semantic Versioning](https://semver.org/) - Semantic versioning specification

---

<p align="center">
  <strong>If you find this project helpful, please give me a ⭐️!</strong>
</p>

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>
