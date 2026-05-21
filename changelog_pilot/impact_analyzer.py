#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
变更影响分析器 - 分析API变更的影响范围
"""

from pathlib import Path
from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum


class ImpactLevel(Enum):
    """影响等级"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class ChangeImpact:
    """变更影响"""
    level: ImpactLevel
    affected_components: List[str]
    affected_endpoints: List[str]
    affected_models: List[str]
    recommendations: List[str]
    breaking_changes: List[str]


class ImpactAnalyzer:
    """变更影响分析器"""
    
    def __init__(self, config: Optional[Dict] = None):
        """初始化分析器"""
        self.config = config or {}
        self.project_path = Path(self.config.get("project_path", "."))
    
    def analyze(self, path: Optional[Path] = None) -> str:
        """
        分析变更影响
        
        Args:
            path: 项目路径
        
        Returns:
            分析报告字符串
        """
        project_path = path or self.project_path
        
        # 获取变更文件
        changed_files = self._get_changed_files()
        
        # 分析影响
        impact = self._calculate_impact(changed_files)
        
        # 生成报告
        return self._generate_report(impact, changed_files)
    
    def _get_changed_files(self) -> List[str]:
        """获取变更的文件"""
        try:
            import subprocess
            
            result = subprocess.run(
                ["git", "diff", "--name-only", "HEAD"],
                capture_output=True,
                text=True,
                cwd=self.project_path
            )
            
            return [f for f in result.stdout.strip().split("\n") if f]
            
        except Exception:
            return []
    
    def _calculate_impact(self, changed_files: List[str]) -> ChangeImpact:
        """计算变更影响"""
        impact = ChangeImpact(
            level=ImpactLevel.LOW,
            affected_components=[],
            affected_endpoints=[],
            affected_models=[],
            recommendations=[],
            breaking_changes=[]
        )
        
        # 分析每个变更文件
        for file in changed_files:
            file_impact = self._analyze_file_impact(file)
            
            if file_impact:
                impact.affected_components.append(file)
                
                if file_impact.get("type") == "endpoint":
                    impact.affected_endpoints.extend(file_impact.get("items", []))
                elif file_impact.get("type") == "model":
                    impact.affected_models.extend(file_impact.get("items", []))
                
                # 检查破坏性变更
                if file_impact.get("breaking"):
                    impact.breaking_changes.append(file)
        
        # 计算影响等级
        impact.level = self._calculate_level(impact)
        
        # 生成建议
        impact.recommendations = self._generate_recommendations(impact)
        
        return impact
    
    def _analyze_file_impact(self, file: str) -> Optional[Dict]:
        """分析单个文件的变更影响"""
        impact_type = None
        items = []
        breaking = False
        
        # 根据文件名判断影响类型
        if any(kw in file.lower() for kw in ["route", "endpoint", "view", "handler"]):
            impact_type = "endpoint"
        elif any(kw in file.lower() for kw in ["model", "schema", "serializer", "entity"]):
            impact_type = "model"
        elif any(kw in file.lower() for kw in ["middleware", "auth", "permission"]):
            impact_type = "middleware"
            breaking = True  # 中间件变更通常是破坏性的
        
        # 尝试读取文件获取更多信息
        file_path = self.project_path / file
        if file_path.exists():
            try:
                content = file_path.read_text(encoding="utf-8")
                
                # 检测破坏性变更
                if any(kw in content for kw in ["BREAKING", "removed", "deleted", "deprecated"]):
                    breaking = True
                
            except Exception:
                pass
        
        if impact_type:
            return {
                "type": impact_type,
                "items": items,
                "breaking": breaking,
                "file": file
            }
        
        return None
    
    def _calculate_level(self, impact: ChangeImpact) -> ImpactLevel:
        """计算影响等级"""
        # 基础分数
        score = 0
        
        # 文件数量
        if len(impact.affected_components) > 10:
            score += 3
        elif len(impact.affected_components) > 5:
            score += 2
        else:
            score += 1
        
        # 端点数量
        if len(impact.affected_endpoints) > 5:
            score += 3
        elif len(impact.affected_endpoints) > 2:
            score += 2
        
        # 模型数量
        if len(impact.affected_models) > 3:
            score += 2
        
        # 破坏性变更
        if len(impact.breaking_changes) > 0:
            score += 3
        
        # 根据分数确定等级
        if score >= 8:
            return ImpactLevel.CRITICAL
        elif score >= 5:
            return ImpactLevel.HIGH
        elif score >= 3:
            return ImpactLevel.MEDIUM
        else:
            return ImpactLevel.LOW
    
    def _generate_recommendations(self, impact: ChangeImpact) -> List[str]:
        """生成建议"""
        recommendations = []
        
        # 根据影响等级生成建议
        if impact.level == ImpactLevel.CRITICAL:
            recommendations.append("🚨 建议发布主版本 (major) 更新")
            recommendations.append("⚠️ 进行全面的回归测试")
            recommendations.append("📢 提前通知用户可能的破坏性变更")
        
        elif impact.level == ImpactLevel.HIGH:
            recommendations.append("🎯 建议发布次版本 (minor) 更新")
            recommendations.append("🔍 重点测试受影响的组件")
            recommendations.append("📝 详细记录变更内容")
        
        elif impact.level == ImpactLevel.MEDIUM:
            recommendations.append("🔧 建议发布补丁版本 (patch)")
            recommendations.append("✅ 进行基本的功能测试")
        
        else:
            recommendations.append("✅ 变更影响较小")
            recommendations.append("📝 更新变更日志即可")
        
        # 特定建议
        if impact.affected_endpoints:
            recommendations.append("🔌 测试受影响的API端点")
        
        if impact.affected_models:
            recommendations.append("💾 验证数据模型兼容性")
        
        if impact.breaking_changes:
            recommendations.append("💥 检查破坏性变更的迁移指南")
        
        return recommendations
    
    def _generate_report(self, impact: ChangeImpact, changed_files: List[str]) -> str:
        """生成分析报告"""
        lines = []
        
        lines.append("=" * 60)
        lines.append("📊 API变更影响分析报告")
        lines.append("=" * 60)
        lines.append("")
        
        # 影响等级
        level_colors = {
            ImpactLevel.LOW: "🟢 低",
            ImpactLevel.MEDIUM: "🟡 中",
            ImpactLevel.HIGH: "🟠 高",
            ImpactLevel.CRITICAL: "🔴 严重"
        }
        
        lines.append(f"影响等级: {level_colors.get(impact.level, '未知')}")
        lines.append("")
        
        # 变更统计
        lines.append("📈 变更统计")
        lines.append("-" * 40)
        lines.append(f"变更文件数: {len(changed_files)}")
        lines.append(f"受影响端点数: {len(impact.affected_endpoints)}")
        lines.append(f"受影响模型数: {len(impact.affected_models)}")
        lines.append(f"破坏性变更: {len(impact.breaking_changes)}")
        lines.append("")
        
        # 受影响的组件
        if impact.affected_components:
            lines.append("📦 受影响的组件")
            lines.append("-" * 40)
            for component in impact.affected_components[:10]:
                lines.append(f"  - {component}")
            if len(impact.affected_components) > 10:
                lines.append(f"  ... 还有 {len(impact.affected_components) - 10} 个")
            lines.append("")
        
        # 受影响的端点
        if impact.affected_endpoints:
            lines.append("🔌 受影响的API端点")
            lines.append("-" * 40)
            for endpoint in impact.affected_endpoints[:5]:
                lines.append(f"  - {endpoint}")
            if len(impact.affected_endpoints) > 5:
                lines.append(f"  ... 还有 {len(impact.affected_endpoints) - 5} 个")
            lines.append("")
        
        # 破坏性变更
        if impact.breaking_changes:
            lines.append("💥 破坏性变更")
            lines.append("-" * 40)
            for change in impact.breaking_changes:
                lines.append(f"  - {change}")
            lines.append("")
        
        # 建议
        if impact.recommendations:
            lines.append("💡 建议")
            lines.append("-" * 40)
            for rec in impact.recommendations:
                lines.append(f"  {rec}")
            lines.append("")
        
        lines.append("=" * 60)
        
        return "\n".join(lines)
