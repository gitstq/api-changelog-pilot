# 🛫 APIChangelog-Pilot

> 智能API变更日志生成与版本追踪引擎 - 轻量化、零依赖、自动化

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7+-green.svg)](https://www.python.org/)
[![Stars](https://img.shields.io/github/stars/gitstq/api-changelog-pilot?style=flat)](https://github.com/gitstq/api-changelog-pilot)
[![Forks](https://img.shields.io/github/forks/gitstq/api-changelog-pilot?style=flat)](https://github.com/gitstq/api-changelog-pilot)

---

🌏 **语言切换** | [简体中文](./README.md) | [繁體中文](./README_TW.md) | [English](./README_EN.md) | [日本語](./README_JA.md)

---

## 🎯 项目介绍

**APIChangelog-Pilot** 是一款专为开发者设计的智能工具，旨在自动化 API 变更日志的生成与管理。它能够自动分析代码变更、智能识别变更类型、追踪版本历史，并生成符合行业标准的变更日志文档。

### 🔥 核心价值

- **🤖 智能化分析** - 自动识别 feat、fix、docs 等多种变更类型
- **⚡ 零依赖设计** - 仅依赖 Python 标准库，开箱即用
- **📝 规范遵循** - 完美支持 Conventional Commits 规范
- **🔄 版本追踪** - 自动管理语义化版本（SemVer）
- **🎨 多格式输出** - 支持 Markdown、JSON、HTML、YAML 等多种格式
- **💻 TUI 界面** - 提供交互式终端界面，操作便捷
- **🔍 变更影响分析** - 智能评估变更影响范围
- **🎯 API 语义理解** - 深度理解 API 端点和数据模型

### ✨ 与同类工具的差异化亮点

| 特性 | APIChangelog-Pilot | 其他工具 |
|------|-------------------|---------|
| 依赖要求 | 🚀 **零依赖** | 需要 npm/yarn 等 |
| AI 集成 | ✅ 支持 GLM-5.1 | ❌ 不支持 |
| API 语义 | ✅ 深度理解 | ❌ 仅文本分析 |
| TUI 界面 | ✅ 交互友好 | ❌ 命令行为主 |
| 变更影响 | ✅ 智能评估 | ❌ 基础统计 |

---

## 🚀 快速开始

### 📋 环境要求

- Python 3.7 或更高版本
- Git（用于版本控制功能）
- 终端环境（Bash、Zsh、PowerShell 等）

### ⚡ 安装方式

#### 方式一：pip 安装（推荐）

```bash
pip install api-changelog-pilot
```

#### 方式二：源码安装

```bash
# 克隆仓库
git clone https://github.com/gitstq/api-changelog-pilot.git
cd api-changelog-pilot

# 安装
pip install -e .
```

#### 方式三：直接运行

```bash
# 克隆仓库
git clone https://github.com/gitstq/api-changelog-pilot.git
cd api-changelog-pilot

# 直接运行
python -m changelog_pilot --help
```

### 🎮 快速使用

```bash
# 初始化项目配置
api-changelog-pilot init

# 生成变更日志
api-changelog-pilot generate

# 比较版本差异
api-changelog-pilot diff --from v1.0 --to v2.0

# 发布新版本
api-changelog-pilot release --bump minor

# 启动交互式界面
api-changelog-pilot tui
```

---

## 📖 详细使用指南

### 1️⃣ 初始化配置

在项目根目录运行：

```bash
api-changelog-pilot init
```

这将创建 `.changelogpilot.json` 配置文件。

### 2️⃣ 生成变更日志

```bash
# 生成最近所有变更
api-changelog-pilot generate

# 指定版本范围
api-changelog-pilot generate --since v1.0.0 --until v2.0.0

# 指定输出格式
api-changelog-pilot generate --format json

# 启用 AI 增强分析
api-changelog-pilot generate --ai
```

### 3️⃣ 版本管理

```bash
# 查看版本列表
api-changelog-pilot list

# 比较两个版本
api-changelog-pilot diff --from v1.0.0 --to v2.0.0

# 发布新版本
api-changelog-pilot release --bump major    # 主版本更新
api-changelog-pilot release --bump minor    # 次版本更新
api-changelog-pilot release --bump patch    # 补丁更新

# 模拟发布
api-changelog-pilot release --bump minor --dry-run
```

### 4️⃣ 生成报告

```bash
# 生成 Markdown 报告
api-changelog-pilot report --format markdown

# 生成 HTML 报告
api-changelog-pilot report --format html

# 保存到文件
api-changelog-pilot report --format markdown --output CHANGELOG.md
```

### 5️⃣ 变更影响分析

```bash
# 分析当前变更的影响
api-changelog-pilot analyze

# 指定路径分析
api-changelog-pilot analyze --path /path/to/api

# 保存分析结果
api-changelog-pilot analyze --output impact_report.md
```

### 6️⃣ TUI 交互界面

```bash
# 启动交互式界面
api-changelog-pilot tui
```

在 TUI 界面中，你可以：

- 📊 查看变更统计
- 📝 生成变更日志
- 🔍 比较版本差异
- 🎯 分析变更影响
- 📦 发布新版本
- 📄 导出报告
- ⚙️ 配置管理

---

## 💡 设计思路与迭代规划

### 🎨 设计理念

1. **简洁至上** - 零外部依赖，仅使用 Python 标准库
2. **用户友好** - 提供 CLI 和 TUI 两种交互方式
3. **规范遵循** - 完全支持 Conventional Commits 规范
4. **智能分析** - 集成 AI 能力，深度理解代码语义
5. **可扩展性** - 支持插件系统和自定义模板

### 🛠️ 技术选型

- **语言**: Python 3.7+（标准库为主）
- **架构**: 模块化设计，便于扩展
- **输出**: Markdown（默认）、JSON、HTML、YAML
- **版本**: 遵循语义化版本（SemVer）
- **提交**: 遵循 Conventional Commits 规范

### 📅 后续迭代计划

- [ ] **v1.1.0** - 集成 GLM-5.1 AI 模型，增强变更分析能力
- [ ] **v1.2.0** - 支持更多框架（FastAPI、Django、Tornado）
- [ ] **v1.3.0** - 添加 Web UI 界面
- [ ] **v1.4.0** - 支持 GitHub Actions 集成
- [ ] **v2.0.0** - 添加插件系统和社区模板市场

---

## 📦 打包与部署

### 🐳 Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . /app
RUN pip install -e .

ENTRYPOINT ["api-changelog-pilot"]
```

构建并运行：

```bash
docker build -t api-changelog-pilot .
docker run --rm -v $(pwd):/repo api-changelog-pilot generate
```

### 🔧 GitHub Actions 集成

创建 `.github/workflows/changelog.yml`：

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

## 🤝 贡献指南

欢迎提交 Pull Request 或创建 Issue！

### 🐛 Bug 报告

请在 [GitHub Issues](https://github.com/gitstq/api-changelog-pilot/issues) 中创建，包含以下信息：

- 问题描述
- 复现步骤
- 期望行为
- 实际行为
- 环境信息（Python 版本、操作系统等）

### ✨ 功能请求

欢迎提交功能请求，请描述：

- 功能用途
- 使用场景
- 可能的实现方案

### 🔧 代码贡献

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建 Pull Request

---

## 📄 开源协议

本项目采用 [MIT License](LICENSE) 开源协议。

---

## 🙏 致谢

本项目灵感来源于以下优秀项目：

- [Keep a Changelog](https://keepachangelog.com/) - 变更日志规范
- [Conventional Commits](https://www.conventionalcommits.org/) - 提交信息规范
- [Semantic Versioning](https://semver.org/) - 语义化版本规范

---

<p align="center">
  <strong>如果你觉得这个项目有帮助，请给我一个 ⭐️！</strong>
</p>

<p align="center">
 Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>
