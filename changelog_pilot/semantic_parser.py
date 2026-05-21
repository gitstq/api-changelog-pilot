#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
语义解析器 - 解析和理解API语义信息
"""

import re
import ast
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from dataclasses import dataclass, field


@dataclass
class APIEndpoint:
    """API端点"""
    path: str
    method: str
    name: str = ""
    description: str = ""
    parameters: List[Dict] = field(default_factory=list)
    request_body: Optional[Dict] = None
    responses: Dict = field(default_factory=dict)
    decorators: List[str] = field(default_factory=list)
    source_file: str = ""


@dataclass
class APIModel:
    """API数据模型"""
    name: str
    type: str  # class, enum, union
    fields: List[Dict] = field(default_factory=list)
    description: str = ""
    source_file: str = ""


@dataclass
class ParsedAPI:
    """解析的API"""
    endpoints: List[APIEndpoint] = field(default_factory=list)
    models: List[APIModel] = field(default_factory=list)
    tags: Set[str] = field(default_factory=set)


class SemanticParser:
    """语义解析器"""
    
    # 常见的Web框架路由装饰器
    ROUTE_DECORATORS = {
        "flask": ["app.route", "route"],
        "fastapi": ["app.get", "app.post", "app.put", "app.patch", "app.delete",
                   "get", "post", "put", "patch", "delete"],
        "django": ["path", "re_path", "route"],
        "bottle": ["route"],
        "tornado": ["tornado.web"],
    }
    
    # HTTP方法关键词
    HTTP_METHODS = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS", "HEAD"]
    
    def __init__(self, config: Optional[Dict] = None):
        """初始化解析器"""
        self.config = config or {}
        self.framework = self.config.get("framework", "auto")
        self.project_path = Path(self.config.get("project_path", "."))
    
    def parse(self, path: Optional[Path] = None) -> ParsedAPI:
        """
        解析API代码
        
        Args:
            path: 项目路径
        
        Returns:
            解析的API对象
        """
        project_path = path or self.project_path
        
        if not project_path.exists():
            return ParsedAPI()
        
        # 自动检测框架
        if self.framework == "auto":
            self.framework = self._detect_framework(project_path)
        
        # 收集Python文件
        py_files = list(project_path.rglob("*.py"))
        
        # 解析每个文件
        parsed = ParsedAPI()
        
        for py_file in py_files:
            try:
                result = self._parse_file(py_file)
                if result:
                    parsed.endpoints.extend(result.get("endpoints", []))
                    parsed.models.extend(result.get("models", []))
                    parsed.tags.update(result.get("tags", set()))
            except Exception:
                # 忽略解析错误
                pass
        
        return parsed
    
    def _detect_framework(self, path: Path) -> str:
        """自动检测Web框架"""
        py_files = list(path.rglob("*.py"))
        
        imports = set()
        for py_file in py_files:
            try:
                content = py_file.read_text(encoding="utf-8")
                import_lines = re.findall(r'^(?:from|import)\s+(\w+)', content, re.MULTILINE)
                imports.update(import_lines)
            except Exception:
                pass
        
        # 检测框架
        if "fastapi" in imports:
            return "fastapi"
        elif "flask" in imports:
            return "flask"
        elif "django" in imports:
            return "django"
        elif "bottle" in imports:
            return "bottle"
        elif "tornado" in imports:
            return "tornado"
        
        return "unknown"
    
    def _parse_file(self, py_file: Path) -> Optional[Dict]:
        """解析单个Python文件"""
        try:
            content = py_file.read_text(encoding="utf-8")
            tree = ast.parse(content)
            
            endpoints = []
            models = []
            tags = set()
            
            for node in ast.walk(tree):
                # 解析装饰器
                if isinstance(node, ast.FunctionDef):
                    endpoint = self._parse_function(node, content, py_file)
                    if endpoint:
                        endpoints.append(endpoint)
                
                # 解析类定义
                if isinstance(node, ast.ClassDef):
                    model = self._parse_class(node, content, py_file)
                    if model:
                        models.append(model)
                    
                    # 提取tags
                    for base in node.bases:
                        if isinstance(base, ast.Name):
                            tags.add(base.id)
            
            return {
                "endpoints": endpoints,
                "models": models,
                "tags": tags
            }
            
        except Exception:
            return None
    
    def _parse_function(
        self,
        node: ast.FunctionDef,
        content: str,
        py_file: Path
    ) -> Optional[APIEndpoint]:
        """解析函数为API端点"""
        decorators = []
        route_path = ""
        method = "GET"
        
        # 解析装饰器
        for decorator in node.decorator_list:
            decorator_str = ast.unparse(decorator) if hasattr(ast, 'unparse') else ""
            decorators.append(decorator_str)
            
            # 检测FastAPI装饰器
            for http_method in self.HTTP_METHODS:
                if http_method.lower() in decorator_str.lower():
                    method = http_method
                    
                    # 提取路由路径
                    if hasattr(decorator, 'args') and decorator.args:
                        for arg in decorator.args:
                            if isinstance(arg, ast.Constant):
                                route_path = arg.value
                    elif hasattr(decorator, 'func'):
                        # 处理 app.get("/path") 格式
                        if hasattr(decorator.func, 'attr'):
                            pass  # 已经有method了
        
        # 只处理有路由装饰器的函数
        has_route = any("route" in d.lower() or any(m.lower() in d.lower() 
                                                       for m in self.HTTP_METHODS) 
                        for d in decorators)
        
        if not has_route:
            return None
        
        # 提取docstring作为描述
        description = ast.get_docstring(node) or ""
        
        # 解析参数
        parameters = []
        for arg in node.args.args:
            parameters.append({
                "name": arg.arg,
                "type": self._get_type_annotation(arg.annotation)
            })
        
        # 提取路由路径（从装饰器参数）
        for decorator in decorators:
            path_match = re.search(r'["\'](/[^"\']+)["\']', decorator)
            if path_match:
                route_path = path_match.group(1)
                break
        
        return APIEndpoint(
            path=route_path,
            method=method,
            name=node.name,
            description=description,
            parameters=parameters,
            decorators=decorators,
            source_file=str(py_file)
        )
    
    def _parse_class(
        self,
        node: ast.ClassDef,
        content: str,
        py_file: Path
    ) -> Optional[APIModel]:
        """解析类为数据模型"""
        # 检查是否是API相关类
        class_name = node.name.lower()
        is_model = any(kw in class_name for kw in ["model", "schema", "serializer", 
                                                      "request", "response", "dto"])
        
        if not is_model:
            return None
        
        description = ast.get_docstring(node) or ""
        
        # 解析字段
        fields = []
        for item in node.body:
            if isinstance(item, ast.AnnAssign) and isinstance(item.target, ast.Name):
                field_name = item.target.id
                field_type = self._get_type_annotation(item.annotation)
                fields.append({
                    "name": field_name,
                    "type": field_type
                })
        
        return APIModel(
            name=node.name,
            type="class",
            fields=fields,
            description=description,
            source_file=str(py_file)
        )
    
    def _get_type_annotation(self, annotation) -> str:
        """获取类型注解字符串"""
        if annotation is None:
            return "Any"
        
        if hasattr(ast, 'unparse'):
            try:
                return ast.unparse(annotation)
            except Exception:
                pass
        
        if isinstance(annotation, ast.Name):
            return annotation.id
        elif isinstance(annotation, ast.Constant):
            return str(annotation.value)
        
        return "Any"
    
    def generate_openapi(
        self,
        parsed: ParsedAPI,
        title: str = "API",
        version: str = "1.0.0"
    ) -> Dict:
        """生成OpenAPI规范"""
        openapi = {
            "openapi": "3.0.0",
            "info": {
                "title": title,
                "version": version,
                "description": "Generated by APIChangelog-Pilot"
            },
            "paths": {},
            "components": {
                "schemas": {}
            }
        }
        
        # 添加端点
        for endpoint in parsed.endpoints:
            path = endpoint.path or "/"
            method = endpoint.method.lower()
            
            if path not in openapi["paths"]:
                openapi["paths"][path] = {}
            
            openapi["paths"][path][method] = {
                "summary": endpoint.name,
                "description": endpoint.description,
                "parameters": endpoint.parameters,
                "responses": {
                    "200": {
                        "description": "Successful response"
                    }
                }
            }
        
        # 添加模型
        for model in parsed.models:
            openapi["components"]["schemas"][model.name] = {
                "type": "object",
                "properties": {
                    field["name"]: {"type": field["type"]}
                    for field in model.fields
                }
            }
        
        return openapi
    
    def compare_apis(
        self,
        old_api: ParsedAPI,
        new_api: ParsedAPI
    ) -> Dict:
        """比较两个API版本的差异"""
        changes = {
            "endpoints": {
                "added": [],
                "removed": [],
                "modified": []
            },
            "models": {
                "added": [],
                "removed": [],
                "modified": []
            }
        }
        
        # 比较端点
        old_endpoints = {(e.path, e.method): e for e in old_api.endpoints}
        new_endpoints = {(e.path, e.method): e for e in new_api.endpoints}
        
        for key, endpoint in new_endpoints.items():
            if key not in old_endpoints:
                changes["endpoints"]["added"].append(endpoint)
            else:
                # 检查是否修改
                old = old_endpoints[key]
                if endpoint.description != old.description:
                    changes["endpoints"]["modified"].append({
                        "before": old,
                        "after": endpoint
                    })
        
        for key in old_endpoints:
            if key not in new_endpoints:
                changes["endpoints"]["removed"].append(old_endpoints[key])
        
        # 比较模型
        old_models = {m.name: m for m in old_api.models}
        new_models = {m.name: m for m in new_api.models}
        
        for name, model in new_models.items():
            if name not in old_models:
                changes["models"]["added"].append(model)
            else:
                old = old_models[name]
                if model.fields != old.fields:
                    changes["models"]["modified"].append({
                        "before": old,
                        "after": model
                    })
        
        for name in old_models:
            if name not in new_models:
                changes["models"]["removed"].append(old_models[name])
        
        return changes
