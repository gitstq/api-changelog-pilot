#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
配置管理模块 - 管理APIChangelog-Pilot的配置
"""

import json
from pathlib import Path
from typing import Any, Dict, Optional


class Config:
    """配置管理类"""
    
    DEFAULT_CONFIG = {
        "repo_path": ".",
        "output_format": "markdown",
        "tag_prefix": "v",
        "include_scope": True,
        "group_by_scope": True,
        "ai_enabled": False,
        "ai_model": "glm-5.1",
        "ai_api_key": "",
        "verbose": False,
        "output_dir": ".",
        "changelog_file": "CHANGELOG.md",
        "conventional_commits": True,
        "breaking_change_indicators": [
            "BREAKING CHANGE",
            "breaking",
            "!:"
        ],
        "commit_types": {
            "feat": {"title": "Features", "description": "New features"},
            "fix": {"title": "Bug Fixes", "description": "Bug fixes"},
            "docs": {"title": "Documentation", "description": "Documentation changes"},
            "style": {"title": "Styles", "description": "Code style changes"},
            "refactor": {"title": "Code Refactoring", "description": "Code refactoring"},
            "perf": {"title": "Performance Improvements", "description": "Performance improvements"},
            "test": {"title": "Tests", "description": "Test updates"},
            "build": {"title": "Builds", "description": "Build system changes"},
            "ci": {"title": "Continuous Integration", "description": "CI/CD changes"},
            "chore": {"title": "Maintenance", "description": "Maintenance tasks"}
        },
        "api_patterns": [
            "api.*\\.py$",
            "routes?.*\\.py$",
            "endpoints?.*\\.py$",
            "views?.*\\.py$",
            "controllers?.*\\.py$",
            "models?.*\\.py$",
            "schemas?.*\\.py$"
        ],
        "ignore_patterns": [
            "**/test*/**",
            "**/tests/**",
            "**/__pycache__/**",
            "**/node_modules/**",
            "**/.venv/**",
            "**/venv/**"
        ],
        "release_template": "# Release {version}\n\n{changes}\n\n---\n",
        "changelog_template": "# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n## [Unreleased]\n\n{changes}\n"
    }
    
    def __init__(self, config_dict: Optional[Dict] = None):
        """初始化配置"""
        self._config = config_dict or self.DEFAULT_CONFIG.copy()
    
    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split(".")
        value = self._config
        
        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default
            
            if value is None:
                return default
        
        return value
    
    def set(self, key: str, value: Any):
        """设置配置值"""
        keys = key.split(".")
        config = self._config
        
        for k in keys[:-1]:
            if k not in config:
                config[k] = {}
            config = config[k]
        
        config[keys[-1]] = value
    
    def update(self, updates: Dict):
        """批量更新配置"""
        self._config.update(updates)
    
    def to_dict(self) -> Dict:
        """转换为字典"""
        return self._config.copy()
    
    def init_default(self):
        """初始化默认配置"""
        self._config = self.DEFAULT_CONFIG.copy()
    
    def load(self, path: Path):
        """从文件加载配置"""
        config_path = Path(path)
        
        if not config_path.exists():
            return
        
        try:
            if config_path.suffix == ".json":
                self._load_json(config_path)
            elif config_path.suffix in [".yaml", ".yml"]:
                self._load_yaml(config_path)
            else:
                # 尝试JSON
                self._load_json(config_path)
        except Exception as e:
            print(f"Failed to load config: {e}")
    
    def _load_json(self, path: Path):
        """加载JSON配置"""
        with open(path, "r", encoding="utf-8") as f:
            self._config.update(json.load(f))
    
    def _load_yaml(self, path: Path):
        """加载YAML配置"""
        try:
            import yaml
            with open(path, "r", encoding="utf-8") as f:
                self._config.update(yaml.safe_load(f))
        except ImportError:
            print("PyYAML not installed, falling back to JSON")
            self._load_json(path)
    
    def save(self, path: Path):
        """保存配置到文件"""
        config_path = Path(path)
        
        # 确保父目录存在
        config_path.parent.mkdir(parents=True, exist_ok=True)
        
        if config_path.suffix == ".json":
            self._save_json(config_path)
        elif config_path.suffix in [".yaml", ".yml"]:
            self._save_yaml(config_path)
        else:
            self._save_json(config_path)
    
    def _save_json(self, path: Path):
        """保存为JSON"""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self._config, f, indent=2, ensure_ascii=False)
    
    def _save_yaml(self, path: Path):
        """保存为YAML"""
        try:
            import yaml
            with open(path, "w", encoding="utf-8") as f:
                yaml.dump(self._config, f, default_flow_style=False, allow_unicode=True)
        except ImportError:
            print("PyYAML not installed, saving as JSON")
            self._save_json(path.with_suffix(".json"))
    
    def validate(self) -> bool:
        """验证配置"""
        required_keys = ["repo_path", "output_format"]
        
        for key in required_keys:
            if key not in self._config:
                print(f"Missing required config key: {key}")
                return False
        
        return True
