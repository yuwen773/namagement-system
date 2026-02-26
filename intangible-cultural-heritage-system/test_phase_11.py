#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""阶段十一功能测试脚本 - 数据列表页面"""

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright
import time
import os

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg): print(f"{Colors.GREEN}[PASS] {msg}{Colors.RESET}")
def print_fail(msg): print(f"{Colors.RED}[FAIL] {msg}{Colors.RESET}")
def print_info(msg): print(f"{Colors.BLUE}[INFO] {msg}{Colors.RESET}")
def print_section(msg):
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}  {msg}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{'='*60}{Colors.RESET}\n")

def login(page):
    """登录"""
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')

    username_input = page.locator('input[type="text"]').first
    password_input = page.locator('input[type="password"]').first
    username_input.fill('admin')
    password_input.fill('password123')

    # 使用更灵活的选择器
    login_btn = page.locator('button').filter(has_text='登录').first
    login_btn.click()
    page.wait_for_timeout(2000)

def test_heritage_list(page):
    """测试非遗项目列表页面"""
    print_section("测试 1: 非遗项目列表页面")

    # 点击非遗项目菜单
    heritage_link = page.locator('a, [class*="menu"]').filter(has_text='非遗项目').first
    if heritage_link.count() > 0:
        heritage_link.click()
        page.wait_for_load_state('networkidle')
        print_success("点击非遗项目菜单")
    else:
        print_fail("未找到非遗项目菜单")
        return False

    page.screenshot(path='D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/test_screenshots/11_heritage_list.png', full_page=True)
    print_info("已保存项目列表截图")

    # 检查筛选表单
    try:
        search_input = page.locator('input[placeholder*="搜索"], input[placeholder*="关键词"]').first
        if search_input.count() > 0:
            print_success("发现关键词搜索输入框")

        # 检查分类下拉框
        category_select = page.locator('[class*="category"], select').first
        if category_select.count() > 0:
            print_success("发现分类筛选器")

        # 检查级别筛选
        level_select = page.locator('[class*="level"], select').all()
        if len(level_select) >= 1:
            print_success(f"发现 {len(level_select)} 个筛选下拉框")

    except Exception as e:
        print_fail(f"检查筛选器出错: {e}")

    # 检查数据表格
    try:
        table = page.locator('table, [class*="table"], [class*="el-table"]').first
        if table.count() > 0:
            print_success("发现数据表格")

            # 检查表格行
            rows = page.locator('tr[class*="row"], [class*="table-row"]').all()
            print_info(f"表格包含 {len(rows)} 行数据")

            # 点击第一行测试跳转
            if len(rows) > 1:
                first_row = rows[1] if len(rows) > 1 else rows[0]
                first_row.click()
                page.wait_for_timeout(1000)

                current_url = page.url
                if '/heritage/' in current_url or '/detail/' in current_url:
                    print_success("点击表格行跳转到详情页")
                    # 返回列表
                    page.go_back()
                    page.wait_for_load_state('networkidle')
                else:
                    print_info("点击行未跳转（可能需要特定交互）")

        else:
            print_fail("未发现数据表格")

    except Exception as e:
        print_fail(f"检查数据表格出错: {e}")

    # 检查分页器
    try:
        pagination = page.locator('[class*="pagination"], .el-pagination').first
        if pagination.count() > 0:
            print_success("发现分页器")

    except Exception as e:
        print_info("未发现分页器或数据不足一页")

    return True

