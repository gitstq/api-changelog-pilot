#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例Flask API项目 - 演示APIChangelog-Pilot的使用
"""

from flask import Flask, jsonify, request
from functools import wraps

app = Flask(__name__)

# 模拟数据
users = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
]

products = [
    {"id": 1, "name": "Widget", "price": 9.99},
    {"id": 2, "name": "Gadget", "price": 19.99},
]


def require_auth(f):
    """认证装饰器"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    return decorated


# === 用户端点 ===

@app.route("/api/v1/users", methods=["GET"])
def get_users():
    """获取用户列表"""
    return jsonify({"users": users})


@app.route("/api/v1/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    """获取单个用户"""
    user = next((u for u in users if u["id"] == user_id), None)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404


@app.route("/api/v1/users", methods=["POST"])
def create_user():
    """创建用户"""
    data = request.json
    new_user = {
        "id": len(users) + 1,
        "name": data.get("name"),
        "email": data.get("email"),
    }
    users.append(new_user)
    return jsonify(new_user), 201


@app.route("/api/v1/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    """更新用户"""
    user = next((u for u in users if u["id"] == user_id), None)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    data = request.json
    user["name"] = data.get("name", user["name"])
    user["email"] = data.get("email", user["email"])
    
    return jsonify(user)


@app.route("/api/v1/users/<int:user_id>", methods=["DELETE"])
@require_auth
def delete_user(user_id):
    """删除用户"""
    global users
    users = [u for u in users if u["id"] != user_id]
    return jsonify({"message": "User deleted"})


# === 产品端点 ===

@app.route("/api/v1/products", methods=["GET"])
def get_products():
    """获取产品列表"""
    return jsonify({"products": products})


@app.route("/api/v1/products/<int:product_id>", methods=["GET"])
def get_product(product_id):
    """获取单个产品"""
    product = next((p for p in products if p["id"] == product_id), None)
    if product:
        return jsonify(product)
    return jsonify({"error": "Product not found"}), 404


# === 健康检查 ===

@app.route("/health", methods=["GET"])
def health():
    """健康检查"""
    return jsonify({"status": "healthy"})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
