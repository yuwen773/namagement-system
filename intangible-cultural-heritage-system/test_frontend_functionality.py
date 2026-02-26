"""
前端功能自动化测试脚本
测试范围：docs/test/frontend-test-plan.md
"""

from playwright.sync_api import sync_playwright, expect
import json
import time
import sys

# 测试配置
BASE_URL = "http://localhost:5173"
API_URL = "http://localhost:8000/api/v1"

# 测试账号
TEST_USERS = {
    "admin": {"username": "admin", "password": "password123"},
    "user": {"username": "user", "password": "password123"}
}

# 测试结果记录
test_results = []


def log_result(test_id, test_name, passed, message=""):
    """记录测试结果"""
    status = "[PASS]" if passed else "[FAIL]"
    result = {
        "id": test_id,
        "name": test_name,
        "passed": passed,
        "message": message
    }
    test_results.append(result)
    print(f"{status} | {test_id}: {test_name}")
    if message:
        print(f"    -> {message}")


def take_screenshot(page, name):
    """截图保存"""
    timestamp = int(time.time() * 1000)
    path = f"test_screenshots/{name}_{timestamp}.png"
    page.screenshot(path=path, full_page=True)
    return path


def login_user(page, username, password):
    """辅助函数：用户登录"""
    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")

    # 使用更精确的选择器定位 el-input 输入框
    page.locator(".el-input__inner").first.fill(username)
    page.locator(".el-input__inner").nth(1).fill(password)
    page.click("button:has-text('登录')")

    try:
        page.wait_for_url("**/dashboard", timeout=5000)
        return True
    except:
        return False


def test_login_logout(page):
    """测试登录/登出流程"""
    print("\n=== 测试登录/登出流程 ===")

    # TC-001: 正常登录
    success = login_user(page, TEST_USERS["admin"]["username"], TEST_USERS["admin"]["password"])

    if success:
        log_result("TC-001", "正常登录", True, "登录成功，跳转到驾驶舱")

        # 检查 localStorage 中有 token
        token = page.evaluate("() => localStorage.getItem('access_token')")
        if token:
            log_result("TC-001-1", "Token存储验证", True, "access_token 已存储")
        else:
            log_result("TC-001-1", "Token存储验证", False, "access_token 未找到")
    else:
        log_result("TC-001", "正常登录", False, "登录失败")
        take_screenshot(page, "login_failed")
        return False

    # TC-004: 登出
    try:
        # 点击退出按钮
        page.click(".logout-btn")

        # 等待确认对话框并点击确定
        page.wait_for_selector(".el-message-box", timeout=2000)
        page.click(".el-button--primary:has-text('确定')")

        # 等待跳转到登录页
        page.wait_for_url("**/login", timeout=3000)
        log_result("TC-004", "登出功能", True, "登出成功，跳转到登录页")
    except Exception as e:
        log_result("TC-004", "登出功能", False, str(e))

    return True


def test_login_form_validation(page):
    """测试登录表单验证"""
    print("\n=== 测试登录表单验证 ===")

    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")

    # TC-003: 表单验证 - 直接点击登录
    try:
        page.click("button:has-text('登录')")
        page.wait_for_timeout(500)

        # 检查是否显示验证错误信息
        error_text = page.locator(".el-form-item__error").count()
        if error_text > 0:
            log_result("TC-003", "表单验证", True, f"检测到 {error_text} 条验证提示")
        else:
            log_result("TC-003", "表单验证", False, "未显示验证提示")
    except Exception as e:
        log_result("TC-003", "表单验证", False, str(e))


def test_login_failure(page):
    """测试登录失败"""
    print("\n=== 测试登录失败 ===")

    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")

    # TC-002: 登录失败
    try:
        page.locator(".el-input__inner").first.fill("wronguser")
        page.locator(".el-input__inner").nth(1).fill("wrongpass")
        page.click("button:has-text('登录')")

        page.wait_for_timeout(2000)

        current_url = page.url
        if "/login" in current_url:
            log_result("TC-002", "登录失败", True, "仍在登录页，未跳转")
        else:
            log_result("TC-002", "登录失败", False, f"意外跳转到: {current_url}")
    except Exception as e:
        log_result("TC-002", "登录失败", False, str(e))


