# 🛫 APIChangelog-Pilot

> 智能API變更新日誌生成與版本追蹤引擎 - 輕量化、零依賴、自動化

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7+-green.svg)](https://www.python.org/)
[![Stars](https://img.shields.io/github/stars/gitstq/api-changelog-pilot?style=flat)](https://github.com/gitstq/api-changelog-pilot)
[![Forks](https://img.shields.io/github/forks/gitstq/api-changelog-pilot?style=flat)](https://github.com/gitstq/api-changelog-pilot)

---

🌏 **語言切換** | [簡體中文](./README.md) | [繁體中文](./README_TW.md) | [English](./README_EN.md) | [日本語](./README_JA.md)

---

## 🎯 項目介紹

**APIChangelog-Pilot** 是一款專為開發者設計的智慧工具，旨在自動化 API 變 밝�錄的生成與管理。它能夠自動分析代碼變更、智慧識別變更類型、追蹤版本歷史，並生成符合行業標準的變<delete_file>文檔。

### 🔥 核心價值

- **🤖 智慧化分析** - 自動識別 feat、fix、docs 等多種變更類型
- **⚡ 零依賴設計** - 僅依賴 Python 標準庫，開箱即用
- **📝 規範遵循** - 完美支持 Conventional Commits 規範
- **🔄 版本追蹤** - 自動管理語義化版本（SemVer）
- **🎨 多格式輸出** - 支持 Markdown、JSON、HTML、YAML 等多種格式
- **💻 TUI 界面** - 提供互動式終端界面，操作便捷
- **🔍 變更影響分析** - 智慧評估變更影響範圍
- **🎯 API 語義理解** - 深度理解 API 端點和數據模型

### ✨ 與同類工具的差異化亮點

| 特性 | APIChangelog-Pilot | 其他工具 |
|------|-------------------|---------|
| 依賴要求 | 🚀 **零依賴** | 需要 npm/yarn 等 |
| AI 集成 | ✅ 支持 GLM-5.1 | ❌ 不支持 |
| API 語義 | ✅ 深度理解 | ❌ 僅文本分析 |
| TUI 界面 | ✅ 互動友好 | ❌ 命令列為主 |
| 變更影響 | ✅ 智慧評估 | ❌ 基礎統計 |

---

## 🚀 快速開始

### 📋 環境要求

- Python 3.7 或更高版本
- Git（用於版本控制功能）
- 終端環境（Bash、Zsh、PowerShell 等）

### ⚡ 安裝方式

#### 方式一：pip 安裝（推薦）

```bash
pip install api-changelog-pilot
```

#### 方式二：原始碼安裝

```bash
# 克隆倉庫
git clone https://github.com/gitstq/api-changelog-pilot.git
cd api-changelog-pilot

# 安裝
pip install -e .
```

#### 方式三：直接運行

```bash
# 克隆倉庫
git clone https://github.com/gitstq/api-changelog-pilot.git
cd api-changelog-pilot

# 直接運行
python -m changelog_pilot --help
```

### 🎮 快速使用

```bash
# 初始化專案配置
api-changelog-pilot init

# 生成變更新日誌
api-changelog-pilot generate

# 比較版本差異
api-changelog-pilot diff --from v1.0 --to v2.0

# 發布新版本
api-changelog-pilot release --bump minor

# 啟動互動式界面
api-changelog-pilot tui
```

---

## 📖 詳細使用指南

### 1️⃣ 初始化配置

在專案根目錄運行：

```bash
api-changelog-pilot init
```

這將創建 `.changelogpilot.json` 設定檔。

### 2️⃣ 生成變更新日誌

```bash
# 生成最近所有變更
api-changelog-pilot generate

# 指定版本範圍
api-changelog-pilot generate --since v1.0.0 --until v2.0.0

# 指定輸出格式
api-changelog-pilot generate --format json

# 啟用 AI 增強分析
api-changelog-pilot generate --ai
```

### 3️⃣ 版本管理

```bash
# 查看版本列表
api-changelog-pilot list

# 比較兩個版本
api-changelog-pilot diff --from v1.0.0 --to v2.0.0

# 發布新版本
api-changelog-pilot release --bump major    # 主版本更新
api-changelog-pilot release --bump minor    # 次版本更新
api-changelog-pilot release --bump patch    # 補丁更新

# 模擬發布
api-changelog-pilot release --bump minor --dry-run
```

### 4️⃣ 生成報告

```bash
# 生成 Markdown 報告
api-changelog-pilot report --format markdown

# 生成 HTML 報告
api-changelog-pilot report --format html

# 保存到文件
api-changelog-pilot report --format markdown --output CHANGELOG.md
```

### 5️⃣ 變更影響分析

```bash
# 分析當前變更的影響
api-changelog-pilot analyze

# 指定路徑分析
api-changelog-pilot analyze --path /path/to/api

# 保存分析結果
api-changelog-pilot analyze --output impact_report.md
```

### 6️⃣ TUI 互動界面

```bash
# 啟動互動式界面
api-changelog-pilot tui
```

在 TUI 界面中，你可以：

- 📊 查看變更統計
- 📝 生成變更新日誌
- 🔍 比較版本差異
- 🎯 分析變更影響
- 📦 發布新版本
- 📄 導出報告
- ⚙️ 配置管理

---

## 💡 設計思路與迭代規劃

### 🎨 設計理念

1. **簡潔至上** - 零外部依賴，僅使用 Python 標準庫
2. **使用者友好** - 提供 CLI 和 TUI 兩種互動方式
3. **規範遵循** - 完全支持 Conventional Commits 規範
4. **智慧分析** - 集成 AI 能力，深度理解代碼語義
5. **可擴展性** - 支持插件系統和自訂義模板

### 🛠️ 技術選型

- **語言**: Python 3.7+（標準庫為主）
- **架構**: 模組化設計，便於擴展
- **輸出**: Markdown（預設）、JSON、HTML、YAML
- **版本**: 遵循語義化版本（SemVer）
- **提交**: 遵循 Conventional Commits 規範

### 📅 後續迭代計劃

- [ ] **v1.1.0** - 集成 GLM-5.1 AI 模型，增強變更分析能力
- [ ] **v1.2.0** - 支持更多框架（FastAPI、Django、Tornado）
- [ ] **v1.3.0** - 添加 Web UI 界面
- [ ] **v1.4.0** - 支持 GitHub Actions 集成
- [ ] **v2.0.0** - 添加插件系統和社區模板市場

---

## 📦 打包與部署

### 🐳 Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . /app
RUN pip install -e .

ENTRYPOINT ["api-changelog-pilot"]
```

構建並運行：

```bash
docker build -t api-changelog-pilot .
docker run --rm -v $(pwd):/repo api-changelog-pilot generate
```

### 🔧 GitHub Actions 集成

創建 `.github/workflows/changelog.yml`：

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

## 🤝 貢獻指南

歡迎提交 Pull Request 或創建 Issue！

### 🐛 Bug 報告

請在 [GitHub Issues](https://github.com/gitstq/api-changelog-pilot/issues) 中創建，包含以下資訊：

- 問題描述
- 重現步驟
- 期望行為
- 實際行為
- 環境資訊（Python 版本、作業系統等）

### ✨ 功能請求

歡迎提交功能請求，請描述：

- 功能用途
- 使用場景
- 可能的實現方案

### 🔧 程式碼貢獻

1. Fork 本倉庫
2. 創建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'feat: add amazing feature'`)
4. 推送至分支 (`git push origin feature/amazing-feature`)
5. 創建 Pull Request

---

## 📄 開源協議

本項目採用 [MIT License](LICENSE) 開源協議。

---

## 🙏 致謝

本項目靈感來源於以下優秀項目：

- [Keep a Changelog](https://keepachangelog.com/) - 變更新日誌規範
- [Conventional Commits](https://www.conventionalcommits.org/) - 提交資訊規範
- [Semantic Versioning](https://semver.org/) - 語義化版本規範

---

<p align="center">
  <strong>如果你覺得這個項目有幫助，請給我一個 ⭐️！</strong>
</p>

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>
