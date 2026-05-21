#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APIChangelog-Pilot - 智能API变更日志生成与版本追踪引擎
零依赖、轻量级、自动化的API变更管理解决方案
"""

import argparse
import sys
import os
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from changelog_pilot.changelog import ChangelogGenerator
from changelog_pilot.version_tracker import VersionTracker
from changelog_pilot.tui import ChangelogTUI
from changelog_pilot.config import Config
from changelog_pilot.formats import FormatManager


def setup_argparse() -> argparse.ArgumentParser:
    """配置命令行参数解析器"""
    parser = argparse.ArgumentParser(
        prog="api-changelog-pilot",
        description="🛫 APIChangelog-Pilot - 智能API变更日志生成与版本追踪引擎",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
使用示例:
  %(prog)s init                    # 初始化项目配置
  %(prog)s generate                 # 分析变更并生成日志
  %(prog)s diff --from v1.0 --to v2.0  # 比较两个版本
  %(prog)s release --bump major     # 发布新版本
  %(prog)s report --format markdown # 生成变更报告

更多信息请访问: https://github.com/gitstq/api-changelog-pilot
        """
    )
    
    parser.add_argument(
        "--version", "-v",
        action="version",
        version="%(prog)s 1.0.0"
    )
    
    parser.add_argument(
        "--config", "-c",
        type=str,
        default=".changelogpilot.json",
        help="配置文件路径 (默认: .changelogpilot.json)"
    )
    
    parser.add_argument(
        "--verbose", "-V",
        action="store_true",
        help="显示详细输出"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="可用命令")
    
    # init 命令
    init_parser = subparsers.add_parser(
        "init",
        help="初始化APIChangelog-Pilot项目配置"
    )
    init_parser.add_argument(
        "--force", "-f",
        action="store_true",
        help="强制覆盖已存在的配置文件"
    )
    
    # generate 命令
    gen_parser = subparsers.add_parser(
        "generate",
        help="分析代码变更并生成变更日志"
    )
    gen_parser.add_argument(
        "--since", "-s",
        type=str,
        help="分析的起始版本/标签 (例如: v1.0.0)"
    )
    gen_parser.add_argument(
        "--until", "-u",
        type=str,
        default="HEAD",
        help="分析的结束版本/标签 (默认: HEAD)"
    )
    gen_parser.add_argument(
        "--output", "-o",
        type=str,
        help="输出文件路径"
    )
    gen_parser.add_argument(
       ("--format", "-f"),
        type=str,
        choices=["markdown", "json", "yaml", "keepachangelog"],
        default="markdown",
        help="输出格式 (默认: markdown)"
    )
    gen_parser.add_argument(
        "--ai", "-a",
        action="store_true",
        help="启用AI智能分析 (需要配置API密钥)"
    )
    
    # diff 命令
    diff_parser = subparsers.add_parser(
        "diff",
        help="比较两个版本/标签之间的差异"
    )
    diff_parser.add_argument(
        "--from", "-f",
        dest="from_ref",
        type=str,
        required=True,
        help="起始版本/标签"
    )
    diff_parser.add_argument(
        "--to", "-t",
        type=str,
        default="HEAD",
        help="结束版本/标签 (默认: HEAD)"
    )
    diff_parser.add_argument(
        "--type", "-T",
        choices=["api", "breaking", "feature", "fix", "all"],
        default="all",
        help="变更类型过滤 (默认: all)"
    )
    
    # release 命令
    release_parser = subparsers.add_parser(
        "release",
        help="发布新版本"
    )
    release_parser.add_argument(
        "--bump", "-b",
        choices=["major", "minor", "patch"],
        required=True,
        help="版本号增量类型"
    )
    release_parser.add_argument(
        "--message", "-m",
        type=str,
        help="版本发布消息"
    )
    release_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="模拟运行，不实际创建文件"
    )
    
    # report 命令
    report_parser = subparsers.add_parser(
        "report",
        help="生成变更报告"
    )
    report_parser.add_argument(
        "--format", "-f",
        type=str,
        choices=["markdown", "html", "json", "pdf"],
        default="markdown",
        help="报告格式 (默认: markdown)"
    )
    report_parser.add_argument(
        "--output", "-o",
        type=str,
        help="输出文件路径"
    )
    report_parser.add_argument(
        "--template", "-t",
        type=str,
        help="自定义模板文件路径"
    )
    
    # analyze 命令
    analyze_parser = subparsers.add_parser(
        "analyze",
        help="深度分析API变更影响"
    )
    analyze_parser.add_argument(
        "--path", "-p",
        type=str,
        help="API代码路径 (默认: 当前目录)"
    )
    analyze_parser.add_argument(
        "--output", "-o",
        type=str,
        help="分析结果输出路径"
    )
    
    # tui 命令
    subparsers.add_parser(
        "tui",
        help="启动交互式TUI界面"
    )
    
    # config 命令
    config_parser = subparsers.add_parser(
        "config",
        help="配置管理"
    )
    config_parser.add_argument(
        "--set", "-s",
        nargs=2,
        metavar=("KEY", "VALUE"),
        help="设置配置项"
    )
    config_parser.add_argument(
        "--get", "-g",
        metavar="KEY",
        help="获取配置项值"
    )
    config_parser.add_argument(
        "--list", "-l",
        action="store_true",
        help="列出所有配置项"
    )
    
    return parser


