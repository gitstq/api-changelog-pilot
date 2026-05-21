#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
版本追踪器 - 管理API版本标签和版本历史
"""

import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from datetime import datetime


@dataclass
class Version:
    """语义化版本"""
    major: int
    minor: int
    patch: int
    prerelease: str = ""
    
    def __str__(self) -> str:
        version = f"v{self.major}.{self.minor}.{self.patch}"
        if self.prerelease:
            version += f"-{self.prerelease}"
        return version
    
    @classmethod
    def parse(cls, version_str: str) -> "Version":
        """解析版本字符串"""
        # 移除v前缀
        version_str = version_str.lstrip("v")
        
        # 分割版本号
        parts = version_str.split("-")
        version_parts = parts[0].split(".")
        
        return cls(
            major=int(version_parts[0]) if len(version_parts) > 0 else 0,
            minor=int(version_parts[1]) if len(version_parts) > 1 else 0,
            patch=int(version_parts[2]) if len(version_parts) > 2 else 0,
            prerelease=parts[1] if len(parts) > 1 else ""
        )
    
    def bump_major(self) -> "Version":
        """增加主版本号"""
        return Version(self.major + 1, 0, 0)
    
    def bump_minor(self) -> "Version":
        """增加次版本号"""
        return Version(self.major, self.minor + 1, 0)
    
    def bump_patch(self) -> "Version":
        """增加补丁版本号"""
        return Version(self.major, self.minor, self.patch + 1)


@dataclass
class VersionTag:
    """版本标签"""
    version: Version
    message: str
    commit_hash: str
    author: str
    date: str
    
    @classmethod
    def parse(cls, tag_output: str) -> Optional["VersionTag"]:
        """解析标签输出"""
        lines = tag_output.strip().split("\n")
        if len(lines) < 2:
            return None
        
        version = Version.parse(lines[0])
        
        # 解析详细信息
        details = {}
        for line in lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                details[key.lower()] = value
        
        return cls(
            version=version,
            message=lines[1] if len(lines) > 1 else "",
            commit_hash=details.get("commit", ""),
            author=details.get("tagger", ""),
            date=details.get("date", "")
        )


class VersionTracker:
    """版本追踪器"""
    
    # 标签格式模式
    TAG_PATTERN = r"^v?(\d+)\.(\d+)\.(\d+)(?:-([a-zA-Z0-9.]+))?$"
    
    def __init__(self, config: Optional[Dict] = None):
        """初始化追踪器"""
        self.config = config or {}
        self.repo_path = Path(self.config.get("repo_path", "."))
        self.tag_prefix = self.config.get("tag_prefix", "v")
    
    def list_versions(self) -> List[Version]:
        """列出所有版本"""
        tags = self._get_tags()
        return [tag.version for tag in tags]
    
    def get_latest_version(self) -> Optional[Version]:
        """获取最新版本"""
        versions = self.list_versions()
        if not versions:
            return None
        return max(versions, key=lambda v: (v.major, v.minor, v.patch))
    
    def get_version_tags(self) -> List[VersionTag]:
        """获取版本标签列表"""
        return self._get_tags()
    
    def create_version(
        self,
        version: Version,
        message: str = "",
        dry_run: bool = False
    ) -> Tuple[bool, str]:
        """
        创建新版本标签
        
        Args:
            version: 版本号
            message: 版本消息
            dry_run: 是否模拟运行
        
        Returns:
            (成功标志, 消息)
        """
        tag_name = f"{self.tag_prefix}{version}"
        full_message = message or f"Release {tag_name}"
        
        if dry_run:
            return True, f"[Dry Run] Would create tag: {tag_name}"
        
        try:
            # 创建标签
            subprocess.run(
                ["git", "tag", "-a", tag_name, "-m", full_message],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            
            # 推送标签
            subprocess.run(
                ["git", "push", "origin", tag_name],
                cwd=self.repo_path,
                check=True,
                capture_output=True
            )
            
            return True, f"Created and pushed tag: {tag_name}"
            
        except subprocess.CalledProcessError as e:
            return False, f"Failed to create tag: {e.stderr.decode()}"
    
    def bump_version(
        self,
        bump_type: str,
        message: str = "",
        dry_run: bool = False
    ) -> str:
        """
        增加版本号并创建标签
        
        Args:
            bump_type: 增加类型 (major/minor/patch)
            message: 版本消息
            dry_run: 是否模拟运行
        
        Returns:
            新版本号字符串
        """
        current = self.get_latest_version()
        
        if current is None:
            # 如果没有版本，从0.0.0开始
            current = Version(0, 0, 0)
        
        # 根据类型增加版本
        if bump_type == "major":
            new_version = current.bump_major()
        elif bump_type == "minor":
            new_version = current.bump_minor()
        else:
            new_version = current.bump_patch()
        
        # 创建版本
        success, msg = self.create_version(new_version, message, dry_run)
        
        if not success and not dry_run:
            raise RuntimeError(msg)
        
        return str(new_version)
    
    def compare(
        self,
        from_ref: str,
        to_ref: str,
        filter_type: str = "all"
    ) -> str:
        """
        比较两个版本之间的差异
        
        Args:
            from_ref: 起始版本
            to_ref: 结束版本
            filter_type: 变更类型过滤
        
        Returns:
            差异报告字符串
        """
        try:
            # 获取版本范围
            if from_ref and not from_ref.startswith("v"):
                from_ref = f"v{from_ref}"
            if not to_ref.startswith("v"):
                to_ref = f"v{to_ref}"
            
            # 获取提交历史
            result = subprocess.run(
                ["git", "log", f"{from_ref}..{to_ref}", "--oneline", "--format=%H|%s|%b"],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            lines = result.stdout.strip().split("\n")
            
            # 分析变更
            stats = self._analyze_commits(lines, filter_type)
            
            # 生成报告
            return self._format_diff_report(from_ref, to_ref, stats, lines)
            
        except subprocess.CalledProcessError as e:
            return f"Error comparing versions: {e.stderr.decode()}"
    
    def _get_tags(self) -> List[VersionTag]:
        """获取所有版本标签"""
        try:
            result = subprocess.run(
                [
                    "git", "tag", "-l",
                    "--format=%(refname:short)\n%(objectname:short)\n%(taggername)\n%(taggerdate:iso)\n---\n%(contents)"
                ],
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            tags = []
            tag_parts = result.stdout.split("---\n")
            
            for part in tag_parts:
                if not part.strip():
                    continue
                
                lines = part.strip().split("\n")
                if lines:
                    tag = self._parse_tag_output(lines)
                    if tag:
                        tags.append(tag)
            
            return tags
            
        except subprocess.CalledProcessError:
            return []
    
    def _parse_tag_output(self, lines: List[str]) -> Optional[VersionTag]:
        """解析标签输出"""
        if not lines:
            return None
        
        tag_name = lines[0].strip()
        
        # 检查是否符合版本格式
        if not re.match(self.TAG_PATTERN, tag_name):
            return None
        
        version = Version.parse(tag_name)
        
        return VersionTag(
            version=version,
            message=lines[4] if len(lines) > 4 else "",
            commit_hash=lines[1] if len(lines) > 1 else "",
            author=lines[2] if len(lines) > 2 else "",
            date=lines[3] if len(lines) > 3 else ""
        )
    
    def _analyze_commits(
        self,
        commits: List[str],
        filter_type: str
    ) -> Dict[str, int]:
        """分析提交统计"""
        stats = {
            "added": 0,
            "removed": 0,
            "modified": 0,
            "total": len(commits)
        }
        
        for commit in commits:
            # 简单统计
            if "add" in commit.lower():
                stats["added"] += 1
            elif "remove" in commit.lower():
                stats["removed"] += 1
            else:
                stats["modified"] += 1
        
        return stats
    
    def _format_diff_report(
        self,
        from_ref: str,
        to_ref: str,
        stats: Dict,
        commits: List[str]
    ) -> str:
        """格式化差异报告"""
        lines = []
        
        lines.append("=" * 60)
        lines.append(f"API Version Diff Report: {from_ref} → {to_ref}")
        lines.append("=" * 60)
        lines.append("")
        
        # 统计摘要
        lines.append("📊 Change Statistics")
        lines.append("-" * 40)
        lines.append(f"Total commits: {stats['total']}")
        lines.append(f"  - Added features: {stats['added']}")
        lines.append(f"  - Removed: {stats['removed']}")
        lines.append(f"  - Modified: {stats['modified']}")
        lines.append("")
        
        # 提交列表
        lines.append("📝 Commit History")
        lines.append("-" * 40)
        for commit in commits:
            parts = commit.split("|")
            if len(parts) >= 2:
                commit_hash = parts[0][:7]
                message = parts[1]
                lines.append(f"  - {commit_hash}: {message}")
        lines.append("")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)
    
    def get_version_history(self, limit: int = 10) -> List[Dict]:
        """获取版本历史"""
        tags = self.get_version_tags()
        
        return [
            {
                "version": str(tag.version),
                "date": tag.date,
                "author": tag.author,
                "message": tag.message,
            }
            for tag in sorted(tags, key=lambda t: (t.version.major, t.version.minor, t.version.patch), reverse=True)[:limit]
        ]
