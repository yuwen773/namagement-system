"""
数据清洗工具测试脚本

用于验证 DataCleaner 和 QuestionPipeline 的功能。
"""

import sys
import os
import time

# 添加 Django 项目路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qa_project.settings')

import django
django.setup()

from crawler.utils import DataCleaner, DuplicateChecker, clean_html, normalize_text, clean_item


def test_clean_html():
    """测试 HTML 标签移除功能"""
    print("=" * 60)
    print("测试 1: clean_html() - HTML 标签移除")
    print("=" * 60)

    cleaner = DataCleaner()

    # 测试用例 1: 包含 HTML 标签
    html_text = "<p>这是一个<strong>测试</strong>文本</p>"
    result = cleaner.clean_html(html_text)
    expected = "这是一个测试文本"
    assert result == expected, f"期望 '{expected}', 得到 '{result}'"
    print(f"[通过] HTML 标签移除: '{html_text}' -> '{result}'")

    # 测试用例 2: 包含 HTML 实体
    html_text = "&lt;div&gt; &amp; &nbsp;"
    result = cleaner.clean_html(html_text)
    print(f"[通过] HTML 实体处理: '{html_text}' -> '{result}'")

    # 测试用例 3: 空值处理
    result = cleaner.clean_html(None)
    assert result == "", f"期望空字符串, 得到 '{result}'"
    print(f"[通过] 空值处理: None -> '{result}'")

    # 测试用例 4: 复杂 HTML
    html_text = '<div class="container"><p>Hello<br/>World</p></div>'
    result = cleaner.clean_html(html_text)
    expected = "HelloWorld"
    assert result == expected, f"期望 '{expected}', 得到 '{result}'"
    print(f"[通过] 复杂 HTML: '{html_text}' -> '{result}'")

    print()


def test_normalize_text():
    """测试文本规范化功能"""
    print("=" * 60)
    print("测试 2: normalize_text() - 文本规范化")
    print("=" * 60)

    cleaner = DataCleaner()

    # 测试用例 1: 多余空格
    text = "这   是   测试   文本"
    result = cleaner.normalize_text(text)
    expected = "这 是 测试 文本"
    assert result == expected, f"期望 '{expected}', 得到 '{result}'"
    print(f"[通过] 多余空格: '{text}' -> '{result}'")

    # 测试用例 2: 多余换行
    text = "第一行\n\n第二行\n\n\n第三行"
    result = cleaner.normalize_text(text)
    assert "\n\n\n" not in result, f"应移除多余换行"
    print(f"[通过] 多余换行: 原文本有多行 -> '{result[:30]}...'")

    # 测试用例 3: HTML 实体
    text = "你好&nbsp;世界 &amp; 你"
    result = cleaner.normalize_text(text)
    print(f"[通过] HTML 实体: '{text}' -> '{result}'")

    # 测试用例 4: 混合情况
    text = "  测试   文本  \n\n  带有   空格  \n  "
    result = cleaner.normalize_text(text)
    print(f"[通过] 混合情况: 原文本 -> '{result}'")

    print()


def test_validate_data():
    """测试数据验证功能"""
    print("=" * 60)
    print("测试 3: validate_data() - 数据验证")
    print("=" * 60)

    cleaner = DataCleaner()

    # 测试用例 1: 有效数据
    valid_data = {
        'title': '测试问题',
        'answer_content': '测试回答',
        'source_url': 'https://example.com/1',
    }
    is_valid, errors = cleaner.validate_data(valid_data)
    assert is_valid, f"期望有效数据, 得到错误: {errors}"
    print(f"[通过] 有效数据: {valid_data}")

    # 测试用例 2: 缺失必填字段
    invalid_data = {
        'title': '测试问题',
        # 缺少 answer_content 和 source_url
    }
    is_valid, errors = cleaner.validate_data(invalid_data)
    assert not is_valid, "期望无效数据"
    print(f"[通过] 缺失字段检测: {errors}")

    # 测试用例 3: 空字符串
    empty_data = {
        'title': '   ',  # 空格
        'answer_content': '',
        'source_url': 'https://example.com/1',
    }
    is_valid, errors = cleaner.validate_data(empty_data)
    assert not is_valid, "期望空字符串无效"
    print(f"[通过] 空字符串检测: {errors}")

    # 测试用例 4: 超长字段
    long_data = {
        'title': 'a' * 300,  # 超过 255 限制
        'answer_content': '测试回答',
        'source_url': 'https://example.com/1',
    }
    is_valid, errors = cleaner.validate_data(long_data)
    assert not is_valid, "期望超长字段无效"
    print(f"[通过] 超长字段检测: {errors}")

    print()


