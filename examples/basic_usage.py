#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APIChangelog-Pilot 使用示例
"""

from changelog_pilot.changelog import ChangelogGenerator
from changelog_pilot.version_tracker import VersionTracker
from changelog_pilot.diff_analyzer import DiffAnalyzer
from changelog_pilot.config import Config


def example_basic_usage():
    """基本使用示例"""
    print("=" * 60)
    print("示例1: 基本使用")
    print("=" * 60)
    
    # 创建配置
    config = Config()
    config.set("repo_path", ".")
    config.set("output_format", "markdown")
    
    # 创建生成器
    generator = ChangelogGenerator(config.to_dict())
    
    # 生成变更日志
    changelog = generator.generate(since="v1.0.0", until="HEAD")
    
    print(changelog)
    print()


def example_version_bump():
    """版本递增示例"""
    print("=" * 60)
    print("示例2: 版本递增")
    print("=" * 60)
    
    config = Config()
    tracker = VersionTracker(config.to_dict())
    
    # 获取最新版本
    latest = tracker.get_latest_version()
    print(f"当前版本: {latest}")
    
    # 递增版本
    new_version = tracker.bump_version("minor", dry_run=True)
    print(f"新版本 (模拟): {new_version}")
    print()


def example_diff_analysis():
    """差异分析示例"""
    print("=" * 60)
    print("示例3: 差异分析")
    print("=" * 60)
    
    config = Config()
    analyzer = DiffAnalyzer(config.to_dict())
    
    # 分析变更影响
    impact = analyzer.analyze_impact(since="v1.0.0")
    
    print(f"总文件数: {impact.get('total_files', 0)}")
    print(f"影响等级: {impact.get('impact', {}).get('severity', 'unknown')}")
    print()


def example_custom_format():
    """自定义格式示例"""
    print("=" * 60)
    print("示例4: 自定义格式")
    print("=" * 60)
    
    config = Config()
    generator = ChangelogGenerator(config.to_dict())
    
    # 生成不同格式的报告
    changelog_md = generator.generate_report(format_type="markdown")
    changelog_json = generator.generate_report(format_type="json")
    changelog_html = generator.generate_report(format_type="html")
    
    print("Markdown格式:")
    print(changelog_md[:500])
    print("...")
    print()


def example_tui_mode():
    """TUI模式示例"""
    print("=" * 60)
    print("示例5: TUI交互模式")
    print("=" * 60)
    
    print("运行以下命令启动TUI模式:")
    print("  python -m changelog_pilot tui")
    print()
    
    print("或者使用命令行工具:")
    print("  api-changelog-pilot tui")
    print()


if __name__ == "__main__":
    # 运行所有示例
    try:
        example_basic_usage()
    except Exception as e:
        print(f"示例1跳过: {e}")
    
    try:
        example_version_bump()
    except Exception as e:
        print(f"示例2跳过: {e}")
    
    try:
        example_diff_analysis()
    except Exception as e:
        print(f"示例3跳过: {e}")
    
    example_custom_format()
    example_tui_mode()
    
    print("=" * 60)
    print("所有示例完成!")
    print("=" * 60)
