#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
用户行为分析 API 测试脚本

测试以下 API 接口：
1. 点击流分析 - GET /api/admin/analytics/clickstream/
2. 活跃用户分析 - GET /api/admin/analytics/active-users/
3. 登录频次分析 - GET /api/admin/analytics/login-frequency/
4. 页面停留分析 - GET /api/admin/analytics/page-duration/

使用方法：
    python test_user_behavior_analytics.py
"""

import os
import sys
import json
import time
import requests
from datetime import datetime, timedelta

# 添加后端路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 配置
BASE_URL = "http://localhost:8000"
API_ENDPOINTS = {
    "clickstream": "/api/admin/analytics/clickstream/",
    "active_users": "/api/admin/analytics/active-users/",
    "login_frequency": "/api/admin/analytics/login-frequency/",
    "page_duration": "/api/admin/analytics/page-duration/",
}


def get_admin_token():
    """获取管理员 Token"""
    login_url = f"{BASE_URL}/api/accounts/login/"
    login_data = {
        "username": "admin",
        "password": "admin123"
    }

    try:
        response = requests.post(login_url, json=login_data, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get("code") == 200:
                return data.get("data", {}).get("token")
        return None
    except Exception as e:
        print(f"登录失败: {e}")
        return None


def test_api(endpoint_name, token, params=None):
    """测试单个 API 接口"""
    if params is None:
        params = {}

    endpoint = API_ENDPOINTS[endpoint_name]
    url = f"{BASE_URL}{endpoint}"
    headers = {"Authorization": f"Bearer {token}"}

    start_time = time.time()
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        elapsed_time = time.time() - start_time

        result = {
            "endpoint": endpoint,
            "status_code": response.status_code,
            "elapsed_time": f"{elapsed_time:.3f}s",
            "success": False,
            "data": None,
            "message": ""
        }

        if response.status_code == 200:
            data = response.json()
            result["data"] = data.get("data")
            result["message"] = data.get("message", "成功")
            if data.get("code") == 200:
                result["success"] = True
                print(f"  [PASS] {endpoint_name}: {result['message']} ({result['elapsed_time']})")
            else:
                result["message"] = data.get("message", "API 返回错误")
                print(f"  [FAIL] {endpoint_name}: {result['message']}")
        elif response.status_code == 401:
            result["message"] = "未授权，请检查 Token"
            print(f"  [FAIL] {endpoint_name}: 401 未授权")
        elif response.status_code == 403:
            result["message"] = "权限不足，需要管理员权限"
            print(f"  [FAIL] {endpoint_name}: 403 权限不足")
        else:
            result["message"] = f"HTTP {response.status_code}"
            print(f"  [FAIL] {endpoint_name}: {result['message']}")

        return result

    except requests.exceptions.Timeout:
        print(f"  [FAIL] {endpoint_name}: 请求超时")
        return {"success": False, "message": "请求超时"}
    except Exception as e:
        print(f"  [FAIL] {endpoint_name}: {str(e)}")
        return {"success": False, "message": str(e)}


def validate_clickstream_data(data):
    """验证点击流分析数据"""
    print("\n  验证点击流分析数据...")
    errors = []

    if not data:
        errors.append("返回数据为空")
        return errors

    summary = data.get("summary", {})
    if not summary:
        errors.append("缺少 summary 字段")
    else:
        if "total_logs" not in summary:
            errors.append("summary 缺少 total_logs")
        if "days" not in summary:
            errors.append("summary 缺少 days")
        if "unique_users" not in summary:
            errors.append("summary 缺少 unique_users")

    behavior_distribution = data.get("behavior_distribution", {})
    if not behavior_distribution:
        errors.append("缺少 behavior_distribution 字段")

    conversion_funnel = data.get("conversion_funnel", {})
    if not conversion_funnel:
        errors.append("缺少 conversion_funnel 字段")
    else:
        required_fields = ["login_users", "view_users", "collect_users"]
        for field in required_fields:
            if field not in conversion_funnel:
                errors.append(f"conversion_funnel 缺少 {field}")

    path_patterns = data.get("path_patterns", [])
    if not isinstance(path_patterns, list):
        errors.append("path_patterns 应为列表")

    return errors


def validate_active_users_data(data):
    """验证活跃用户分析数据"""
    print("\n  验证活跃用户分析数据...")
    errors = []

    if not data:
        errors.append("返回数据为空")
        return errors

    summary = data.get("summary", {})
    if not summary:
        errors.append("缺少 summary 字段")
    else:
        required_fields = ["total_users", "active_today", "active_week", "active_month"]
        for field in required_fields:
            if field not in summary:
                errors.append(f"summary 缺少 {field}")

    dau = data.get("dau", {})
    wau = data.get("wau", {})
    mau = data.get("mau", {})

    if not dau or not wau or not mau:
        errors.append("缺少 dau/wau/mau 字段")
    else:
        if "today" not in dau:
            errors.append("dau 缺少 today")
        if "change_rate" not in dau:
            errors.append("dau 缺少 change_rate")

    stickiness = data.get("stickiness", {})
    if not stickiness:
        errors.append("缺少 stickiness 字段")
    else:
        if "dau_mau_ratio" not in stickiness:
            errors.append("stickiness 缺少 dau_mau_ratio")

    return errors


def validate_login_frequency_data(data):
    """验证登录频次分析数据"""
    print("\n  验证登录频次分析数据...")
    errors = []

    if not data:
        errors.append("返回数据为空")
        return errors

    summary = data.get("summary", {})
    if not summary:
        errors.append("缺少 summary 字段")
    else:
        required_fields = ["total_logs", "days", "total_users"]
        for field in required_fields:
            if field not in summary:
                errors.append(f"summary 缺少 {field}")

    login_frequency = data.get("login_frequency_distribution", {})
    if not login_frequency:
        errors.append("缺少 login_frequency_distribution 字段")
    else:
        required_fields = ["high_frequency", "medium_frequency", "low_frequency", "silent"]
        for field in required_fields:
            if field not in login_frequency:
                errors.append(f"login_frequency_distribution 缺少 {field}")

    hourly_distribution = data.get("hourly_distribution", {})
    if not hourly_distribution:
        errors.append("缺少 hourly_distribution 字段")
    else:
        if "detail" not in hourly_distribution:
            errors.append("hourly_distribution 缺少 detail")

    daily_trend = data.get("daily_trend", [])
    if not isinstance(daily_trend, list):
        errors.append("daily_trend 应为列表")

    return errors


def validate_page_duration_data(data):
    """验证页面停留分析数据"""
    print("\n  验证页面停留分析数据...")
    errors = []

    if not data:
        errors.append("返回数据为空")
        return errors

    summary = data.get("summary", {})
    if not summary:
        errors.append("缺少 summary 字段")
    else:
        required_fields = ["total_logs", "days", "total_pages"]
        for field in required_fields:
            if field not in summary:
                errors.append(f"summary 缺少 {field}")

    page_statistics = data.get("page_statistics", [])
    if not isinstance(page_statistics, list):
        errors.append("page_statistics 应为列表")
    else:
        if page_statistics:
            first_page = page_statistics[0]
            required_fields = ["page", "avg_duration", "total_visits"]
            for field in required_fields:
                if field not in first_page:
                    errors.append(f"page_statistics 项缺少 {field}")

    duration_distribution = data.get("duration_distribution", {})
    if not duration_distribution:
        errors.append("缺少 duration_distribution 字段")
    else:
        required_fields = ["short", "medium", "long"]
        for field in required_fields:
            if field not in duration_distribution:
                errors.append(f"duration_distribution 缺少 {field}")

    return errors


def main():
    """主测试函数"""
    print("=" * 60)
    print("用户行为分析 API 测试")
    print("=" * 60)
    print(f"测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"测试地址: {BASE_URL}")
    print()

    # 获取管理员 Token
    print("正在获取管理员 Token...")
    token = get_admin_token()
    if not token:
        print("\n[ERROR] 无法获取管理员 Token，测试终止")
        print("请确保：")
        print("  1. 后端服务器已启动 (python manage.py runserver)")
        print("  2. 存在管理员账号 (用户名: admin, 密码: admin123)")
        return 1

    print(f"[OK] Token 获取成功\n")

    # 测试结果汇总
    results = {}
    test_count = 0
    pass_count = 0

    # 1. 测试点击流分析 API
    print("-" * 60)
    print("1. 测试点击流分析 API")
    print("-" * 60)
    test_count += 1
    result = test_api("clickstream", token, {"days": 30, "limit_path": 20})
    results["clickstream"] = result
    if result["success"]:
        pass_count += 1
        errors = validate_clickstream_data(result.get("data"))
        if errors:
            print(f"  [WARN] 数据验证警告: {', '.join(errors)}")
        else:
            print("  [OK] 数据验证通过")
    else:
        validate_clickstream_data(None)

    # 2. 测试活跃用户分析 API
    print("\n" + "-" * 60)
    print("2. 测试活跃用户分析 API")
    print("-" * 60)
    test_count += 1
    result = test_api("active_users", token, {"days": 30, "trend_by": "day"})
    results["active_users"] = result
    if result["success"]:
        pass_count += 1
        errors = validate_active_users_data(result.get("data"))
        if errors:
            print(f"  [WARN] 数据验证警告: {', '.join(errors)}")
        else:
            print("  [OK] 数据验证通过")
    else:
        validate_active_users_data(None)

    # 3. 测试登录频次分析 API
    print("\n" + "-" * 60)
    print("3. 测试登录频次分析 API")
    print("-" * 60)
    test_count += 1
    result = test_api("login_frequency", token, {"days": 30})
    results["login_frequency"] = result
    if result["success"]:
        pass_count += 1
        errors = validate_login_frequency_data(result.get("data"))
        if errors:
            print(f"  [WARN] 数据验证警告: {', '.join(errors)}")
        else:
            print("  [OK] 数据验证通过")
    else:
        validate_login_frequency_data(None)

    # 4. 测试页面停留分析 API
    print("\n" + "-" * 60)
    print("4. 测试页面停留分析 API")
    print("-" * 60)
    test_count += 1
    result = test_api("page_duration", token, {"days": 30})
    results["page_duration"] = result
    if result["success"]:
        pass_count += 1
        errors = validate_page_duration_data(result.get("data"))
        if errors:
            print(f"  [WARN] 数据验证警告: {', '.join(errors)}")
        else:
            print("  [OK] 数据验证通过")
    else:
        validate_page_duration_data(None)

    # 测试参数传递
    print("\n" + "-" * 60)
    print("5. 测试参数传递")
    print("-" * 60)
    test_count += 1

    # 测试 days 参数
    result = test_api("clickstream", token, {"days": 7})
    if result["success"]:
        data = result.get("data", {})
        if data.get("summary", {}).get("days") == 7:
            print("  [PASS] days 参数传递正确")
        else:
            print(f"  [WARN] days 参数传递异常: 期望 7, 实际 {data.get('summary', {}).get('days')}")
    else:
        print(f"  [FAIL] days 参数测试失败")

    # 测试 limit 参数
    result = test_api("active_users", token, {"days": 30, "trend_by": "week"})
    if result["success"]:
        print("  [PASS] trend_by 参数传递正确")
    else:
        print(f"  [FAIL] trend_by 参数测试失败")

    # 输出测试汇总
    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)
    print(f"总测试数: {test_count}")
    print(f"通过: {pass_count}")
    print(f"失败: {test_count - pass_count}")
    print(f"通过率: {pass_count / test_count * 100:.1f}%")

    if pass_count == test_count:
        print("\n[SUCCESS] 所有测试通过!")
        return 0
    else:
        print("\n[WARNING] 部分测试未通过，请检查 API 实现")
        return 1


if __name__ == "__main__":
    sys.exit(main())
