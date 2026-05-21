#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APIChangelog-Pilot 测试文件
"""

import pytest
from changelog_pilot.changelog import ChangelogGenerator, ChangeType, ChangeEntry
from changelog_pilot.version_tracker import VersionTracker, Version
from changelog_pilot.config import Config
from changelog_pilot.diff_analyzer import DiffAnalyzer
from changelog_pilot.semantic_parser import SemanticParser


class TestVersion:
    """版本测试"""
    
    def test_version_parse(self):
        """测试版本解析"""
        v = Version.parse("v1.2.3")
        assert v.major == 1
        assert v.minor == 2
        assert v.patch == 3
    
    def test_version_bump(self):
        """测试版本递增"""
        v = Version(1, 2, 3)
        
        assert str(v.bump_major()) == "v2.0.0"
        assert str(v.bump_minor()) == "v1.3.0"
        assert str(v.bump_patch()) == "v1.2.4"
    
    def test_version_str(self):
        """测试版本字符串"""
        v = Version(1, 0, 0)
        assert str(v) == "v1.0.0"
        
        v = Version(1, 0, 0, "beta")
        assert str(v) == "v1.0.0-beta"


class TestChangelogGenerator:
    """变更日志生成器测试"""
    
    def test_parse_conventional_commit(self):
        """测试解析Conventional Commits格式"""
        config = Config().to_dict()
        generator = ChangelogGenerator(config)
        
        commits = [
            {
                "hash": "abc123",
                "subject": "feat(api): add new endpoint",
                "body": "",
                "author": "Test Author",
                "date": "2025-01-01"
            }
        ]
        
        changes = generator._parse_commits(commits)
        
        assert len(changes) == 1
        assert changes[0].type == ChangeType.MINOR
        assert "api" in changes[0].scope
    
    def test_parse_breaking_change(self):
        """测试解析破坏性变更"""
        config = Config().to_dict()
        generator = ChangelogGenerator(config)
        
        commits = [
            {
                "hash": "abc123",
                "subject": "feat!: remove deprecated API",
                "body": "BREAKING CHANGE: This is a breaking change",
                "author": "Test Author",
                "date": "2025-01-01"
            }
        ]
        
        changes = generator._parse_commits(commits)
        
        assert len(changes) == 1
        assert changes[0].breaking == True


class TestConfig:
    """配置测试"""
    
    def test_default_config(self):
        """测试默认配置"""
        config = Config()
        
        assert config.get("repo_path") == "."
        assert config.get("output_format") == "markdown"
        assert config.get("tag_prefix") == "v"
    
    def test_get_set(self):
        """测试获取和设置配置"""
        config = Config()
        
        config.set("test_key", "test_value")
        assert config.get("test_key") == "test_value"
        
        config.set("nested.key", "nested_value")
        assert config.get("nested.key") == "nested_value"
    
    def test_to_dict(self):
        """测试转换为字典"""
        config = Config()
        config.set("test", "value")
        
        d = config.to_dict()
        assert "test" in d
        assert d["test"] == "value"


class TestDiffAnalyzer:
    """差异分析器测试"""
    
    def test_api_file_detection(self):
        """测试API文件检测"""
        analyzer = DiffAnalyzer()
        
        assert analyzer._filter_api_files([
            DiffFile(path="api/routes.py", diff_type=DiffType.MODIFIED)
        ])


class TestSemanticParser:
    """语义解析器测试"""
    
    def test_type_annotation(self):
        """测试类型注解解析"""
        parser = SemanticParser()
        
        # 测试基本类型
        assert parser._get_type_annotation(None) == "Any"
    
    def test_auto_detect_framework(self):
        """测试自动检测框架"""
        parser = SemanticParser()
        
        # 使用项目路径
        framework = parser._detect_framework()
        assert framework in ["flask", "fastapi", "django", "bottle", "tornado", "unknown"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
