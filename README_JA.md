# 🛫 APIChangelog-Pilot

> インテリジェントAPI変更ログ生成・バージョントラッキングエンジン - 軽量、ゼロ依存、自動化

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.7+-green.svg)](https://www.python.org/)
[![Stars](https://img.shields.io/github/stars/gitstq/api-changelog-pilot?style=flat)](https://github.com/gitstq/api-changelog-pilot)
[![Forks](https://img.shields.io/github/forks/gitstq/api-changelog-pilot?style=flat)](https://github.com/gitstq/api-changelog-pilot)

---

🌏 **言語切替** | [简体中文](./README.md) | [繁體中文](./README_TW.md) | [English](./README_EN.md) | [日本語](./README_JA.md)

---

## 🎯 プロジェクト紹介

**APIChangelog-Pilot** は、開発者向けに設計されたインテリジェントツールで、API変更ログの生成与管理を自動化します。コードの変更を自動分析し、変更タイプをインテリジェントに識別し、バージョン履歴を追跡して、業界標準に準拠した変更ログドキュメントを生成します。

### 🔥 コアバリュー

- **🤖 インテリジェント分析** - feat、fix、docsなど複数種類の変更タイプを自動識別
- **⚡ ゼロ依存設計** - Python標準ライブラリのみに依存、箱から出してすぐ使用可能
- **📝 規格準拠** - Conventional Commits仕様に完全対応
- **🔄 バージョントラッキング** - セマンティックバージョニング（SemVer）の自動管理
- **🎨 マルチフォーマット出力** - Markdown、JSON、HTML、YAMLなど複数フォーマット対応
- **💻 TUIインターフェース** - インタラクティブなターミナルインターフェース
- **🔍 変更影響分析** - 変更影響範囲のインテリジェント評価
- **🎯 APIセマンティック理解** - APIエンドポイントとデータモデルの深い理解

### ✨ 他ツールとの差別化ポイント

| 機能 | APIChangelog-Pilot | 他のツール |
|------|-------------------|-----------|
| 依存関係 | 🚀 **ゼロ依存** | npm/yarnなどが必要 |
| AI統合 | ✅ GLM-5.1対応 | ❌ 非対応 |
| APIセマンティクス | ✅ 深い理解 | ❌ テキストのみ |
| TUIインターフェース | ✅ インタラクティブ | ❌ コマンドラインのみ |
| 変更影響 | ✅ インテリジェント評価 | ❌ 基本的な統計 |

---

## 🚀 クイックスタート

### 📋 動作環境

- Python 3.7以上
- Git（バージョン管理機能用）
- ターミナル環境（Bash、Zsh、PowerShellなど）

### ⚡ インストール方法

#### 方法1：pipインストール（推奨）

```bash
pip install api-changelog-pilot
```

#### 方法2：ソースからインストール

```bash
# リポジトリをクローン
git clone https://github.com/gitstq/api-changelog-pilot.git
cd api-changelog-pilot

# インストール
pip install -e .
```

#### 方法3：直接実行

```bash
# リポジトリをクローン
git clone https://github.com/gitstq/api-changelog-pilot.git
cd api-changelog-pilot

# 直接実行
python -m changelog_pilot --help
```

### 🎮 クイック使用法

```bash
# プロジェクト設定を初期化
api-changelog-pilot init

# 変更ログを生成
api-changelog-pilot generate

# バージョン差分を比較
api-changelog-pilot diff --from v1.0 --to v2.0

# 新バージョンをリリース
api-changelog-pilot release --bump minor

# インタラクティブインターフェースを起動
api-changelog-pilot tui
```

---

## 📖 詳細な使用方法

### 1️⃣ 設定の初期化

プロジェクトルートディレクトリで実行：

```bash
api-changelog-pilot init
```

これにより、`.changelogpilot.json`設定ファイルが作成されます。

### 2️⃣ 変更ログの生成

```bash
# 最近のすべての変更を生成
api-changelog-pilot generate

# バージョン範囲を指定
api-changelog-pilot generate --since v1.0.0 --until v2.0.0

# 出力フォーマットを指定
api-changelog-pilot generate --format json

# AI強化分析を有効化
api-changelog-pilot generate --ai
```

### 3️⃣ バージョン管理

```bash
# バージョン一覧を表示
api-changelog-pilot list

# 2つのバージョンを比較
api-changelog-pilot diff --from v1.0.0 --to v2.0.0

# 新バージョンをリリース
api-changelog-pilot release --bump major    # メジャーバージョン更新
api-changelog-pilot release --bump minor    # マイナーバージョン更新
api-changelog-pilot release --bump patch    # パッチ更新

# シミュレーションリリース
api-changelog-pilot release --bump minor --dry-run
```

### 4️⃣ レポート生成

```bash
# Markdownレポートを生成
api-changelog-pilot report --format markdown

# HTMLレポートを生成
api-changelog-pilot report --format html

# ファイルに保存
api-changelog-pilot report --format markdown --output CHANGELOG.md
```

### 5️⃣ 変更影響分析

```bash
# 現在の変更の影響を分析
api-changelog-pilot analyze

# 特定のパスを分析
api-changelog-pilot analyze --path /path/to/api

# 分析結果を保存
api-changelog-pilot analyze --output impact_report.md
```

### 6️⃣ TUIインタラクティブインターフェース

```bash
# インタラクティブインターフェースを起動
api-changelog-pilot tui
```

TUIインターフェースでは：

- 📊 変更統計を表示
- 📝 変更ログを生成
- 🔍 バージョン差分を比較
- 🎯 変更影響を分析
- 📦 新バージョンをリリース
- 📄 レポートをエクスポート
- ⚙️ 設定を管理

---

## 💡 設計思想とロードマップ

### 🎨 設計哲学

1. **シンプルさを優先** - 外部依存ゼロ、Python標準ライブラリのみ使用
2. **ユーザーフレンドリー** - CLIとTUIの両方の対話方式を提供
3. **規格準拠** - Conventional Commits仕様に完全対応
4. **インテリジェント分析** - AI能力を統合、コードセマンティクスを深く理解
5. **拡張性** - プラグインシステムとカスタムテンプレートをサポート

### 🛠️ 技術選定

- **言語**: Python 3.7+（標準ライブラリ中心）
- **アーキテクチャ**: モジュール設計で拡張容易
- **出力**: Markdown（デフォルト）、JSON、HTML、YAML
- **バージョニング**: セマンティックバージョニング（SemVer）準拠
- **コミット**: Conventional Commits仕様準拠

### 📅 今後の開発計画

- [ ] **v1.1.0** - GLM-5.1 AIモデルを統合、変更分析能力を強化
- [ ] **v1.2.0** - 他のフレームワークに対応（FastAPI、Django、Tornado）
- [ ] **v1.3.0** - Web UIインターフェースを追加
- [ ] **v1.4.0** - GitHub Actions統合をサポート
- [ ] **v2.0.0** - プラグインシステムとコミュニティテンプレートマーケットプレイスを追加

---

## 📦 パッケージングとデプロイ

### 🐳 Dockerデプロイ

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . /app
RUN pip install -e .

ENTRYPOINT ["api-changelog-pilot"]
```

ビルドと実行：

```bash
docker build -t api-changelog-pilot .
docker run --rm -v $(pwd):/repo api-changelog-pilot generate
```

### 🔧 GitHub Actions統合

`.github/workflows/changelog.yml`を作成：

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

## 🤝 コントリビューション

Pull RequestやIssueの作成を歓迎します！

### 🐛 バグ報告

[GitHub Issues](https://github.com/gitstq/api-changelog-pilot/issues)で作成し、以下を含めてください：

- 問題の説明
- 再現手順
- 期待される動作
- 実際の動作
- 環境情報（Pythonバージョン、OSなど）

### ✨ 機能リクエスト

機能リクエストも歓迎です！以下を説明してください：

- 機能の目的
- 使用シナリオ
- 考えられる実装方法

### 🔧 コードコントリビューション

1. このリポジトリをFork
2. フィーチャーブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'feat: add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. Pull Requestを作成

---

## 📄 ライセンス

このプロジェクトは[MIT License](LICENSE)でライセンスされています。

---

## 🙏 謝辞

このプロジェクトは以下の優れたプロジェクトに触発されました：

- [Keep a Changelog](https://keepachangelog.com/) - 変更ログ仕様
- [Conventional Commits](https://www.conventionalcommits.org/) - コミットメッセージ仕様
- [Semantic Versioning](https://semver.org/) - セマンティックバージョニング仕様

---

<p align="center">
  <strong>このプロジェクトが役に立ったら、⭐️をください！</strong>
</p>

<p align="center">
  Made with ❤️ by <a href="https://github.com/gitstq">gitstq</a>
</p>
