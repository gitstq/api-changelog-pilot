#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TUI界面 - 交互式终端用户界面
"""

import sys
from typing import Dict, List, Optional


class ChangelogTUI:
    """变更日志TUI界面"""
    
    # 颜色代码
    COLORS = {
        "reset": "\033[0m",
        "bold": "\033[1m",
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "bg_black": "\033[40m",
    }
    
    # 菜单选项
    MENU_OPTIONS = [
        ("📊", "查看变更统计", "stats"),
        ("📝", "生成变更日志", "generate"),
        ("🔍", "比较版本差异", "diff"),
        ("🎯", "分析变更影响", "analyze"),
        ("📦", "发布新版本", "release"),
        ("📄", "导出报告", "export"),
        ("⚙️", "配置设置", "config"),
        ("❌", "退出", "quit"),
    ]
    
    def __init__(self, config):
        """初始化TUI"""
        self.config = config
        self.running = True
    
    def run(self):
        """运行TUI"""
        self._clear_screen()
        
        while self.running:
            self._show_header()
            self._show_menu()
            
            choice = self._get_input("请选择操作")
            
            self._handle_choice(choice)
    
    def _clear_screen(self):
        """清屏"""
        print("\033[2J\033[H", end="")
    
    def _show_header(self):
        """显示标题"""
        print(self.COLORS["cyan"])
        print("╔═══════════════════════════════════════════════════════════╗")
        print("║                                                           ║")
        print("║   🛫 APIChangelog-Pilot - 智能API变更日志生成引擎          ║")
        print("║                                                           ║")
        print("║   轻量化 · 零依赖 · 自动化 · 智能化                        ║")
        print("║                                                           ║")
        print("╚═══════════════════════════════════════════════════════════╝")
        print(self.COLORS["reset"])
        print()
    
    def _show_menu(self):
        """显示菜单"""
        print(self.COLORS["bold"] + "📋 主菜单:" + self.COLORS["reset"])
        print()
        
        for i, (icon, text, _) in enumerate(self.MENU_OPTIONS, 1):
            print(f"  {self.COLORS['yellow']}{i}{self.COLORS['reset']}. {icon} {text}")
        
        print()
    
    def _get_input(self, prompt: str = "") -> str:
        """获取用户输入"""
        if prompt:
            print(prompt, end=": ")
        return input().strip()
    
    def _handle_choice(self, choice: str):
        """处理用户选择"""
        try:
            idx = int(choice) - 1
            if 0 <= idx < len(self.MENU_OPTIONS):
                _, _, action = self.MENU_OPTIONS[idx]
                
                if action == "quit":
                    self._quit()
                else:
                    self._execute_action(action)
            else:
                self._show_error("无效的选择")
        except ValueError:
            self._show_error("请输入数字")
    
    def _execute_action(self, action: str):
        """执行动作"""
        actions = {
            "stats": self._show_stats,
            "generate": self._generate_changelog,
            "diff": self._compare_versions,
            "analyze": self._analyze_impact,
            "release": self._release_version,
            "export": self._export_report,
            "config": self._show_config,
        }
        
        action_func = actions.get(action)
        if action_func:
            action_func()
        else:
            self._show_error(f"未知动作: {action}")
    
    def _show_stats(self):
        """显示统计信息"""
        print(self.COLORS["bold"] + "\n📊 变更统计\n" + self.COLORS["reset"])
        
        from changelog_pilot.changelog import ChangelogGenerator
        
        generator = ChangelogGenerator(self.config.to_dict())
        
        try:
            # 获取最近提交统计
            from pathlib import Path
            import subprocess
            
            result = subprocess.run(
                ["git", "log", "--oneline", "-20"],
                capture_output=True,
                text=True,
                cwd=Path(self.config.get("repo_path", "."))
            )
            
            commits = result.stdout.strip().split("\n") if result.stdout else []
            
            print(f"  最近提交数量: {len(commits)}")
            print()
            
            # 按类型统计
            type_counts = {}
            for commit in commits:
                if "feat" in commit.lower():
                    type_counts["✨ 新功能"] = type_counts.get("✨ 新功能", 0) + 1
                elif "fix" in commit.lower():
                    type_counts["🐛 修复"] = type_counts.get("🐛 修复", 0) + 1
                elif "doc" in commit.lower():
                    type_counts["📝 文档"] = type_counts.get("📝 文档", 0) + 1
            
            for change_type, count in type_counts.items():
                print(f"  {change_type}: {count}")
            
            print()
            self._wait_continue()
            
        except Exception as e:
            self._show_error(f"获取统计失败: {e}")
    
    def _generate_changelog(self):
        """生成变更日志"""
        print(self.COLORS["bold"] + "\n📝 生成变更日志\n" + self.COLORS["reset"])
        
        from changelog_pilot.changelog import ChangelogGenerator
        
        generator = ChangelogGenerator(self.config.to_dict())
        
        try:
            changelog = generator.generate(use_ai=False)
            print(changelog)
            print()
            
            # 询问是否保存
            save = self._get_input("是否保存到文件? (y/n)")
            if save.lower() == "y":
                filename = self._get_input("请输入文件名 (默认: CHANGELOG.md)")
                filename = filename or "CHANGELOG.md"
                
                from pathlib import Path
                Path(filename).write_text(changelog, encoding="utf-8")
                print(f"✅ 已保存到: {filename}")
            
            self._wait_continue()
            
        except Exception as e:
            self._show_error(f"生成失败: {e}")
    
    def _compare_versions(self):
        """比较版本"""
        print(self.COLORS["bold"] + "\n🔍 比较版本差异\n" + self.COLORS["reset"])
        
        from_version = self._get_input("起始版本 (例如: v1.0.0)")
        to_version = self._get_input("结束版本 (例如: HEAD)")
        to_version = to_version or "HEAD"
        
        from changelog_pilot.version_tracker import VersionTracker
        
        tracker = VersionTracker(self.config.to_dict())
        
        try:
            result = tracker.compare(from_version, to_version)
            print(result)
            self._wait_continue()
            
        except Exception as e:
            self._show_error(f"比较失败: {e}")
    
    def _analyze_impact(self):
        """分析影响"""
        print(self.COLORS["bold"] + "\n🎯 变更影响分析\n" + self.COLORS["reset"])
        
        from changelog_pilot.diff_analyzer import DiffAnalyzer
        
        analyzer = DiffAnalyzer(self.config.to_dict())
        
        try:
            analysis = analyzer.analyze_impact()
            
            print(f"分析结果:")
            print(f"  总文件数: {analysis.get('total_files', 0)}")
            print()
            
            impact = analysis.get("impact", {})
            print(f"影响等级: {self.COLORS['yellow']}{impact.get('severity', 'unknown').upper()}{self.COLORS['reset']}")
            
            if impact.get("affected_endpoints"):
                print(f"\n受影响的端点:")
                for endpoint in impact["affected_endpoints"][:5]:
                    print(f"  - {endpoint}")
            
            if impact.get("recommendations"):
                print(f"\n建议:")
                for rec in impact["recommendations"]:
                    print(f"  💡 {rec}")
            
            self._wait_continue()
            
        except Exception as e:
            self._show_error(f"分析失败: {e}")
    
    def _release_version(self):
        """发布版本"""
        print(self.COLORS["bold"] + "\n🎉 发布新版本\n" + self.COLORS["reset"])
        
        print("版本类型:")
        print("  1. major - 破坏性变更")
        print("  2. minor - 新功能")
        print("  3. patch - 修复补丁")
        
        bump_type = self._get_input("请选择版本类型 (1/2/3)")
        
        type_map = {"1": "major", "2": "minor", "3": "patch"}
        bump = type_map.get(bump_type, "patch")
        
        dry_run = self._get_input("模拟运行? (y/n)").lower() == "y"
        
        from changelog_pilot.version_tracker import VersionTracker
        
        tracker = VersionTracker(self.config.to_dict())
        
        try:
            new_version = tracker.bump_version(bump, dry_run=dry_run)
            
            if dry_run:
                print(f"🔍 模拟: 将发布版本 {new_version}")
            else:
                print(f"🎉 成功发布版本 {new_version}")
            
            self._wait_continue()
            
        except Exception as e:
            self._show_error(f"发布失败: {e}")
    
    def _export_report(self):
        """导出报告"""
        print(self.COLORS["bold"] + "\n📄 导出报告\n" + self.COLORS["reset"])
        
        print("导出格式:")
        print("  1. markdown")
        print("  2. html")
        print("  3. json")
        
        format_choice = self._get_input("请选择格式 (1/2/3)")
        
        format_map = {"1": "markdown", "2": "html", "3": "json"}
        export_format = format_map.get(format_choice, "markdown")
        
        filename = self._get_input("请输入文件名")
        
        from changelog_pilot.changelog import ChangelogGenerator
        
        generator = ChangelogGenerator(self.config.to_dict())
        
        try:
            report = generator.generate_report(format_type=export_format)
            
            if filename:
                from pathlib import Path
                Path(filename).write_text(report, encoding="utf-8")
                print(f"✅ 报告已保存到: {filename}")
            else:
                print(report)
            
            self._wait_continue()
            
        except Exception as e:
            self._show_error(f"导出失败: {e}")
    
    def _show_config(self):
        """显示配置"""
        print(self.COLORS["bold"] + "\n⚙️ 配置设置\n" + self.COLORS["reset"])
        
        config = self.config.to_dict()
        
        print("当前配置:")
        print(f"  仓库路径: {config.get('repo_path', '.')}")
        print(f"  输出格式: {config.get('output_format', 'markdown')}")
        print(f"  标签前缀: {config.get('tag_prefix', 'v')}")
        print(f"  AI启用: {config.get('ai_enabled', False)}")
        print()
        
        edit = self._get_input("是否编辑配置? (y/n)")
        if edit.lower() == "y":
            key = self._get_input("配置项名称")
            value = self._get_input("配置值")
            
            if key and value:
                self.config.set(key, value)
                print(f"✅ 已设置 {key} = {value}")
        
        self._wait_continue()
    
    def _show_error(self, message: str):
        """显示错误"""
        print(f"\n{self.COLORS['red']}❌ 错误: {message}{self.COLORS['reset']}")
        self._wait_continue()
    
    def _wait_continue(self):
        """等待用户继续"""
        self._get_input("\n按 Enter 继续...")
    
    def _quit(self):
        """退出"""
        print(f"\n{self.COLORS['cyan']}👋 再见!{self.COLORS['reset']}\n")
        self.running = False
