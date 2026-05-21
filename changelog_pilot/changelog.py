#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
变更日志生成器 - 智能分析代码变更并生成规范的变更日志
"""

import re
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, field
from enum import Enum


class ChangeType(Enum):
    """变更类型枚举"""
    MAJOR = "major"          # 破坏性变更
    MINOR = "minor"          # 新功能
    PATCH = "patch"          # 修复
    DEPRECATED = "deprecated"  # 废弃
    REMOVED = "removed"      # 移除
    SECURITY = "security"    # 安全修复
    PERFORMANCE = "performance"  # 性能优化
    DOCUMENTATION = "documentation"  # 文档更新
    BUILD = "build"          # 构建系统
    CI = "ci"                # CI/CD


@dataclass
class ChangeEntry:
    """变更条目"""
    type: ChangeType
    scope: str
    subject: str
    body: str = ""
    breaking: bool = False
    commit_hash: str = ""
    author: str = ""
    date: str = ""
    issues: List[str] = field(default_factory=list)
    scope_impact: Dict[str, any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return {
            "type": self.type.value,
            "scope": self.scope,
            "subject": self.subject,
            "body": self.body,
            "breaking": self.breaking,
            "commit_hash": self.commit_hash,
            "author": self.author,
            "date": self.date,
            "issues": self.issues,
        }


@dataclass
class ChangelogSection:
    """变更日志区块"""
    title: str
    changes: List[ChangeEntry] = field(default_factory=list)
    
    def add_change(self, change: ChangeEntry):
        """添加变更"""
        self.changes.append(change)


class ChangelogGenerator:
    """变更日志生成器"""
    
    # 变更类型到标题的映射
    TYPE_TITLES = {
        ChangeType.MAJOR: "💥 Breaking Changes",
        ChangeType.MINOR: "✨ New Features",
        ChangeType.PATCH: "🐛 Bug Fixes",
        ChangeType.DEPRECATED: "⚠️ Deprecations",
        ChangeType.REMOVED: "🗑️ Removed",
        ChangeType.SECURITY: "🔒 Security",
        ChangeType.PERFORMANCE: "⚡ Performance",
        ChangeType.DOCUMENTATION: "📝 Documentation",
        ChangeType.BUILD: "👷 Build System",
        ChangeType.CI: "🔄 CI/CD",
    }
    
    # Conventional Commits 类型映射
    COMMIT_TYPE_MAP = {
        "feat": ChangeType.MINOR,
        "feature": ChangeType.MINOR,
        "fix": ChangeType.PATCH,
        "docs": ChangeType.DOCUMENTATION,
        "style": ChangeType.PATCH,
        "refactor": ChangeType.PATCH,
        "perf": ChangeType.PERFORMANCE,
        "test": ChangeType.PATCH,
        "build": ChangeType.BUILD,
        "ci": ChangeType.CI,
        "chore": ChangeType.PATCH,
        "revert": ChangeType.PATCH,
        "breaking": ChangeType.MAJOR,
        "security": ChangeType.SECURITY,
        "deprecate": ChangeType.DEPRECATED,
        "remove": ChangeType.REMOVED,
    }
    
    # API相关关键词
    API_KEYWORDS = [
        "api", "endpoint", "route", "handler", "controller",
        "request", "response", "method", "http", "rest", "graphql",
        "payload", "schema", "model", "serializer", "middleware"
    ]
    
    def __init__(self, config: Optional[Dict] = None):
        """初始化生成器"""
        self.config = config or {}
        self.repo_path = Path(self.config.get("repo_path", "."))
        self.include_scope = self.config.get("include_scope", True)
        self.group_by_scope = self.config.get("group_by_scope", True)
        self.breaking_changes = []
        
    def generate(
        self,
        since: Optional[str] = None,
        until: str = "HEAD",
        use_ai: bool = False
    ) -> str:
        """
        生成变更日志
        
        Args:
            since: 起始版本/标签
            until: 结束版本/标签
            use_ai: 是否使用AI分析
        
        Returns:
            格式化的变更日志字符串
        """
        # 获取提交历史
        commits = self._get_commits(since, until)
        
        # 解析提交信息
        changes = self._parse_commits(commits)
        
        # 按类型分组
        sections = self._group_by_type(changes)
        
        # 检测破坏性变更
        self._detect_breaking_changes(sections)
        
        # 如果启用AI分析，进行深度分析
        if use_ai:
            sections = self._ai_enhance(sections, commits)
        
        # 生成格式化的日志
        return self._format_changelog(sections, since, until)
    
    def _get_commits(self, since: Optional[str], until: str) -> List[Dict]:
        """获取提交历史"""
        cmd = ["git", "log", "--format=%H|%s|%b|%an|%ad|%ae", "--date=iso"]
        
        if since:
            cmd.append(f"{since}..{until}")
        else:
            cmd.append(f"--all")
        
        try:
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            commits = []
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                    
                parts = line.split("|")
                if len(parts) >= 5:
                    commits.append({
                        "hash": parts[0],
                        "subject": parts[1],
                        "body": parts[2] if len(parts) > 2 else "",
                        "author": parts[3],
                        "date": parts[4],
                        "email": parts[5] if len(parts) > 5 else "",
                    })
            
            return commits
        except subprocess.CalledProcessError:
            # 如果不是git仓库，返回空列表
            return []
    
    def _parse_commits(self, commits: List[Dict]) -> List[ChangeEntry]:
        """解析提交信息为变更条目"""
        changes = []
        
        for commit in commits:
            entry = self._parse_commit(commit)
            if entry:
                changes.append(entry)
        
        return changes
    
    def _parse_commit(self, commit: Dict) -> Optional[ChangeEntry]:
        """解析单个提交"""
        subject = commit.get("subject", "")
        body = commit.get("body", "")
        
        # 跳过合并提交和回退提交
        if subject.startswith("Merge") or subject.startswith("Revert"):
            return None
        
        # 解析 Conventional Commits 格式
        pattern = r'^(\w+)(?:\(([^)]+)\))?(!)?:\s*(.+)$'
        match = re.match(pattern, subject)
        
        if match:
            commit_type = match.group(1).lower()
            scope = match.group(2) or "general"
            breaking = match.group(3) == "!" or "BREAKING CHANGE" in body
            description = match.group(4)
        else:
            # 尝试自动检测
            commit_type, scope, description = self._auto_detect_type(subject)
            breaking = "BREAKING CHANGE" in body
        
        # 检测API相关变更
        is_api_change = any(
            kw in subject.lower() or kw in body.lower()
            for kw in self.API_KEYWORDS
        )
        
        if is_api_change:
            scope = "api"
        
        change_type = self.COMMIT_TYPE_MAP.get(commit_type, ChangeType.PATCH)
        
        # 提取关联的Issue
        issues = re.findall(r"#(\d+)", f"{subject} {body}")
        
        return ChangeEntry(
            type=change_type,
            scope=scope,
            subject=description,
            body=body,
            breaking=breaking,
            commit_hash=commit.get("hash", "")[:7],
            author=commit.get("author", ""),
            date=commit.get("date", ""),
            issues=issues
        )
    
    def _auto_detect_type(self, text: str) -> Tuple[str, str, str]:
        """自动检测提交类型"""
        text_lower = text.lower()
        
        # 检测类型
        if any(kw in text_lower for kw in ["add", "new", "introduce", "implement"]):
            commit_type = "feat"
        elif any(kw in text_lower for kw in ["fix", "bug", "patch"]):
            commit_type = "fix"
        elif any(kw in text_lower for kw in ["deprecate", "obsolete"]):
            commit_type = "deprecate"
        elif any(kw in text_lower for kw in ["remove", "delete", "drop"]):
            commit_type = "remove"
        elif any(kw in text_lower for kw in ["security", "vulnerability"]):
            commit_type = "security"
        elif any(kw in text_lower for kw in ["doc", "readme", "comment"]):
            commit_type = "docs"
        elif any(kw in text_lower for kw in ["refactor", "restructure"]):
            commit_type = "refactor"
        elif any(kw in text_lower for kw in ["perf", "optimize", "speed"]):
            commit_type = "perf"
        else:
            commit_type = "chore"
        
        # 提取scope（从括号中）
        scope_match = re.search(r'\(([^)]+)\)', text)
        scope = scope_match.group(1) if scope_match else "general"
        
        # 清理描述
        description = re.sub(r'^\w+(?:\([^)]+\))?!?:\s*', '', text)
        
        return commit_type, scope, description
    
    def _group_by_type(self, changes: List[ChangeEntry]) -> Dict[ChangeType, List[ChangeEntry]]:
        """按类型分组"""
        grouped = {}
        
        for change in changes:
            if change.type not in grouped:
                grouped[change.type] = []
            grouped[change.type].append(change)
        
        return grouped
    
    def _detect_breaking_changes(self, sections: Dict[ChangeType, List[ChangeEntry]]):
        """检测破坏性变更"""
        for change_type, changes in sections.items():
            for change in changes:
                if change.breaking:
                    self.breaking_changes.append(change)
    
    def _ai_enhance(
        self,
        sections: Dict[ChangeType, List[ChangeEntry]],
        commits: List[Dict]
    ) -> Dict[ChangeType, List[ChangeEntry]]:
        """
        使用AI增强变更分析
        
        注意: 这里需要集成GLM-5.1或其他AI模型
        当前实现为占位符
        """
        # TODO: 集成AI模型进行深度分析
        # 1. 分析变更影响范围
        # 2. 生成更详细的描述
        # 3. 提供迁移建议
        
        return sections
    
    def _format_changelog(
        self,
        sections: Dict[ChangeType, List[ChangeEntry]],
        since: Optional[str],
        until: str
    ) -> str:
        """格式化变更日志"""
        lines = []
        
        # 标题
        lines.append("# API Changelog")
        lines.append("")
        
        # 版本信息
        if since:
            lines.append(f"## [{since}] - {datetime.now().strftime('%Y-%m-%d')}")
        else:
            lines.append(f"## Unreleased")
        lines.append("")
        
        # 输出破坏性变更警告
        if self.breaking_changes:
            lines.append("> ### ⚠️ Breaking Changes Detected!")
            for change in self.breaking_changes:
                lines.append(f"> - {change.scope}: {change.subject}")
            lines.append("")
        
        # 按优先级输出各类型变更
        priority_types = [
            ChangeType.MAJOR,
            ChangeType.MINOR,
            ChangeType.PATCH,
            ChangeType.DEPRECATED,
            ChangeType.REMOVED,
            ChangeType.SECURITY,
            ChangeType.PERFORMANCE,
            ChangeType.DOCUMENTATION,
            ChangeType.BUILD,
            ChangeType.CI,
        ]
        
        has_content = False
        
        for change_type in priority_types:
            if change_type not in sections or not sections[change_type]:
                continue
            
            has_content = True
            title = self.TYPE_TITLES.get(change_type, change_type.value)
            lines.append(f"### {title}")
            lines.append("")
            
            # 按scope分组（可选）
            if self.group_by_scope:
                scoped_changes = {}
                for change in sections[change_type]:
                    if change.scope not in scoped_changes:
                        scoped_changes[change.scope] = []
                    scoped_changes[change.scope].append(change)
                
                for scope, scope_changes in scoped_changes.items():
                    if scope != "general":
                        lines.append(f"#### {scope}")
                        lines.append("")
                    
                    for change in scope_changes:
                        lines.append(self._format_change_entry(change))
                    lines.append("")
            else:
                for change in sections[change_type]:
                    lines.append(self._format_change_entry(change))
                lines.append("")
        
        if not has_content:
            lines.append("*No changes in this release.*")
            lines.append("")
        
        # 页脚
        lines.append("---")
        lines.append("")
        lines.append("*Generated by APIChangelog-Pilot*")
        
        return "\n".join(lines)
    
    def _format_change_entry(self, change: ChangeEntry) -> str:
        """格式化单个变更条目"""
        lines = []
        
        # 主体
        subject = f"- {change.subject}"
        if change.commit_hash:
            subject += f" (`{change.commit_hash}`)"
        if change.breaking:
            subject = "💥 " + subject
        lines.append(subject)
        
        # 详细信息
        if change.body:
            for line in change.body.strip().split("\n"):
                lines.append(f"  {line.strip()}")
        
        # Issue链接
        if change.issues:
            issue_links = ", ".join(f"[#{issue}](https://github.com/issues/{issue})" 
                                    for issue in change.issues)
            lines.append(f"  - Issues: {issue_links}")
        
        return "\n".join(lines)
    
    def generate_report(self, format_type: str = "markdown", **kwargs) -> str:
        """生成变更报告"""
        changelog = self.generate(use_ai=kwargs.get("use_ai", False))
        
        if format_type == "markdown":
            return changelog
        elif format_type == "json":
            return self._to_json()
        elif format_type == "html":
            return self._to_html(changelog)
        elif format_type == "yaml":
            return self._to_yaml()
        
        return changelog
    
    def _to_json(self) -> str:
        """转换为JSON格式"""
        import json
        
        data = {
            "generated_at": datetime.now().isoformat(),
            "version": "unreleased",
            "changes": {
                ctype.value: [c.to_dict() for c in changes]
                for ctype, changes in self._group_by_type([]).items()
            }
        }
        
        return json.dumps(data, indent=2, ensure_ascii=False)
    
    def _to_html(self, markdown_content: str) -> str:
        """转换为HTML格式"""
        # 简单的Markdown到HTML转换
        html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>API Changelog</title>
    <style>
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; max-width: 800px; margin: 0 auto; padding: 20px; }}
        h1 {{ color: #333; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
        h2 {{ color: #555; margin-top: 30px; }}
        h3 {{ color: #666; margin-left: 10px; }}
        ul {{ list-style-type: none; padding-left: 0; }}
        li {{ margin: 10px 0; padding: 10px; background: #f9f9f9; border-radius: 5px; }}
        code {{ background: #eee; padding: 2px 5px; border-radius: 3px; }}
        .breaking {{ background: #fff3cd; border-left: 4px solid #ffc107; }}
        blockquote {{ background: #f0f0f0; padding: 10px; border-left: 4px solid #007bff; }}
    </style>
</head>
<body>
    <pre>{markdown_content}</pre>
</body>
</html>"""
        return html
    
    def _to_yaml(self) -> str:
        """转换为YAML格式"""
        import yaml
        
        data = {
            "changelog": {
                "version": "unreleased",
                "date": datetime.now().strftime("%Y-%m-%d"),
                "changes": {}
            }
        }
        
        return yaml.dump(data, allow_unicode=True, default_flow_style=False)
