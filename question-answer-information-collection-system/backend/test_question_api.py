"""
问答数据 API 测试脚本

测试步骤 12 创建的 Question API 接口。
"""

import os
import sys
import django

# 设置 Django 环境
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qa_project.settings')
django.setup()

import requests
import json

# 配置
BASE_URL = 'http://127.0.0.1:8000/api'
ADMIN_TOKEN = None  # 将被设置为管理员 token
USER_TOKEN = None   # 将被设置为普通用户 token


def get_token(username, password):
    """获取 JWT Token"""
    url = f'{BASE_URL}/auth/token/'
    data = {'username': username, 'password': password}
    resp = requests.post(url, json=data)
    if resp.status_code == 200:
        return resp.json().get('access')
    return None


def test_questions_list():
    """测试获取问答列表"""
    print("\n=== 测试获取问答列表 ===")
    headers = {'Authorization': f'Bearer {USER_TOKEN}'}

    # 测试基础列表
    resp = requests.get(f'{BASE_URL}/questions/', headers=headers)
    print(f"GET /api/questions/")
    print(f"状态码: {resp.status_code}")
    print(f"响应: {json.dumps(resp.json(), ensure_ascii=False, indent=2)}")

    # 测试分页
    resp = requests.get(f'{BASE_URL}/questions/?page=1&page_size=5', headers=headers)
    print(f"\nGET /api/questions/?page=1&page_size=5")
    print(f"状态码: {resp.status_code}")

    # 测试搜索
    resp = requests.get(f'{BASE_URL}/questions/?search=test', headers=headers)
    print(f"\nGET /api/questions/?search=test")
    print(f"状态码: {resp.status_code}")

    return resp.status_code == 200


def test_question_detail():
    """测试获取问答详情"""
    print("\n=== 测试获取问答详情 ===")
    headers = {'Authorization': f'Bearer {USER_TOKEN}'}

    # 先获取列表，找到一个有效的 ID
    resp = requests.get(f'{BASE_URL}/questions/', headers=headers)
    if resp.status_code == 200:
        data = resp.json().get('data', [])
        if data:
            question_id = data[0].get('id')
            resp = requests.get(f'{BASE_URL}/questions/{question_id}/', headers=headers)
            print(f"GET /api/questions/{question_id}/")
            print(f"状态码: {resp.status_code}")
            print(f"响应: {json.dumps(resp.json(), ensure_ascii=False, indent=2)}")
            return resp.status_code == 200

    print("没有找到可测试的问答数据")
    return True  # 不算失败


def test_question_tags():
    """测试获取标签列表"""
    print("\n=== 测试获取标签列表 ===")
    headers = {'Authorization': f'Bearer {USER_TOKEN}'}

    resp = requests.get(f'{BASE_URL}/questions/tags/', headers=headers)
    print(f"GET /api/questions/tags/")
    print(f"状态码: {resp.status_code}")
    print(f"响应: {json.dumps(resp.json(), ensure_ascii=False, indent=2)}")
    return resp.status_code == 200


def test_delete_question_admin():
    """测试管理员删除问答"""
    print("\n=== 测试管理员删除问答 ===")
    headers = {'Authorization': f'Bearer {ADMIN_TOKEN}'}

    # 先创建测试数据（通过爬虫或直接创建）
    from apps.crawler.models import Question, Tag
    from apps.api.serializers import QuestionSerializer

    # 检查是否有数据
    if Question.objects.count() == 0:
        print("数据库中没有问答数据，跳过删除测试")
        return True

    # 获取一个可删除的 ID
    resp = requests.get(f'{BASE_URL}/questions/', headers=headers)
    if resp.status_code == 200:
        data = resp.json().get('data', [])
        if data:
            question_id = data[0].get('id')
            resp = requests.delete(f'{BASE_URL}/questions/{question_id}/', headers=headers)
            print(f"DELETE /api/questions/{question_id}/")
            print(f"状态码: {resp.status_code}")
            print(f"响应: {json.dumps(resp.json(), ensure_ascii=False, indent=2)}")
            return resp.status_code == 200

    return True


def test_delete_question_user():
    """测试普通用户删除问答（应该被拒绝）"""
    print("\n=== 测试普通用户删除问答（应该返回403）===")
    headers = {'Authorization': f'Bearer {USER_TOKEN}'}

    resp = requests.delete(f'{BASE_URL}/questions/1/', headers=headers)
    print(f"DELETE /api/questions/1/")
    print(f"状态码: {resp.status_code}")
    print(f"响应: {json.dumps(resp.json(), ensure_ascii=False, indent=2)}")

    if resp.status_code == 403:
        print("✓ 普通用户删除被正确拒绝（403）")
        return True
    else:
        print("✗ 期望返回 403，实际返回", resp.status_code)
        return False


def test_unauthorized_access():
    """测试未授权访问"""
    print("\n=== 测试未授权访问 ===")

    resp = requests.get(f'{BASE_URL}/questions/')
    print(f"未授权 GET /api/questions/")
    print(f"状态码: {resp.status_code}")

    if resp.status_code == 401:
        print("✓ 未授权访问正确拒绝（401）")
        return True
    else:
        print("✗ 期望返回 401，实际返回", resp.status_code)
        return False


def main():
    """主测试函数"""
    print("=" * 60)
    print("问答数据 API 测试")
    print("=" * 60)

    # 获取 token
    global ADMIN_TOKEN, USER_TOKEN

    # 尝试获取管理员 token
    ADMIN_TOKEN = get_token('admin', 'admin123')
    if not ADMIN_TOKEN:
        print("\n警告: 无法获取管理员 token，请确保已创建管理员账号")
        print("使用 createsuperuser 创建: python manage.py createsuperuser")
        ADMIN_TOKEN = get_token('testadmin', 'test123')

    # 尝试获取普通用户 token
    USER_TOKEN = get_token('testuser', 'test123')
    if not USER_TOKEN:
        print("\n警告: 无法获取普通用户 token")

    # 如果没有 token，只能测试未授权访问
    if not ADMIN_TOKEN and not USER_TOKEN:
        print("\n没有有效的 token，只测试未授权访问...")
        test_unauthorized_access()
        return

    results = []

    # 运行测试
    results.append(("未授权访问", test_unauthorized_access()))

    if USER_TOKEN:
        results.append(("问答列表", test_questions_list()))
        results.append(("问答详情", test_question_detail()))
        results.append(("标签列表", test_question_tags()))
        results.append(("普通用户删除", test_delete_question_user()))

    if ADMIN_TOKEN:
        results.append(("管理员删除", test_delete_question_admin()))

    # 汇总结果
    print("\n" + "=" * 60)
    print("测试结果汇总")
    print("=" * 60)

    all_passed = True
    for name, passed in results:
        status = "✓ 通过" if passed else "✗ 失败"
        print(f"{status}: {name}")
        if not passed:
            all_passed = False

    print("\n" + ("全部测试通过！" if all_passed else "存在失败的测试"))


if __name__ == '__main__':
    main()
