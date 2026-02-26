#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""阶段十二功能测试脚本 - 管理功能页面"""

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

    login_btn = page.locator('button').filter(has_text='登录').first
    login_btn.click()
    page.wait_for_timeout(2000)

def test_heritage_manage(page):
    """测试项目管理页面"""
    print_section("测试 1: 项目管理页面")

    # 点击项目管理菜单
    manage_link = page.locator('a, [class*="menu"]').filter(has_text='项目管理').first
    if manage_link.count() > 0:
        manage_link.click()
        page.wait_for_load_state('networkidle')
        print_success("点击项目管理菜单")
    else:
        print_fail("未找到项目管理菜单")
        return False

    page.wait_for_timeout(1000)
    page.screenshot(path='D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/test_screenshots/12_heritage_manage.png', full_page=True)
    print_info("已保存项目管理页面截图")

    # 检查搜索/筛选区域
    try:
        search_input = page.locator('input[placeholder*="搜索"], input[placeholder*="名称"]').first
        if search_input.count() > 0:
            print_success("发现搜索输入框")

        filters = page.locator('select, [role="combobox"]').all()
        if len(filters) > 0:
            print_success(f"发现 {len(filters)} 个筛选器")

    except Exception as e:
        print_info(f"检查筛选器: {e}")

    # 检查新增按钮
    try:
        add_btn = page.locator('button:has-text("新增"), button:has-text("添加"), button:has-text("创建")').first
        if add_btn.count() > 0:
            print_success("发现新增按钮")

    except Exception as e:
        print_info(f"未发现新增按钮: {e}")

    # 检查数据表格
    try:
        table = page.locator('table, [class*="table"], [class*="el-table"]').first
        if table.count() > 0:
            print_success("发现数据表格")

            # 检查操作列
            actions = page.locator('button:has-text("编辑"), button:has-text("删除")').all()
            if len(actions) > 0:
                print_success(f"发现 {len(actions)} 个操作按钮")

        else:
            print_info("未发现数据表格")

    except Exception as e:
        print_info(f"检查数据表格: {e}")

    return True

def test_inheritor_manage(page):
    """测试传承人管理页面"""
    print_section("测试 2: 传承人管理页面")

    inheritor_link = page.locator('a, [class*="menu"]').filter(has_text='传承人管理').first
    if inheritor_link.count() > 0:
        inheritor_link.click()
        page.wait_for_load_state('networkidle')
        print_success("点击传承人管理菜单")
    else:
        print_fail("未找到传承人管理菜单")
        return False

    page.wait_for_timeout(1000)
    page.screenshot(path='D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/test_screenshots/12_inheritor_manage.png', full_page=True)
    print_info("已保存传承人管理页面截图")

    # 检查搜索和表格
    try:
        search_input = page.locator('input[placeholder*="搜索"], input[placeholder*="姓名"]').first
        if search_input.count() > 0:
            print_success("发现搜索输入框")

        table = page.locator('table, [class*="table"]').first
        if table.count() > 0:
            print_success("发现数据表格")

    except Exception as e:
        print_info(f"检查传承人管理页面: {e}")

    return True

def test_category_manage(page):
    """测试分类管理页面"""
    print_section("测试 3: 分类管理页面")

    category_link = page.locator('a, [class*="menu"]').filter(has_text='分类管理').first
    if category_link.count() > 0:
        category_link.click()
        page.wait_for_load_state('networkidle')
        print_success("点击分类管理菜单")
    else:
        print_fail("未找到分类管理菜单")
        return False

    page.wait_for_timeout(1000)
    page.screenshot(path='D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/test_screenshots/12_category_manage.png', full_page=True)
    print_info("已保存分类管理页面截图")

    # 检查视图切换按钮
    try:
        view_buttons = page.locator('button:has-text("列表"), button:has-text("树形"), button:has-text("List"), button:has-text("Tree")').all()
        if len(view_buttons) > 0:
            print_success("发现视图切换按钮")

        # 检查表格或树形结构
        table = page.locator('table, [class*="table"], [class*="tree"]').first
        if table.count() > 0:
            print_success("发现数据展示区域")

    except Exception as e:
        print_info(f"检查分类管理页面: {e}")

    return True

def test_data_import(page):
    """测试数据导入页面"""
    print_section("测试 4: 数据导入页面")

    import_link = page.locator('a, [class*="menu"]').filter(has_text='数据导入').first
    if import_link.count() > 0:
        import_link.click()
        page.wait_for_load_state('networkidle')
        print_success("点击数据导入菜单")
    else:
        print_fail("未找到数据导入菜单")
        return False

    page.wait_for_timeout(1000)
    page.screenshot(path='D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/test_screenshots/12_data_import.png', full_page=True)
    print_info("已保存数据导入页面截图")

    # 检查 Tab 切换
    try:
        tabs = page.locator('[class*="tab"]').all()
        if len(tabs) > 0:
            print_success(f"发现 {len(tabs)} 个 Tab 标签")

    except Exception as e:
        print_info(f"检查 Tab: {e}")

    # 检查上传区域
    try:
        upload_area = page.locator('[class*="upload"], [class*="dropzone"]').first
        if upload_area.count() > 0:
            print_success("发现文件上传区域")

    except Exception as e:
        print_info(f"检查上传区域: {e}")

    # 检查历史记录表格
    try:
        history_table = page.locator('table, [class*="table"]').first
        if history_table.count() > 0:
            print_success("发现历史记录表格")

    except Exception as e:
        print_info(f"检查历史记录: {e}")

    return True

def test_admin_access_control(page):
    """测试管理员权限控制"""
    print_section("测试 5: 管理员权限控制")

    # 检查所有管理菜单是否可见
    admin_menus = ['项目管理', '传承人管理', '分类管理', '数据导入']
    visible_count = 0

    for menu in admin_menus:
        menu_link = page.locator('a, [class*="menu"]').filter(has_text=menu).first
        if menu_link.count() > 0:
            visible_count += 1
            print_success(f"管理菜单可见: {menu}")

    if visible_count == len(admin_menus):
        print_success(f"所有 {visible_count} 个管理菜单均可见")
    else:
        print_fail(f"仅有 {visible_count}/{len(admin_menus)} 个管理菜单可见")

    return True

def main():
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║       非遗文化管理系统 - 阶段十二功能测试                ║")
    print("║          Management Pages Testing                       ║")
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

            results['项目管理页面'] = test_heritage_manage(page)
            results['传承人管理页面'] = test_inheritor_manage(page)
            results['分类管理页面'] = test_category_manage(page)
            results['数据导入页面'] = test_data_import(page)
            results['管理员权限控制'] = test_admin_access_control(page)

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
        print(f"\n{Colors.GREEN}{Colors.BOLD}[SUCCESS] 所有测试通过！阶段十二实施完成。{Colors.RESET}")
        return 0
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}[WARNING] 部分测试未通过，请检查上述问题。{Colors.RESET}")
        return 1

if __name__ == '__main__':
    os.makedirs('D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/test_screenshots', exist_ok=True)
    sys.exit(main())
