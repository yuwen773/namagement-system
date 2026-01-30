# -*- coding: utf-8 -*-
"""
简单测试脚本 - 测试单个菜谱的爬取
"""

import sys
import time

# Windows 控制台编码修复
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

from request_utils import get_request_utils
from parser_utils import parse_recipe_detail


def test_single_recipe():
    """测试单个菜谱爬取"""
    print("=" * 50)
    print("测试爬虫 - 单个菜谱")
    print("=" * 50)

    # 使用一个可能存在的菜谱 ID
    recipe_id = 100000
    url = f"https://www.xiachufang.com/recipe/{recipe_id}/"

    print(f"\n目标 URL: {url}")
    print("\n等待 5 秒后开始请求...")
    time.sleep(5)

    try:
        print("\n1. 发送 HTTP 请求...")
        request_utils = get_request_utils()
        response = request_utils.get(url)

        print(f"   状态码: {response.status_code}")
        print(f"   内容长度: {len(response.text)}")

        if response.status_code == 429:
            print("\n   [警告] 请求被限流 (429)")
            print("   建议: 等待更长时间再试，或使用代理 IP")
            return

        if response.status_code != 200:
            print(f"\n   [错误] 请求失败: {response.status_code}")
            return

        print("\n2. 解析 HTML 内容...")
        recipe_data = parse_recipe_detail(response.text)

        print("\n3. 解析结果:")
        print(f"   菜谱名称: {recipe_data.get('name')}")
        print(f"   图片 URL: {recipe_data.get('image_url')}")
        print(f"   菜系: {recipe_data.get('cuisine_type')}")
        print(f"   难度: {recipe_data.get('difficulty')}")
        print(f"   烹饪时间: {recipe_data.get('cooking_time')} 分钟")
        print(f"   食材数量: {len(recipe_data.get('ingredients', []))}")
        print(f"   步骤数量: {len(recipe_data.get('steps', []))}")

        if recipe_data.get('ingredients'):
            print("\n   食材列表:")
            for ing in recipe_data['ingredients'][:5]:
                print(f"     - {ing.get('name')}: {ing.get('amount')}")
            if len(recipe_data['ingredients']) > 5:
                print(f"     ... 还有 {len(recipe_data['ingredients']) - 5} 种")

        if recipe_data.get('steps'):
            print("\n   制作步骤（前3步）:")
            for i, step in enumerate(recipe_data['steps'][:3], 1):
                print(f"     {i}. {step[:50]}...")

        print("\n" + "=" * 50)
        print("[成功] 测试完成！")
        print("=" * 50)

        request_utils.close()

    except Exception as e:
        print(f"\n[错误] {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_single_recipe()