def test_route_guards(page):
    """测试路由守卫"""
    print("\n=== 测试路由守卫 ===")

    # 清除登录状态
    page.evaluate("() => localStorage.clear()")

    # TC-005: 未登录访问受保护页面
    page.goto(f"{BASE_URL}/dashboard")
    page.wait_for_load_state("networkidle")

    current_url = page.url
    if "/login" in current_url:
        log_result("TC-005", "未登录重定向", True, "自动跳转到登录页")
    else:
        log_result("TC-005", "未登录重定向", False, f"当前URL: {current_url}")
        take_screenshot(page, "route_guard_failed")

    # TC-006: 已登录用户访问登录页
    login_user(page, TEST_USERS["admin"]["username"], TEST_USERS["admin"]["password"])
    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")

    current_url = page.url
    if "/dashboard" in current_url:
        log_result("TC-006", "已登录重定向", True, "自动重定向到驾驶舱")
    else:
        log_result("TC-006", "已登录重定向", False, f"仍在登录页: {current_url}")


def test_dashboard(page):
    """测试驾驶舱页面"""
    print("\n=== 测试驾驶舱页面 ===")

    login_user(page, TEST_USERS["admin"]["username"], TEST_USERS["admin"]["password"])
    page.wait_for_load_state("networkidle")

    # TC-008: 驾驶舱初始加载
    try:
        # 检查统计卡片
        stat_cards = page.locator(".stat-card, [class*='StatCard']").count()
        if stat_cards >= 4:
            log_result("TC-008", "驾驶舱初始加载", True, f"发现 {stat_cards} 个统计卡片")
        else:
            log_result("TC-008", "驾驶舱初始加载", False, f"只发现 {stat_cards} 个统计卡片")

        take_screenshot(page, "dashboard_loaded")
    except Exception as e:
        log_result("TC-008", "驾驶舱初始加载", False, str(e))

    # TC-009: ECharts 图表组件
    try:
        # 检查是否有 ECharts 图表容器
        charts = page.locator("canvas").count()
        if charts > 0:
            log_result("TC-009", "图表组件渲染", True, f"发现 {charts} 个 ECharts canvas")
        else:
            log_result("TC-009", "图表组件渲染", False, "未发现图表组件")
    except Exception as e:
        log_result("TC-009", "图表组件渲染", False, str(e))

    # TC-010: 侧边栏菜单
    try:
        menu_items = page.locator(".el-menu-item").count()
        if menu_items >= 3:
            log_result("TC-010", "侧边栏菜单", True, f"发现 {menu_items} 个菜单项")
        else:
            log_result("TC-010", "侧边栏菜单", False, f"只发现 {menu_items} 个菜单项")
    except Exception as e:
        log_result("TC-010", "侧边栏菜单", False, str(e))


def test_heritage_list(page):
    """测试项目列表页面"""
    print("\n=== 测试项目列表页面 ===")

    # TC-013: 项目列表初始加载
    try:
        page.goto(f"{BASE_URL}/heritage")
        page.wait_for_load_state("networkidle")

        # 检查表格
        tables = page.locator("table, .el-table").count()
        if tables > 0:
            log_result("TC-013", "项目列表加载", True, "表格正常显示")
        else:
            log_result("TC-013", "项目列表加载", False, "未发现表格")

        take_screenshot(page, "heritage_list")
    except Exception as e:
        log_result("TC-013", "项目列表加载", False, str(e))