def cmd_init(args: argparse.Namespace, config: Config) -> int:
    """初始化命令"""
    config_path = Path(args.config)
    
    if config_path.exists() and not args.force:
        print(f"⚠️  配置文件已存在: {config_path}")
        print("   使用 --force 强制覆盖")
        return 1
    
    config.init_default()
    config.save(config_path)
    print(f"✅ 已创建配置文件: {config_path}")
    print("\n📝 请根据项目需求编辑配置文件")
    return 0


def cmd_generate(args: argparse.Namespace, config: Config) -> int:
    """生成命令"""
    generator = ChangelogGenerator(config)
    
    try:
        changelog = generator.generate(
            since=args.since,
            until=args.until,
            use_ai=args.ai
        )
        
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(changelog, encoding="utf-8")
            print(f"✅ 变更日志已保存到: {output_path}")
        else:
            print(changelog)
        
        return 0
    except Exception as e:
        print(f"❌ 生成变更日志失败: {e}")
        return 1


def cmd_diff(args: argparse.Namespace, config: Config) -> int:
    """比较命令"""
    tracker = VersionTracker(config)
    
    try:
        diff_result = tracker.compare(
            from_ref=args.from_ref,
            to_ref=args.to_ref,
            filter_type=args.type
        )
        
        print(diff_result)
        return 0
    except Exception as e:
        print(f"❌ 版本比较失败: {e}")
        return 1


def cmd_release(args: argparse.Namespace, config: Config) -> int:
    """发布命令"""
    tracker = VersionTracker(config)
    
    try:
        new_version = tracker.bump_version(
            bump_type=args.bump,
            message=args.message,
            dry_run=args.dry_run
        )
        
        if args.dry_run:
            print(f"🔍 模拟运行: 将创建版本 {new_version}")
        else:
            print(f"🎉 成功发布新版本: {new_version}")
        
        return 0
    except Exception as e:
        print(f"❌ 发布失败: {e}")
        return 1


def cmd_report(args: argparse.Namespace, config: Config) -> int:
    """报告命令"""
    generator = ChangelogGenerator(config)
    formatter = FormatManager(config)
    
    try:
        report = generator.generate_report(
            format_type=args.format,
            template_path=args.template
        )
        
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(report, encoding="utf-8")
            print(f"✅ 报告已保存到: {output_path}")
        else:
            print(report)
        
        return 0
    except Exception as e:
        print(f"❌ 生成报告失败: {e}")
        return 1


def cmd_analyze(args: argparse.Namespace, config: Config) -> int:
    """分析命令"""
    from changelog_pilot.impact_analyzer import ImpactAnalyzer
    
    analyzer = ImpactAnalyzer(config)
    
    try:
        path = Path(args.path) if args.path else Path.cwd()
        analysis = analyzer.analyze(path)
        
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(analysis, encoding="utf-8")
            print(f"✅ 分析结果已保存到: {output_path}")
        else:
            print(analysis)
        
        return 0
    except Exception as e:
        print(f"❌ 分析失败: {e}")
        return 1


def cmd_tui(args: argparse.Namespace, config: Config) -> int:
    """TUI命令"""
    try:
        tui = ChangelogTUI(config)
        tui.run()
        return 0
    except KeyboardInterrupt:
        print("\n👋 再见!")
        return 0
    except Exception as e:
        print(f"❌ TUI启动失败: {e}")
        return 1


def cmd_config(args: argparse.Namespace, config: Config) -> int:
    """配置命令"""
    if args.set:
        key, value = args.set
        config.set(key, value)
        config_path = Path(args.config)
        config.save(config_path)
        print(f"✅ 已设置 {key} = {value}")
        return 0
    
    if args.get:
        value = config.get(args.get)
        if value is not None:
            print(f"{args.get} = {value}")
        else:
            print(f"⚠️  配置项 {args.get} 不存在")
        return 0
    
    if args.list:
        for key, value in config.to_dict().items():
            print(f"{key} = {value}")
        return 0
    
    return 0


def main() -> int:
    """主入口函数"""
    parser = setup_argparse()
    args = parser.parse_args()
    
    # 如果没有命令，显示帮助
    if not args.command:
        parser.print_help()
        return 0
    
    # 加载配置
    config_path = Path(args.config)
    config = Config()
    
    if config_path.exists():
        config.load(config_path)
    
    # 设置日志级别
    if args.verbose:
        config.set("verbose", True)
    
    # 执行对应命令
    commands = {
        "init": cmd_init,
        "generate": cmd_generate,
        "diff": cmd_diff,
        "release": cmd_release,
        "report": cmd_report,
        "analyze": cmd_analyze,
        "tui": cmd_tui,
        "config": cmd_config,
    }
    
    command_func = commands.get(args.command)
    if command_func:
        return command_func(args, config)
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
