"""
爬虫模块导入测试

验证爬虫组件是否正确配置。
"""

import os
import sys

# 强制 UTF-8 编码
os.environ['PYTHONIOENCODING'] = 'utf-8'

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'qa_project.settings')
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

import django
django.setup()


def test_imports():
    """测试模块导入"""
    print("测试爬虫模块导入...")

    # 测试 items
    print("\n1. 测试 items.py...")
    from apps.crawler.items import QuestionItem, create_question_item
    item = QuestionItem(
        title="测试问题",
        answer_content="测试回答",
        source_url="https://wenda.so.com/test"
    )
    print(f"   QuestionItem 创建成功: {dict(item)}")
    print("   [OK]")

    # 测试 utils
    print("\n2. 测试 utils.py...")
    from apps.crawler.utils import DataCleaner, DuplicateChecker
    cleaner = DataCleaner()
    cleaned = cleaner.clean_html("<p>Hello <b>World</b></p>")
    assert cleaned == "Hello World", f"Expected 'Hello World', got '{cleaned}'"
    print(f"   clean_html 测试通过: '{cleaned}'")
    print("   [OK]")

    # 测试 pipelines
    print("\n3. 测试 pipelines.py...")
    from apps.crawler.pipelines import QuestionPipeline
    pipeline = QuestionPipeline()
    print("   QuestionPipeline 创建成功")
    print("   [OK]")

    # 测试 settings
    print("\n4. 测试 settings.py...")
    from apps.crawler.settings import (
        BOT_NAME,
        DOWNLOAD_DELAY,
        PLAYWRIGHT_ENABLED,
        USER_AGENT_LIST
    )
    print(f"   BOT_NAME: {BOT_NAME}")
    print(f"   DOWNLOAD_DELAY: {DOWNLOAD_DELAY}")
    print(f"   PLAYWRIGHT_ENABLED: {PLAYWRIGHT_ENABLED}")
    print(f"   USER_AGENT_COUNT: {len(USER_AGENT_LIST)}")
    print("   [OK]")

    # 测试 spider
    print("\n5. 测试 spiders/wenda_spider.py...")
    try:
        from apps.crawler.spiders import WendaSpider
        spider = WendaSpider(mode='demo', limit=5)
        print(f"   Spider 名称: {spider.name}")
        print(f"   允许域名: {spider.allowed_domains}")
        print(f"   采集模式: {spider.mode}")
        print(f"   采集限制: {spider.limit}")
        print("   [OK]")
    except Exception as e:
        print(f"   [FAIL] 导入失败: {e}")
        raise

    print("\n" + "=" * 50)
    print("所有测试通过！爬虫模块配置正确。")
    print("=" * 50)

    # 打印运行命令
    print("\n运行爬虫命令:")
    print("  演示模式 (20条): python crawl.py --mode demo")
    print("  全量模式 (100条): python crawl.py --mode full --limit 100")
    print("  Scrapy 原生命令: scrapy crawl wenda_360 -o output.json")


def test_data_cleaner():
    """测试数据清洗功能"""
    print("\n数据清洗功能测试...")

    from apps.crawler.utils import DataCleaner

    cleaner = DataCleaner()

    # 测试 HTML 清洗
    test_cases = [
        ("<p>Hello World</p>", "Hello World"),
        ("<a href='#'>Link</a>", "Link"),
        ("<script>alert('xss')</script>", "alert('xss')"),
    ]

    for html, expected in test_cases:
        result = cleaner.clean_html(html)
        assert result == expected, f"Expected '{expected}', got '{result}'"
        print(f"  clean_html('{html}') = '{result}' [OK]")

    # 测试文本规范化
    test_cases = [
        ("Hello   World", "Hello World"),
        ("Hello\n\nWorld", "Hello\nWorld"),
        ("  Hello World  ", "Hello World"),
    ]

    for text, expected in test_cases:
        result = cleaner.normalize_text(text)
        assert result == expected, f"Expected '{expected}', got '{result}'"
        print(f"  normalize_text('{text}') = '{result}' [OK]")

    # 测试数据验证
    valid_data = {
        'title': '测试问题',
        'answer_content': '测试回答',
        'source_url': 'https://wenda.so.com/test'
    }
    is_valid, errors = cleaner.validate_data(valid_data)
    assert is_valid, f"Expected valid, got errors: {errors}"
    print(f"  有效数据验证通过 [OK]")

    invalid_data = {
        'title': '',
        'answer_content': '测试回答',
        'source_url': 'https://wenda.so.com/test'
    }
    is_valid, errors = cleaner.validate_data(invalid_data)
    assert not is_valid, "Expected invalid"
    print(f"  无效数据检测通过 [OK]")

    print("\n数据清洗测试全部通过！")


if __name__ == '__main__':
    test_imports()
    test_data_cleaner()
