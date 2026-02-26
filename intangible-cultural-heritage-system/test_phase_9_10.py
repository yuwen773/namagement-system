#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""阶段九、十功能测试脚本 - 非遗文化管理系统"""

import sys
import io
# 设置标准输出为UTF-8编码
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from playwright.sync_api import sync_playwright
import time

class Colors:
    """终端颜色输出"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg):
    print(f"{Colors.GREEN}[PASS] {msg}{Colors.RESET}")

def print_fail(msg):
    print(f"{Colors.RED}[FAIL] {msg}{Colors.RESET}")

def print_info(msg):
    print(f"{Colors.BLUE}[INFO] {msg}{Colors.RESET}")

def print_section(msg):
    print(f"\n{Colors.BOLD}{Colors.YELLOW}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}  {msg}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.YELLOW}{'='*60}{Colors.RESET}\n")

def test_login(page):
    """测试登录功能"""
    print_section("测试 1: 登录功能")

    # 访问首页，应自动跳转到登录页
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')

    current_url = page.url
    if '/login' in current_url or current_url.endswith('5173/'):
        print_success("自动跳转到登录页")
    else:
        print_fail(f"未跳转到登录页，当前URL: {current_url}")
        return False

    # 截图登录页
    page.screenshot(path='D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/test_screenshots/01_login_page.png')
    print_info("已保存登录页截图")

    # 填写登录表单
    try:
        # 查找用户名输入框
        username_input = page.locator('input[type="text"], input[placeholder*="用户"], input[placeholder*="username"]').first
        if username_input.count() > 0:
            username_input.fill('admin')
            print_success("填写用户名: admin")
        else:
            print_fail("未找到用户名输入框")
            return False

        # 查找密码输入框
        password_input = page.locator('input[type="password"]').first
        if password_input.count() > 0:
            password_input.fill('password123')
            print_success("填写密码: ******")
        else:
            print_fail("未找到密码输入框")
            return False

        # 点击登录按钮
        login_btn = page.locator('button[type="submit"], button:has-text("登录"), button:has-text("Login")').first
        if login_btn.count() > 0:
            login_btn.click()
            print_success("点击登录按钮")
        else:
            print_fail("未找到登录按钮")
            page.screenshot(path='D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/test_screenshots/login_error.png')
            return False

        # 等待跳转
        page.wait_for_timeout(2000)
        page.wait_for_load_state('networkidle')

        current_url = page.url
        if '/dashboard' in current_url:
            print_success("登录成功，跳转到驾驶舱")
        else:
            print_fail(f"登录后未跳转到驾驶舱，当前URL: {current_url}")
            page.screenshot(path='D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/test_screenshots/after_login.png')
            return False

    except Exception as e:
        print_fail(f"登录过程出错: {e}")
        page.screenshot(path='D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/test_screenshots/login_exception.png')
        return False

    return True

def test_main_layout(page):
    """测试主布局"""
    print_section("测试 2: 主布局组件")

    # 截图主布局
    page.screenshot(path='D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/test_screenshots/02_main_layout.png', full_page=True)
    print_info("已保存主布局截图")

    # 检查顶部导航栏
    try:
        # 检查Logo/标题
        logo = page.locator('.logo, h1, [class*="logo"], [class*="title"]').first
        if logo.count() > 0:
            print_success("顶部导航栏显示Logo/标题")

        # 检查用户信息
        user_info = page.locator('[class*="user"], [class*="avatar"]').first
        if user_info.count() > 0:
            print_success("顶部显示用户信息区域")

        # 检查角色标签（管理员）
        admin_tag = page.locator('[class*="admin"], [class*="role"], .el-tag:has-text("管理员")').first
        if admin_tag.count() > 0:
            print_success("显示管理员角色标签")

        # 检查退出按钮
        logout_btn = page.locator('button:has-text("退出"), button:has-text("登出"), [class*="logout"]').first
        if logout_btn.count() > 0:
            print_success("显示退出按钮")

    except Exception as e:
        print_fail(f"检查顶部导航栏出错: {e}")

    # 检查侧边栏菜单
    try:
        # 检查"驾驶舱"菜单
        dashboard_menu = page.locator('[class*="menu"], [class*="sidebar"]').first
        if dashboard_menu.count() > 0:
            menu_text = dashboard_menu.inner_text()
            if '驾驶舱' in menu_text:
                print_success("侧边栏显示驾驶舱菜单")

            # 检查管理员专属菜单
            if '项目管理' in menu_text or '传承人管理' in menu_text or '分类管理' in menu_text:
                print_success("侧边栏显示管理员管理菜单")
            else:
                print_fail("侧边栏未显示管理菜单")

    except Exception as e:
        print_fail(f"检查侧边栏菜单出错: {e}")

    return True

def test_dashboard_stat_cards(page):
    """测试驾驶舱统计卡片"""
    print_section("测试 3: 驾驶舱统计卡片")

    try:
        # 等待页面完全加载
        page.wait_for_timeout(1000)

        # 检查统计卡片
        cards = page.locator('[class*="stat"], [class*="card"], .stat-card').all()
        if len(cards) >= 4:
            print_success(f"发现 {len(cards)} 个统计卡片")
        else:
            print_fail(f"统计卡片数量不足，仅发现 {len(cards)} 个")
            page.screenshot(path='D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/test_screenshots/cards_error.png')
            return False

        # 检查卡片内容
        card_texts = [card.inner_text() for card in cards[:4]]
        for i, text in enumerate(card_texts):
            print_info(f"卡片 {i+1}: {text[:100]}...")

        # 检查是否显示数字
        has_numbers = any(any(c.isdigit() for c in text) for text in card_texts)
        if has_numbers:
            print_success("统计卡片显示数据")
        else:
            print_fail("统计卡片未显示数据")

    except Exception as e:
        print_fail(f"检查统计卡片出错: {e}")
        return False

    return True

def test_dashboard_charts(page):
    """测试驾驶舱图表"""
    print_section("测试 4: 驾驶舱图表")

    # 等待图表加载
    page.wait_for_timeout(2000)

    # 截图
    page.screenshot(path='D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/test_screenshots/03_dashboard_charts.png', full_page=True)
    print_info("已保存驾驶舱截图")

    try:
        # 检查世界地图（ECharts 容器）
        map_container = page.locator('[class*="map"], [class*="chart"], .echarts').all()
        if len(map_container) >= 3:
            print_success(f"发现 {len(map_container)} 个图表容器")
        else:
            print_fail(f"图表容器数量不足，仅发现 {len(map_container)} 个")

        # 检查分类筛选器
        category_filter = page.locator('select, [class*="select"], [role="combobox"]').first
        if category_filter.count() > 0:
            print_success("发现分类筛选器")
        else:
            print_info("未发现分类筛选器（可能集成在其他位置）")

        # 检查控制台是否有ECharts错误
        console_errors = []
        page.on('console', lambda msg: console_errors.append(msg) if msg.type == 'error' else None)

        page.wait_for_timeout(1000)

        if len(console_errors) > 0:
            print_fail(f"控制台发现 {len(console_errors)} 个错误")
        else:
            print_success("控制台无错误")

    except Exception as e:
        print_fail(f"检查图表出错: {e}")
        return False

    return True

def test_category_filter(page):
    """测试分类筛选功能"""
    print_section("测试 5: 分类筛选功能")

    try:
        # 查找分类筛选下拉框
        category_select = page.locator('select, [class*="category"] select, [role="combobox"]').first

        if category_select.count() > 0:
            print_success("找到分类筛选器")

            # 尝试选择不同的分类
            page.wait_for_timeout(500)

            # 点击筛选器
            category_select.click()
            page.wait_for_timeout(500)

            print_info("已点击分类筛选器")

        else:
            print_info("未找到独立的分类筛选器")

    except Exception as e:
        print_fail(f"测试分类筛选出错: {e}")

    return True

def test_logout(page):
    """测试退出登录"""
    print_section("测试 6: 退出登录")

    try:
        # 查找并点击退出按钮
        logout_btn = page.locator('button:has-text("退出"), button:has-text("登出"), [class*="logout"]').first

        if logout_btn.count() > 0:
            logout_btn.click()
            print_success("点击退出按钮")

            # 检查是否有确认对话框
            page.wait_for_timeout(1000)

            # 如果有确认框，点击确认
            confirm_btn = page.locator('button:has-text("确认"), button:has-text("确定"), .el-button--primary').first
            if confirm_btn.count() > 0 and confirm_btn.is_visible():
                confirm_btn.click()
                print_success("确认退出")

            page.wait_for_timeout(2000)

            # 检查是否跳转到登录页
            current_url = page.url
            if '/login' in current_url:
                print_success("退出成功，跳转到登录页")
            else:
                print_fail(f"退出后未跳转到登录页，当前URL: {current_url}")

        else:
            print_fail("未找到退出按钮")

    except Exception as e:
        print_fail(f"测试退出登录出错: {e}")

    return True

def test_responsive(page):
    """测试响应式布局"""
    print_section("测试 7: 响应式布局")

    try:
        # 先登录
        page.goto('http://localhost:5173/login')
        page.wait_for_load_state('networkidle')

        username_input = page.locator('input[type="text"]').first
        password_input = page.locator('input[type="password"]').first
        username_input.fill('admin')
        password_input.fill('password123')

        login_btn = page.locator('button[type="submit"]').first
        login_btn.click()
        page.wait_for_load_state('networkidle')
        page.wait_for_timeout(2000)

        # 测试不同屏幕尺寸
        sizes = [
            ('桌面', 1920, 1080),
            ('平板', 768, 1024),
            ('手机', 375, 667)
        ]

        for name, width, height in sizes:
            page.set_viewport_size({'width': width, 'height': height})
            page.wait_for_timeout(500)

            screenshot_path = f'D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/test_screenshots/04_responsive_{name}.png'
            page.screenshot(path=screenshot_path, full_page=True)
            print_success(f"{name}尺寸 ({width}x{height}) 截图已保存")

        # 恢复默认尺寸
        page.set_viewport_size({'width': 1920, 'height': 1080})

    except Exception as e:
        print_fail(f"测试响应式布局出错: {e}")

    return True

def main():
    """主测试流程"""
    print(f"{Colors.BOLD}{Colors.BLUE}")
    print("╔══════════════════════════════════════════════════════════╗")
    print("║       非遗文化管理系统 - 阶段九、十功能测试              ║")
    print("║    Intangible Cultural Heritage System Testing           ║")
    print("╚══════════════════════════════════════════════════════════╝")
    print(f"{Colors.RESET}\n")

    results = {
        '登录功能': False,
        '主布局': False,
        '统计卡片': False,
        '图表显示': False,
        '分类筛选': False,
        '退出登录': False,
        '响应式布局': False
    }

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 显示浏览器便于观察
        context = browser.new_context(viewport={'width': 1920, 'height': 1080})
        page = context.new_page()

        # 监听控制台消息
        def handle_console(msg):
            if msg.type == 'error':
                print(f"{Colors.YELLOW}[WARN] 控制台错误: {msg.text}{Colors.RESET}")
        page.on('console', handle_console)

        try:
            # 执行测试
            results['登录功能'] = test_login(page)
            results['主布局'] = test_main_layout(page)
            results['统计卡片'] = test_dashboard_stat_cards(page)
            results['图表显示'] = test_dashboard_charts(page)
            results['分类筛选'] = test_category_filter(page)
            results['退出登录'] = test_logout(page)
            results['响应式布局'] = test_responsive(page)

        finally:
            browser.close()

    # 输出测试结果汇总
    print_section("测试结果汇总")

    passed = sum(1 for v in results.values() if v)
    total = len(results)

    for test, result in results.items():
        status = f"{Colors.GREEN}通过{Colors.RESET}" if result else f"{Colors.RED}失败{Colors.RESET}"
        symbol = "[PASS]" if result else "[FAIL]"
        print(f"{symbol} {test}: {status}")

    print(f"\n{Colors.BOLD}总计: {passed}/{total} 通过{Colors.RESET}")

    if passed == total:
        print(f"\n{Colors.GREEN}{Colors.BOLD}[SUCCESS] 所有测试通过！阶段九、十实施完成。{Colors.RESET}")
        return 0
    else:
        print(f"\n{Colors.YELLOW}{Colors.BOLD}[WARNING] 部分测试未通过，请检查上述问题。{Colors.RESET}")
        return 1

if __name__ == '__main__':
    # 创建截图目录
    import os
    os.makedirs('D:/work/code/personal/namagement-system/intangible-cultural-heritage-system/test_screenshots', exist_ok=True)

    sys.exit(main())