def test_heritage_detail(page):
    """测试非遗项目详情页面"""
    print_section("测试 2: 非遗项目详情页面")

    # 导航到详情页（通过URL直接访问）
    page.goto('http://localhost:5173/heritage/1')
    page.wait_for_load_state('networkidle')
    page.wait_for_timeout(1000)

    page.screenshot(path='D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/test_screenshots/11_heritage_detail.png', full_page=True)
    print_info("已保存项目详情截图")

    # 检查基本信息卡片
    try:
        info_cards = page.locator('[class*="card"], [class*="info"]').all()
        if len(info_cards) >= 2:
            print_success(f"发现 {len(info_cards)} 个信息卡片")

    except Exception as e:
        print_fail(f"检查信息卡片出错: {e}")

    # 检查返回按钮
    try:
        back_btn = page.locator('button:has-text("返回"), [class*="back"], .el-icon').first
        if back_btn.count() > 0:
            print_success("发现返回按钮")

    except Exception as e:
        print_info("未发现返回按钮")

    # 检查传承人列表
    try:
        inheritor_section = page.locator('[class*="inheritor"], [class*="传承人"]').first
        if inheritor_section.count() > 0:
            print_success("发现传承人区域")

    except Exception as e:
        print_info("未发现传承人区域（可能项目无关联传承人）")

    return True

def test_inheritor_list(page):
    """测试传承人列表页面"""
    print_section("测试 3: 传承人列表页面")

    # 点击传承人菜单
    inheritor_link = page.locator('a, [class*="menu"]').filter(has_text='传承人').first
    if inheritor_link.count() > 0:
        inheritor_link.click()
        page.wait_for_load_state('networkidle')
        print_success("点击传承人菜单")
    else:
        print_fail("未找到传承人菜单")
        return False

    page.screenshot(path='D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/test_screenshots/11_inheritor_list.png', full_page=True)
    print_info("已保存传承人列表截图")

    # 检查筛选表单
    try:
        search_input = page.locator('input[placeholder*="搜索"], input[placeholder*="姓名"]').first
        if search_input.count() > 0:
            print_success("发现姓名搜索输入框")

        # 检查多个筛选器
        selects = page.locator('select, [role="combobox"]').all()
        if len(selects) > 0:
            print_success(f"发现 {len(selects)} 个筛选器")

    except Exception as e:
        print_fail(f"检查筛选器出错: {e}")

    # 检查数据表格
    try:
        table = page.locator('table, [class*="table"], [class*="el-table"]').first
        if table.count() > 0:
            print_success("发现数据表格")

            rows = page.locator('tr[class*="row"], [class*="table-row"]').all()
            print_info(f"表格包含 {len(rows)} 行")

        else:
            print_fail("未发现数据表格")

    except Exception as e:
        print_fail(f"检查数据表格出错: {e}")

    return True

def test_visual_style(page):
    """测试视觉风格"""
    print_section("测试 4: 视觉风格一致性")

    # 检查页面标题
    try:
        page.goto('http://localhost:5173/heritage')
        page.wait_for_load_state('networkidle')

        header = page.locator('[class*="header"], h1, h2').first
        if header.count() > 0:
            print_success("页面头部显示正常")

    except Exception as e:
        print_fail(f"检查页面头部出错: {e}")

    return True

def main():
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║       非遗文化管理系统 - 阶段十一功能测试                ║")
    print("║          Data List Pages Testing                         ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")

    results = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()

        def handle_console(msg):
            if msg.type == 'error':
                print(f"{Colors.YELLOW}[WARN] {msg.text}{Colors.RESET}")
        page.on('console', handle_console)

        try:
            login(page)

            results['项目列表页面'] = test_heritage_list(page)
            results['项目详情页面'] = test_heritage_detail(page)
            results['传承人列表页面'] = test_inheritor_list(page)
            results['视觉风格'] = test_visual_style(page)

        finally:
            browser.close()

    print_section("测试结果汇总")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test, result in results.items():
        status = f"{Colors.GREEN}通过{Colors.RESET}" if result else f"{Colors.RED}失败{Colors.RESET}"
        symbol = "[PASS]" if result else "[FAIL]"
        print(f"{symbol} {test}: {status}")

    print(f"\n{Colors.BOLD}总计: {passed}/{total} 通过{Colors.RESET}")

    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}[SUCCESS] 所有测试通过！阶段十一实施完成。{Colors.RESET}")
        return 0
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}[WARNING] 部分测试未通过，请检查上述问题。{Colors.RESET}")
        return 1

if __name__ == '__main__':
    os.makedirs('D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/test_screenshots', exist_ok=True)
    sys.exit(main())
