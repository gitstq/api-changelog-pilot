"""
APIChangelog-Pilot - 智能API变更日志生成与版本追踪引擎
轻量级零依赖命令行工具，自动分析API代码变更并生成规范的变更日志
"""

__version__ = "1.0.0"
__author__ = "gitstq"
__license__ = "MIT"

from .changelog import ChangelogGenerator
from .version_tracker import VersionTracker
from .diff_analyzer import DiffAnalyzer
from .semantic_parser import SemanticParser

__all__ = [
    "ChangelogGenerator",
    "VersionTracker", 
    "DiffAnalyzer",
    "SemanticParser",
]
