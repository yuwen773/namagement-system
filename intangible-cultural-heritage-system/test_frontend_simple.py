"""
简化的前端功能测试脚本
逐步验证每个功能
"""

from playwright.sync_api import sync_playwright
import json
import time

BASE_URL = "http://localhost:5173"

# 测试结果
test_results = []

def log_result(test_id, test_name, passed, message=""):
    """记录测试结果"""
    status = "[PASS]" if passed else "[FAIL]"
    result = {"id": test_id, "name": test_name, "passed": passed, "message": message}
    test_results.append(result)
    print(f"{status} {test_id}: {test_name}")
    if message:
        print(f"     {message}")

def take_screenshot(page, name):
    """截图保存"""
    timestamp = int(time.time() * 1000)
    path = f"test_screenshots/{name}_{timestamp}.png"
    page.screenshot(path=path, full_page=True)
    print(f"     Screenshot saved: {path}")
    return path

def run_tests():
    print("=" * 60)
    print("开始前端功能测试")
    print("=" * 60)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=500)
        page = browser.new_page()
        page.set_default_timeout(10000)

        try:
            # 测试1: 访问登录页面
            print("\n[测试 1] 访问登录页面")
            page.goto(BASE_URL)
            page.wait_for_load_state("networkidle")

            if page.url.endswith("/login") or "/login" in page.url:
                log_result("T1", "登录页面访问", True, f"URL: {page.url}")
            else:
                log_result("T1", "登录页面访问", False, f"URL: {page.url}")
                take_screenshot(page, "login_page")

            # 截图
            take_screenshot(page, "login_page_loaded")

            # 测试2: 检查登录表单元素
            print("\n[测试 2] 检查登录表单")
            input_count = page.locator("input").count()
            button_count = page.locator("button").count()
            log_result("T2", "登录表单元素", input_count >= 2, f"发现 {input_count} 个输入框, {button_count} 个按钮")

            # 测试3: 尝试登录
            print("\n[测试 3] 尝试登录")
            try:
                # 填写表单
                page.locator("input").first.fill("admin")
                page.locator("input").nth(1).fill("password123")

                # 点击登录按钮
                page.locator("button:has-text('登录')").click()

                # 等待跳转
                page.wait_for_url("**/dashboard", timeout=8000)
                log_result("T3", "登录成功", True, "跳转到驾驶舱")

                # 检查 token
                token = page.evaluate("() => localStorage.getItem('access_token')")
                if token:
                    log_result("T3-1", "Token存储", True, "Token 已存储")
                else:
                    log_result("T3-1", "Token存储", False, "Token 未找到")

                take_screenshot(page, "after_login")

            except Exception as e:
                log_result("T3", "登录成功", False, str(e))
                take_screenshot(page, "login_failed")

            # 测试4: 检查驾驶舱
            if "/dashboard" in page.url:
                print("\n[测试 4] 检查驾驶舱")
                try:
                    # 检查页面标题
                    title = page.title()
                    log_result("T4", "驾驶舱加载", True, f"标题: {title}")

                    # 检查菜单
                    menu_items = page.locator(".el-menu-item").count()
                    log_result("T4-1", "侧边栏菜单", menu_items >= 3, f"发现 {menu_items} 个菜单项")

                    take_screenshot(page, "dashboard_loaded")

                except Exception as e:
                    log_result("T4", "驾驶舱加载", False, str(e))

            # 测试5: 点击退出按钮
            try:
                print("\n[测试 5] 测试登出")
                page.click(".logout-btn")
                page.wait_for_timeout(1000)

                # 处理确认对话框
                confirm_btn = page.locator(".el-button--primary:has-text('确定')")
                if confirm_btn.count() > 0:
                    confirm_btn.click()
                    page.wait_for_url("**/login", timeout=3000)
                    log_result("T5", "登出功能", True, "成功退出")
                else:
                    log_result("T5", "登出功能", False, "未找到确认对话框")

            except Exception as e:
                log_result("T5", "登出功能", False, str(e))

            # 测试6: 测试路由守卫
            try:
                print("\n[测试 6] 测试路由守卫")
                page.evaluate("() => localStorage.clear()")
                page.goto(f"{BASE_URL}/dashboard")
                page.wait_for_load_state("networkidle")

                if "/login" in page.url:
                    log_result("T6", "路由守卫", True, "未登录被重定向到登录页")
                else:
                    log_result("T6", "路由守卫", False, f"仍在: {page.url}")

            except Exception as e:
                log_result("T6", "路由守卫", False, str(e))

            # 测试7: 测试项目列表
            try:
                print("\n[测试 7] 测试项目列表")
                # 先登录
                page.goto(f"{BASE_URL}/login")
                page.wait_for_load_state("networkidle")
                page.locator("input").first.fill("admin")
                page.locator("input").nth(1).fill("password123")
                page.locator("button:has-text('登录')").click()
                page.wait_for_url("**/dashboard", timeout=5000)

                # 访问项目列表
                page.goto(f"{BASE_URL}/heritage")
                page.wait_for_load_state("networkidle")

                tables = page.locator("table, .el-table").count()
                log_result("T7", "项目列表", tables > 0, f"发现 {tables} 个表格")

                take_screenshot(page, "heritage_list")

            except Exception as e:
                log_result("T7", "项目列表", False, str(e))

        except Exception as e:
            print(f"\n测试执行出错: {e}")
        finally:
            browser.close()

    # 打印结果
    print("\n" + "=" * 60)
    print("测试结果摘要")
    print("=" * 60)

    passed = sum(1 for r in test_results if r["passed"])
    failed = sum(1 for r in test_results if not r["passed"])
    total = len(test_results)

    print(f"总计: {total} | 通过: {passed} | 失败: {failed}")

    if failed > 0:
        print("\n失败的测试:")
        for r in test_results:
            if not r["passed"]:
                print(f"  - {r['id']}: {r['name']}")
                if r['message']:
                    print(f"    {r['message']}")

    # 保存结果
    with open("test_results.json", "w", encoding="utf-8") as f:
        json.dump({
            "summary": {"total": total, "passed": passed, "failed": failed},
            "results": test_results
        }, f, ensure_ascii=False, indent=2)

    print(f"\n结果已保存到: test_results.json")

    return failed == 0

if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