def test_admin_pages(page):
    """测试管理页面"""
    print("\n=== 测试管理页面 ===")

    # TC-020: 项目管理页面
    try:
        page.goto(f"{BASE_URL}/admin/heritage")
        page.wait_for_load_state("networkidle")

        # 检查是否成功加载管理页面
        current_url = page.url
        if "/admin/heritage" in current_url:
            log_result("TC-020", "项目管理页面访问", True, "管理页面正常加载")

            # 检查新增按钮
            add_buttons = page.locator("button:has-text('新增'), button:has-text('添加')").count()
            if add_buttons > 0:
                log_result("TC-020-1", "新增按钮存在", True)
            else:
                log_result("TC-020-1", "新增按钮存在", False)

            take_screenshot(page, "admin_heritage")
        else:
            log_result("TC-020", "项目管理页面访问", False, f"被重定向到: {current_url}")
    except Exception as e:
        log_result("TC-020", "项目管理页面访问", False, str(e))


def test_permission_control(page):
    """测试权限控制"""
    print("\n=== 测试权限控制 ===")

    # 先登出
    page.evaluate("() => localStorage.clear()")

    # TC-007: 普通用户访问管理页面
    try:
        login_user(page, TEST_USERS["user"]["username"], TEST_USERS["user"]["password"])

        # 尝试访问管理页面
        page.goto(f"{BASE_URL}/admin/heritage")
        page.wait_for_load_state("networkidle")

        current_url = page.url
        # 普通用户应该被重定向回 dashboard
        if "/dashboard" in current_url:
            log_result("TC-007", "普通用户权限控制", True, "普通用户被拒绝访问管理页面")
        else:
            log_result("TC-007", "普通用户权限控制", False, f"普通用户能访问管理页面: {current_url}")

        take_screenshot(page, "user_permission_test")
    except Exception as e:
        log_result("TC-007", "普通用户权限控制", False, str(e))


def test_inheritor_list(page):
    """测试传承人列表页面"""
    print("\n=== 测试传承人列表页面 ===")

    login_user(page, TEST_USERS["admin"]["username"], TEST_USERS["admin"]["password"])

    # TC-018: 传承人列表加载
    try:
        page.goto(f"{BASE_URL}/inheritors")
        page.wait_for_load_state("networkidle")

        tables = page.locator("table, .el-table").count()
        if tables > 0:
            log_result("TC-018", "传承人列表加载", True, "表格正常显示")
        else:
            log_result("TC-018", "传承人列表加载", False, "未发现表格")

        take_screenshot(page, "inheritor_list")
    except Exception as e:
        log_result("TC-018", "传承人列表加载", False, str(e))


def run_all_tests():
    """运行所有测试"""
    print("=" * 60)
    print("开始执行前端功能自动化测试")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 设置默认超时
        page.set_default_timeout(5000)

        try:
            # 执行测试套件
            test_login_logout(page)
            test_login_form_validation(page)
            test_login_failure(page)
            test_route_guards(page)
            test_dashboard(page)
            test_heritage_list(page)
            test_inheritor_list(page)
            test_admin_pages(page)
            test_permission_control(page)

        except Exception as e:
            print(f"\n测试执行出错: {e}")
        finally:
            browser.close()

    # 打印测试结果摘要
    print("\n" + "=" * 60)
    print("测试结果摘要")
    print("=" * 60)

    passed = sum(1 for r in test_results if r["passed"])
    failed = sum(1 for r in test_results if not r["passed"])
    total = len(test_results)

    print(f"\n总计: {total} | 通过: {passed} | 失败: {failed}")

    if failed > 0:
        print("\n失败的测试:")
        for r in test_results:
            if not r["passed"]:
                print(f"  - {r['id']}: {r['name']}")
                if r['message']:
                    print(f"    {r['message']}")

    # 保存测试结果到 JSON
    with open("test_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "summary": {"total": total, "passed": passed, "failed": failed},
            "results": test_results
        }, f, ensure_ascii=False, indent=2)

    print(f"\n测试结果已保存到: test_results.json")
    print("截图已保存到: test_screenshots/")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    exit(0 if success else 1)
