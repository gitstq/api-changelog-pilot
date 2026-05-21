#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
差异分析器 - 分析API代码变更的具体差异
"""

import re
import subprocess
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field
from enum import Enum


class DiffType(Enum):
    """差异类型"""
    ADDED = "added"
    REMOVED = "removed"
    MODIFIED = "modified"
    RENAMED = "renamed"


@dataclass
class DiffFile:
    """差异文件"""
    path: str
    diff_type: DiffType
    additions: int = 0
    deletions: int = 0
    changes: List["CodeChange"] = field(default_factory=list)


@dataclass
class CodeChange:
    """代码变更"""
    line_number: int
    change_type: str  # + 或 -
    content: str
    context: str = ""


@dataclass
class APIModel:
    """API模型/端点"""
    name: str
    type: str  # endpoint, model, parameter
    method: str = ""  # GET, POST, etc.
    path: str = ""
    description: str = ""
    changes: List[str] = field(default_factory=list)


class DiffAnalyzer:
    """差异分析器"""
    
    # API相关文件模式
    API_PATTERNS = [
        r"api.*\.py$",
        r"routes?.*\.py$",
        r"endpoints?.*\.py$",
        r"views?.*\.py$",
        r"controllers?.*\.py$",
        r"models?.*\.py$",
        r"schemas?.*\.py$",
        r"serializers?.*\.py$",
        r"resources?.*\.py$",
        r"handlers?.*\.py$",
        r"\.api\.",
        r"\.rest\.",
        r"\.graphql\.",
    ]
    
    # HTTP方法
    HTTP_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]
    
    def __init__(self, config: Optional[Dict] = None):
        """初始化分析器"""
        self.config = config or {}
        self.repo_path = Path(self.config.get("repo_path", "."))
        self.api_patterns = self.config.get("api_patterns", self.API_PATTERNS)
    
    def analyze(
        self,
        since: Optional[str] = None,
        until: str = "HEAD"
    ) -> Dict:
        """
        分析变更
        
        Args:
            since: 起始版本
            until: 结束版本
        
        Returns:
            分析结果字典
        """
        diff_files = self._get_diff_files(since, until)
        
        # 过滤API相关文件
        api_files = self._filter_api_files(diff_files)
        
        # 分析每个文件的变更
        analyzed = []
        for diff_file in api_files:
            result = self._analyze_file(diff_file, since, until)
            if result:
                analyzed.append(result)
        
        return {
            "total_files": len(api_files),
            "files": analyzed,
            "summary": self._generate_summary(analyzed)
        }
    
    def _get_diff_files(
        self,
        since: Optional[str],
        until: str
    ) -> List[DiffFile]:
        """获取差异文件列表"""
        try:
            # 获取变更的文件列表
            cmd = ["git", "diff", "--name-status"]
            if since:
                cmd.append(f"{since}..{until}")
            else:
                cmd.append(f"--all")
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            files = []
            for line in result.stdout.strip().split("\n"):
                if not line:
                    continue
                
                parts = line.split("\t")
                if len(parts) >= 2:
                    status = parts[0]
                    path = parts[1]
                    
                    # 解析状态
                    if status.startswith("R"):
                        diff_type = DiffType.RENAMED
                    elif status == "A":
                        diff_type = DiffType.ADDED
                    elif status == "D":
                        diff_type = DiffType.REMOVED
                    else:
                        diff_type = DiffType.MODIFIED
                    
                    files.append(DiffFile(
                        path=path,
                        diff_type=diff_type
                    ))
            
            return files
            
        except subprocess.CalledProcessError:
            return []
    
    def _filter_api_files(self, files: List[DiffFile]) -> List[DiffFile]:
        """过滤API相关文件"""
        filtered = []
        
        for file in files:
            for pattern in self.api_patterns:
                if re.search(pattern, file.path, re.IGNORECASE):
                    filtered.append(file)
                    break
        
        return filtered
    
    def _analyze_file(
        self,
        diff_file: DiffFile,
        since: Optional[str],
        until: str
    ) -> Optional[Dict]:
        """分析单个文件的变更"""
        try:
            # 获取文件差异详情
            cmd = ["git", "diff"]
            if since:
                cmd.append(f"{since}..{until}")
            cmd.extend(["--", diff_file.path])
            
            result = subprocess.run(
                cmd,
                cwd=self.repo_path,
                capture_output=True,
                text=True,
                check=True
            )
            
            diff_content = result.stdout
            
            # 解析差异统计
            additions = diff_content.count("\n+") - diff_content.count("\n++")
            deletions = diff_content.count("\n-") - diff_content.count("\n--")
            
            diff_file.additions = additions
            diff_file.deletions = deletions
            
            # 提取关键变更
            changes = self._extract_key_changes(diff_content)
            diff_file.changes = changes
            
            # 提取API端点
            endpoints = self._extract_endpoints(diff_content)
            
            return {
                "path": diff_file.path,
                "type": diff_file.diff_type.value,
                "additions": additions,
                "deletions": deletions,
                "changes": changes,
                "endpoints": endpoints
            }
            
        except subprocess.CalledProcessError:
            return None
    
    def _extract_key_changes(self, diff_content: str) -> List[str]:
        """提取关键变更"""
        changes = []
        
        lines = diff_content.split("\n")
        for line in lines:
            # 只分析变更行
            if line.startswith("+") and not line.startswith("++"):
                content = line[1:].strip()
                if content:
                    changes.append(f"+ {content}")
            elif line.startswith("-") and not line.startswith("--"):
                content = line[1:].strip()
                if content:
                    changes.append(f"- {content}")
        
        return changes[:50]  # 限制数量
    
    def _extract_endpoints(self, diff_content: str) -> List[Dict]:
        """提取API端点"""
        endpoints = []
        
        lines = diff_content.split("\n")
        for line in lines:
            # 检测HTTP方法定义
            for method in self.HTTP_METHODS:
                if f'["{method}"]' in line or f"['{method}']" in line:
                    endpoints.append({
                        "method": method,
                        "pattern": line.strip()
                    })
                    break
            
            # 检测路由定义
            route_match = re.search(r'["\'](/[^"\']+)["\']', line)
            if route_match:
                endpoints.append({
                    "type": "route",
                    "path": route_match.group(1)
                })
        
        return endpoints[:10]  # 限制数量
    
    def _generate_summary(self, analyzed: List[Dict]) -> Dict:
        """生成变更摘要"""
        total_additions = sum(f.get("additions", 0) for f in analyzed)
        total_deletions = sum(f.get("deletions", 0) for f in analyzed)
        
        changes_by_type = {
            "added": 0,
            "modified": 0,
            "removed": 0,
            "renamed": 0
        }
        
        for file in analyzed:
            file_type = file.get("type", "modified")
            if file_type in changes_by_type:
                changes_by_type[file_type] += 1
        
        return {
            "total_additions": total_additions,
            "total_deletions": total_deletions,
            "net_changes": total_additions - total_deletions,
            "changes_by_type": changes_by_type
        }
    
    def analyze_impact(
        self,
        since: Optional[str] = None,
        until: str = "HEAD"
    ) -> Dict:
        """分析变更影响"""
        analysis = self.analyze(since, until)
        
        # 评估影响范围
        impact = {
            "severity": "low",  # low, medium, high, critical
            "affected_endpoints": set(),
            "affected_models": set(),
            "breaking_changes": [],
            "recommendations": []
        }
        
        for file_result in analysis.get("files", []):
            # 检查破坏性变更
            if file_result.get("deletions", 0) > file_result.get("additions", 0):
                impact["severity"] = "medium"
                impact["breaking_changes"].append({
                    "file": file_result["path"],
                    "reason": "More deletions than additions"
                })
            
            # 收集受影响的端点
            for endpoint in file_result.get("endpoints", []):
                if "method" in endpoint:
                    impact["affected_endpoints"].add(
                        f"{endpoint['method']} {endpoint.get('path', '')}"
                    )
        
        # 根据变更数量评估严重性
        if analysis.get("total_files", 0) > 10:
            impact["severity"] = "high"
            impact["recommendations"].append("Consider a major version bump")
        
        if len(impact["breaking_changes"]) > 3:
            impact["severity"] = "critical"
            impact["recommendations"].append("Breaking changes detected - review carefully")
        
        # 转换为列表
        impact["affected_endpoints"] = list(impact["affected_endpoints"])
        
        return {
            **analysis,
            "impact": impact
        }
