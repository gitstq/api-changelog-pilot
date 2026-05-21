# 🤝 APIChangelog-Pilot 贡献指南

感谢您对 APIChangelog-Pilot 的关注！我们欢迎各种形式的贡献，包括但不限于：

- 🐛 Bug 报告
- ✨ 功能请求
- 📝 文档改进
- 💻 代码贡献
- 🌍 翻译支持

---

## 📋 贡献前准备

### 开发环境

```bash
# 1. Fork 本仓库
# 2. 克隆你的 Fork
git clone https://github.com/YOUR_USERNAME/api-changelog-pilot.git
cd api-changelog-pilot

# 3. 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或 venv\Scripts\activate  # Windows

# 4. 安装开发依赖
pip install -e ".[dev]"

# 5. 安装pre-commit钩子
pre-commit install
```

### 代码规范

我们使用以下工具来保持代码质量：

- **Black** - 代码格式化
- **isort** - import 排序
- **flake8** - 代码检查
- **mypy** - 类型检查
- **pytest** - 单元测试

运行代码检查：

```bash
# 格式化代码
black .

# 排序imports
isort .

# 运行检查
flake8 .

# 类型检查
mypy .

# 运行测试
pytest .

# 全部检查
pre-commit run --all-files
```

---

## 🐛 Bug 报告

在报告 Bug 时，请包含：

1. **清晰的标题和描述**
2. **复现步骤**（用编号列表）
3. **预期行为 vs 实际行为**
4. **环境信息**：
   - 操作系统和版本
   - Python 版本
   - APIChangelog-Pilot 版本
5. **相关日志或截图**（如果有）

请使用 [GitHub Issues](https://github.com/gitstq/api-changelog-pilot/issues) 提交 Bug。

---

## ✨ 功能请求

在提交功能请求时，请包含：

1. **功能描述** - 清晰、简洁地描述功能
2. **使用场景** - 这个功能解决什么问题？
3. **可能的实现方案** - 你有什么想法？
4. **替代方案** - 有没有其他方法可以实现？

---

## 💻 代码贡献流程

### 1. 创建分支

```bash
# 基于 main 创建分支
git checkout main
git pull origin main
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

分支命名规范：

- `feature/` - 新功能
- `fix/` - Bug 修复
- `docs/` - 文档更新
- `refactor/` - 代码重构
- `test/` - 测试相关

### 2. 编写代码

- 遵循 [PEP 8](https://www.python.org/dev/peps/pep-0008/) 代码风格
- 添加必要的注释和文档字符串
- 为新功能编写单元测试
- 确保所有测试通过

### 3. 提交更改

我们使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

```
<type>(<scope>): <subject>

<body>

<footer>
```

类型 (type)：

- `feat` - 新功能
- `fix` - Bug 修复
- `docs` - 文档变更
- `style` - 代码格式（不影响功能）
- `refactor` - 重构
- `perf` - 性能优化
- `test` - 测试相关
- `build` - 构建系统或依赖更新
- `ci` - CI/CD 相关
- `chore` - 其他更改

示例：

```bash
# 新功能
git commit -m "feat(api): add OpenAPI schema generation"

# Bug 修复
git commit -m "fix(tui): resolve display issue in Windows terminal"

# 文档更新
git commit -m "docs: update installation instructions"
```

### 4. 推送并创建 PR

```bash
# 推送分支
git push origin feature/your-feature-name
```

然后在 GitHub 上创建 Pull Request。

### 5. Pull Request 审查

- 描述你做了哪些更改
- 链接相关的 Issue
- 确保所有 CI 检查通过
- 等待代码审查

---

## 🧪 测试指南

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_core.py

# 运行特定测试
pytest tests/test_core.py::TestVersion::test_version_parse

# 生成覆盖率报告
pytest --cov=changelog_pilot --cov-report=html
```

### 编写测试

```python
import pytest
from changelog_pilot import ChangelogGenerator

def test_generate_changelog():
    """测试变更日志生成"""
    generator = ChangelogGenerator()
    changelog = generator.generate()
    
    assert changelog is not None
    assert isinstance(changelog, str)
```

---

## 🌐 翻译指南

我们欢迎多语言翻译贡献！

### 支持的语言

- ✅ 简体中文 (Simplified Chinese)
- ✅ 繁体中文 (Traditional Chinese)
- ✅ English
- ✅ 日本語 (Japanese)
- 🔄 更多语言...

### 翻译文件位置

- `README.md` - 简体中文（主版本）
- `README_TW.md` - 繁体中文
- `README_EN.md` - English
- `README_JA.md` - 日本語

### 翻译规范

1. 保持与原版相同的结构
2. 使用母语级表达，避免生硬翻译
3. 保持代码示例不变
4. 更新文件顶部的语言切换链接

---

## 📝 文档贡献

文档改进包括：

- 修正拼写或语法错误
- 改进解释的清晰度
- 添加缺失的示例
- 更新过时的信息
- 翻译文档到其他语言

---

## ❓ 问题与帮助

如果您有任何问题：

1. 查看 [README.md](./README.md) 和文档
2. 搜索 [已有的 Issues](https://github.com/gitstq/api-changelog-pilot/issues)
3. 创建新的 Issue

---

## 📜 许可证

通过贡献代码，您同意您的贡献将遵循 [MIT 许可证](../LICENSE)。

---

<p align="center">
  <strong>感谢您的贡献！让我们一起让 APIChangelog-Pilot 变得更好！</strong>
</p>
