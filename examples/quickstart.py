#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APIChangelog-Pilot 快速启动脚本
自动演示工具的各项功能
"""

import subprocess
import sys
from pathlib import Path


def run_command(cmd, description):
    """运行命令并显示结果"""
    print(f"\n{'=' * 60}")
    print(f"📌 {description}")
    print(f"{'=' * 60}")
    print(f"命令: {' '.join(cmd)}")
    print()
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            cwd=Path(__file__).parent.parent
        )
        
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"⚠️  stderr: {result.stderr}")
        
        return result.returncode == 0
    except Exception as e:
        print(f"❌ 执行失败: {e}")
        return False


def main():
    """主函数"""
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   🛫 APIChangelog-Pilot 快速启动                          ║
    ║                                                           ║
    ║   正在演示工具的各项功能...                                ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)
    
    # 1. 显示帮助
    run_command(
        [sys.executable, "-m", "changelog_pilot", "--help"],
        "显示帮助信息"
    )
    
    # 2. 显示版本
    run_command(
        [sys.executable, "-m", "changelog_pilot", "--version"],
        "显示版本信息"
    )
    
    # 3. 初始化配置
    run_command(
        [sys.executable, "-m", "changelog_pilot", "init"],
        "初始化配置文件"
    )
    
    # 4. 显示配置
    run_command(
        [sys.executable, "-m", "changelog_pilot", "config", "--list"],
        "显示当前配置"
    )
    
    # 5. 生成变更日志（如果有git历史）
    run_command(
        [sys.executable, "-m", "changelog_pilot", "generate", "--format", "markdown"],
        "生成变更日志"
    )
    
    # 6. 版本列表
    run_command(
        [sys.executable, "-m", "changelog_pilot", "diff", "--from", "v0.0.0", "--to", "HEAD"],
        "比较版本差异"
    )
    
    print("""
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║   ✅ 快速启动演示完成!                                     ║
    ║                                                           ║
    ║   接下来你可以:                                            ║
    ║   1. 查看生成的 CHANGELOG.md 文件                         ║
    ║   2. 运行 python examples/basic_usage.py 查看更多示例     ║
    ║   3. 使用 api-changelog-pilot tui 启动交互式界面          ║
    ║   4. 阅读 README.md 了解完整文档                          ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    main()