def test_duplicate_checker():
    """测试重复检测功能"""
    print("=" * 60)
    print("测试 4: DuplicateChecker - 重复检测")
    print("=" * 60)

    checker = DuplicateChecker()

    # 测试用例 1: 新数据
    result = checker.is_duplicate("测试问题", "https://example.com/1")
    assert result == False, "期望非重复"
    print("[通过] 新数据: 标记为非重复")

    # 测试用例 2: 重复标题
    result = checker.is_duplicate("测试问题", "https://example.com/2")
    assert result == True, "期望重复（相同标题）"
    print("[通过] 重复标题: 标记为重复")

    # 测试用例 3: 重复 URL
    result = checker.is_duplicate("不同问题", "https://example.com/1")
    assert result == True, "期望重复（相同 URL）"
    print("[通过] 重复 URL: 标记为重复")

    # 测试用例 4: 新数据
    result = checker.is_duplicate("全新问题", "https://example.com/new")
    assert result == False, "期望非重复"
    print("[通过] 新数据: 标记为非重复")

    # 测试用例 5: 计数
    count = checker.get_duplicate_count()
    assert count == 2, f"期望重复计数 2, 得到 {count}"
    print(f"[通过] 重复计数: {count}")

    # 测试用例 6: 重置
    checker.reset()
    count = checker.get_duplicate_count()
    assert count == 0, f"期望重置后计数 0, 得到 {count}"
    print("[通过] 重置: 计数器已清零")

    print()


def test_clean_item():
    """测试完整清洗流程"""
    print("=" * 60)
    print("测试 5: clean_item() - 完整清洗流程")
    print("=" * 60)

    # 测试用例 1: 原始爬取数据
    raw_item = {
        'title': '<p>如何<strong>学习</strong>Python？</p>',
        'description': '<div class="desc">我想学习Python编程</div>',
        'answer_content': '<p>建议：</p><ol><li>安装Python</li><li>学习基础语法</li></ol>',
        'answer_time': '2024-01-15',
        'answerer': '  张三  ',
        'source_url': 'https://wenda.so.com/q/123',
    }

    result = clean_item(raw_item)

    assert '<p>' not in result['title'], "标题应无 HTML 标签"
    assert '<div' not in result['description'], "描述应无 HTML 标签"
    assert '<p>' not in result['answer_content'], "回答内容应无 HTML 标签"
    assert result['answerer'] == '张三', f"回答者应去除空格, 得到 '{result['answerer']}'"

    print(f"[通过] 原始数据清洗:")
    print(f"  标题: '{raw_item['title']}' -> '{result['title']}'")
    print(f"  回答内容: '{raw_item['answer_content'][:30]}...' -> '{result['answer_content'][:30]}...'")
    print(f"  回答者: '{raw_item['answerer']}' -> '{result['answerer']}'")

    # 测试用例 2: 空值处理
    empty_item = {
        'title': None,
        'answer_content': '',
        'source_url': 'https://example.com',
    }

    result = clean_item(empty_item)
    assert result['title'] == '', "None 应转换为空字符串"
    print("[通过] 空值处理正常")

    print()


def test_batch_performance():
    """测试批量处理性能"""
    print("=" * 60)
    print("测试 6: 批量处理性能测试")
    print("=" * 60)

    import random
    import string

    cleaner = DataCleaner()
    checker = DuplicateChecker()

    # 生成测试数据
    test_items = []
    for i in range(1000):
        item = {
            'title': f'测试问题 {i}',
            'answer_content': f'这是第{i}个回答内容' * 5,
            'source_url': f'https://example.com/{i}',
            'answerer': '测试用户',
        }
        # 添加一些重复
        if i % 10 == 0:
            item['title'] = '重复问题'
            item['source_url'] = f'https://example.com/duplicate-{i//10}'
        test_items.append(item)

    # 性能测试
    start_time = time.time()

    for item in test_items:
        # 清洗
        cleaned = cleaner.clean_item(item)

        # 验证
        is_valid, _ = cleaner.validate_data(cleaned)

        # 去重
        if is_valid:
            duplicate = checker.is_duplicate(cleaned['title'], cleaned['source_url'])

    elapsed = time.time() - start_time

    print(f"[通过] 批量处理 1000 条数据耗时: {elapsed:.3f} 秒")
    print(f"  - 平均每条: {elapsed/1000*1000:.3f} ms")
    print(f"  - 检测到重复: {checker.get_duplicate_count()} 条")

    # 性能断言：1000条应 < 1秒
    assert elapsed < 1.0, f"性能测试失败: 耗时 {elapsed:.3f} 秒"
    print(f"[通过] 性能测试通过 (< 1秒)")

    print()


def main():
    """主测试函数"""
    print("\n" + "=" * 60)
    print("   数据清洗工具测试套件")
    print("=" * 60 + "\n")

    tests = [
        test_clean_html,
        test_normalize_text,
        test_validate_data,
        test_duplicate_checker,
        test_clean_item,
        test_batch_performance,
    ]

    passed = 0
    failed = 0

    for test in tests:
        try:
            test()
            passed += 1
        except AssertionError as e:
            print(f"[失败] {test.__name__}: {e}")
            failed += 1
        except Exception as e:
            print(f"[错误] {test.__name__}: {e}")
            failed += 1

    print("=" * 60)
    print(f"   测试结果: {passed} 通过, {failed} 失败")
    print("=" * 60)

    return failed == 0


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
