#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Data Scripts Directory Structure Test Script

Verify that all data scripts directories are created correctly and test basic functionality.
"""

import os
import sys
from pathlib import Path


def test_directory_structure():
    """Test data scripts directory structure"""
    print("=" * 60)
    print("Data Scripts Directory Structure Test")
    print("=" * 60)

    # Get current script directory
    base_dir = Path(__file__).parent
    print(f"\nBase directory: {base_dir}")

    # 定义期望的子目录
    subdirs = ['spiders', 'cleaning', 'importing', 'simulation']

    # 测试结果
    all_passed = True

    # 检查每个子目录
    print("\n检查子目录:")
    for subdir in subdirs:
        subdir_path = base_dir / subdir
        exists = subdir_path.exists()
        status = "[OK]" if exists else "[FAIL]"
        print(f"  {status} {subdir}/")

        if not exists:
            all_passed = False
        else:
            # 检查 README 是否存在
            readme_path = subdir_path / 'README.md'
            if readme_path.exists():
                print(f"      - README.md exists")
            else:
                print(f"      - README.md not found (optional)")

    # 测试 Python 导入
    print("\n测试 Python 环境导入:")
    try:
        import json
        print("  [OK] json module available (data format processing)")
    except ImportError:
        print("  [FAIL] json module not available")
        all_passed = False

    try:
        import random
        print("  [OK] random module available (random data generation)")
    except ImportError:
        print("  [FAIL] random module not available")
        all_passed = False

    # 测试文件读写
    print("\n测试文件读写:")
    test_file = base_dir / 'test_write.tmp'
    try:
        test_file.write_text('test write', encoding='utf-8')
        content = test_file.read_text(encoding='utf-8')
        test_file.unlink()
        print("  [OK] file read/write normal")
    except Exception as e:
        print(f"  [FAIL] file read/write failed: {e}")
        all_passed = False

    # 测试 JSON 处理
    print("\n测试 JSON 处理:")
    try:
        test_data = {
            "name": "test recipe",
            "cuisine": "Sichuan",
            "difficulty": "easy",
            "ingredients": ["potato", "beef"]
        }
        json_str = json.dumps(test_data, ensure_ascii=False, indent=2)
        parsed = json.loads(json_str)
        print("  [OK] JSON serialize/deserialize normal")
    except Exception as e:
        print(f"  [FAIL] JSON processing failed: {e}")
        all_passed = False

    # 检查后端配置
    print("\n检查后端项目:")
    backend_dir = base_dir.parent / 'backend'
    if backend_dir.exists():
        print("  [OK] backend/ directory exists")

        # 检查 Django 项目
        settings_file = backend_dir / 'config' / 'settings.py'
        if settings_file.exists():
            print("  [OK] Django config file exists")

            # 尝试读取数据库配置
            try:
                with open(settings_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'DATABASES' in content:
                        print("  [OK] database config exists")
                    if 'mysql' in content.lower():
                        print("  [OK] MySQL driver configured")
            except Exception as e:
                print(f"  [WARN] cannot read config: {e}")
        else:
            print("  [WARN] Django config file not found")
    else:
        print("  [WARN] backend/ directory not found")

    # 总结
    print("\n" + "=" * 60)
    if all_passed:
        print("[SUCCESS] All tests passed! Data scripts directory structure is correct.")
        print("\nNext steps:")
        print("  1. spiders/ - Write web scraper scripts")
        print("  2. cleaning/ - Write data cleaning scripts")
        print("  3. importing/ - Write data import scripts")
        print("  4. simulation/ - Write behavior simulation scripts")
        return 0
    else:
        print("[FAILED] Some tests failed, please check directory structure.")
        return 1


if __name__ == '__main__':
    sys.exit(test_directory_structure())
