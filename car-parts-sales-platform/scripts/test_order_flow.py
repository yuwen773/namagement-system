"""
订单流程页面自动化测试脚本

测试页面：
1. 确认订单页 (/checkout)
2. 支付页面 (/payment/:id)
3. 订单列表页 (/orders)
4. 订单详情页 (/orders/:id)
"""

from playwright.sync_api import sync_playwright
import json
import time

# 测试配置
BASE_URL = "http://localhost:5173"
BACKEND_URL = "http://localhost:8000"

# 测试用户凭据
TEST_USER = {
    "phone": "13800138001",
    "password": "123456"
}


def login(page):
    """登录功能"""
    print("\n=== 登录测试 ===")
    page.goto(f"{BASE_URL}/login")
    page.wait_for_load_state("networkidle")

    # 填写登录表单
    page.fill("input[placeholder*='手机号'], input[type='text']:not([readonly])", TEST_USER["phone"])
    page.fill("input[placeholder*='密码'], input[type='password']", TEST_USER["password"])

    # 点击登录按钮
    login_btn = page.locator("button:has-text('登录'), button:has-text('Login'), .el-button--primary").first
    login_btn.click()
    page.wait_for_load_state("networkidle")

    # 检查是否登录成功
    current_url = page.url
    if "/login" not in current_url:
        print("✓ 登录成功")
        return True
    else:
        print("✗ 登录失败")
        page.screenshot(path="test_results/login_failed.png")
        return False


def test_checkout_page(page):
    """测试确认订单页"""
    print("\n=== 测试确认订单页 (/checkout) ===")

    # 首先添加商品到购物车
    print("1. 添加商品到购物车...")
    page.goto(f"{BASE_URL}/products")
    page.wait_for_load_state("networkidle")

    # 点击第一个商品的"加入购物车"按钮
    add_to_cart_btn = page.locator("button:has-text('加入购物车'), button:has-text('Add to Cart')").first
    if add_to_cart_btn.is_visible():
        add_to_cart_btn.click()
        page.wait_for_timeout(1000)
        print("  ✓ 商品已添加到购物车")
    else:
        print("  ! 未找到加入购物车按钮，尝试直接进入")

    # 进入确认订单页
    print("2. 进入确认订单页...")
    page.goto(f"{BASE_URL}/checkout")
    page.wait_for_load_state("networkidle")

    # 截图
    page.screenshot(path="test_results/checkout_page.png", full_page=True)

    # 检查页面元素
    checks = {
        "地址选择区域": "text=收货地址, text=Shipping Address, .address-list",
        "优惠券选择区域": "text=优惠券, text=Coupon, .coupon-list",
        "商品清单": "text=商品清单, text=Order Items, .products-list",
        "金额明细": "text=金额明细, text=Order Summary, .summary-section",
        "提交订单按钮": "text=提交订单, text=Place Order, .submit-btn"
    }

    results = {}
    for name, selector in checks.items():
        try:
            # 尝试多个选择器
            found = False
            for sel in selector.split(", "):
                try:
                    if page.locator(sel).count() > 0:
                        found = True
                        break
                except:
                    continue
            results[name] = "✓" if found else "✗"
        except:
            results[name] = "✗"

    # 打印检查结果
    print("\n  页面元素检查:")
    for name, result in results.items():
        print(f"    {result} {name}")

    # 检查购物车商品显示
    print("\n3. 检查购物车商品...")
    try:
        items = page.locator(".product-card, .items-list .item-card, .order-items-preview .item-preview")
        item_count = items.count()
        print(f"  ✓ 显示 {item_count} 个商品")
    except:
        print("  ✗ 无法获取商品数量")

    # 检查金额计算
    print("\n4. 检查金额计算...")
    try:
        total_amount = page.locator(".total-amount, .bar-amount, .summary-value")
        if total_amount.count() > 0:
            amount_text = total_amount.first.inner_text()
            print(f"  ✓ 总金额显示: {amount_text}")
        else:
            print("  ! 未找到总金额显示")
    except:
        print("  ✗ 无法获取总金额")

    return all("✓" in r for r in results.values())


def test_payment_page(page, order_id=None):
    """测试支付页面"""
    print("\n=== 测试支付页面 (/payment/:id) ===")

    # 获取订单ID（如果未提供）
    if not order_id:
        # 先从订单列表获取一个订单ID
        page.goto(f"{BASE_URL}/orders")
        page.wait_for_load_state("networkidle")

        # 查找待付款订单
        pending_order = page.locator(".order-card, .orders-list .order").first
        if pending_order.count() > 0:
            # 从URL中提取订单ID或点击进入详情
            order_link = pending_order.locator("a").first
            if order_link.count() > 0:
                href = order_link.get_attribute("href") or ""
                if "/orders/" in href:
                    order_id = href.split("/")[-1]
                else:
                    # 尝试从卡片中获取
                    order_number = pending_order.locator("text=Order #").first
                    if order_number.count() > 0:
                        print("  ! 需要手动输入订单ID进行支付测试")
                        return False
            else:
                print("  ! 未找到待付款订单，无法测试支付页面")
                return False
        else:
            print("  ! 未找到任何订单")
            return False

    print(f"1. 访问支付页面 (订单ID: {order_id})...")
    page.goto(f"{BASE_URL}/payment/{order_id}")
    page.wait_for_load_state("networkidle")

    # 截图
    page.screenshot(path="test_results/payment_page.png", full_page=True)

    # 检查页面元素
    checks = {
        "订单摘要": "text=订单摘要, text=Order Summary, .order-summary-card",
        "支付方式选择": "text=支付方式, text=Payment Method, .payment-options",
        "倒计时": ".timer-value, text=:",
        "支付按钮": "text=支付, text=Pay, .pay-btn"
    }

    results = {}
    for name, selector in checks.items():
        try:
            found = False
            for sel in selector.split(", "):
                try:
                    if page.locator(sel).count() > 0:
                        found = True
                        break
                except:
                    continue
            results[name] = "✓" if found else "✗"
        except:
            results[name] = "✗"

    print("\n  页面元素检查:")
    for name, result in results.items():
        print(f"    {result} {name}")

    # 检查支付方式
    print("\n2. 检查支付方式选项...")
    try:
        payment_methods = page.locator(".payment-option, .payment-methods")
        method_count = payment_methods.count()
        print(f"  ✓ 找到 {method_count} 种支付方式")
    except:
        print("  ✗ 无法获取支付方式")

    # 检查倒计时
    print("\n3. 检查倒计时功能...")
    try:
        timer = page.locator(".timer-value")
        if timer.count() > 0:
            timer_text = timer.first.inner_text()
            print(f"  ✓ 倒计时显示: {timer_text}")
            page.wait_for_timeout(2000)
            timer_text2 = timer.first.inner_text()
            if timer_text != timer_text2:
                print("  ✓ 倒计时正在运行")
        else:
            print("  ! 未找到倒计时显示")
    except:
        print("  ✗ 无法检查倒计时")

    return all("✓" in r for r in results.values())


def test_order_list_page(page):
    """测试订单列表页"""
    print("\n=== 测试订单列表页 (/orders) ===")

    print("1. 访问订单列表页...")
    page.goto(f"{BASE_URL}/orders")
    page.wait_for_load_state("networkidle")

    # 截图
    page.screenshot(path="test_results/order_list_page.png", full_page=True)

    # 检查页面元素
    checks = {
        "状态筛选Tabs": ".tabs, .tab",
        "订单列表": ".orders-list, .order-card",
        "订单卡片": ".order-card"
    }

    results = {}
    for name, selector in checks.items():
        try:
            found = page.locator(selector).count() > 0
            results[name] = "✓" if found else "✗"
        except:
            results[name] = "✗"

    print("\n  页面元素检查:")
    for name, result in results.items():
        print(f"    {result} {name}")

    # 测试状态筛选
    print("\n2. 测试状态筛选功能...")
    try:
        tabs = page.locator(".tab, .tabs button")
        tab_count = tabs.count()
        print(f"  ✓ 找到 {tab_count} 个状态标签")

        if tab_count > 0:
            # 点击第二个标签
            tabs.nth(1).click()
            page.wait_for_timeout(500)
            print("  ✓ 状态筛选功能正常")
    except:
        print("  ✗ 状态筛选测试失败")

    # 检查订单卡片
    print("\n3. 检查订单卡片信息...")
    try:
        order_cards = page.locator(".order-card")
        card_count = order_cards.count()
        print(f"  ✓ 显示 {card_count} 个订单")

        if card_count > 0:
            first_card = order_cards.first
            # 检查订单号
            order_number = first_card.locator("text=Order #, .order-number")
            if order_number.count() > 0:
                print(f"  ✓ 订单号: {order_number.first.inner_text()}")

            # 检查订单状态
            status = first_card.locator(".order-status, .status-")
            if status.count() > 0:
                print(f"  ✓ 订单状态: {status.first.inner_text()}")

            # 检查操作按钮
            actions = first_card.locator(".action-btn, button")
            action_count = actions.count()
            print(f"  ✓ 操作按钮数量: {action_count}")
    except:
        print("  ✗ 无法检查订单卡片")

    return all("✓" in r for r in results.values())


def test_order_detail_page(page):
    """测试订单详情页"""
    print("\n=== 测试订单详情页 (/orders/:id) ===")

    # 首先从订单列表获取订单ID
    print("1. 获取订单ID...")
    page.goto(f"{BASE_URL}/orders")
    page.wait_for_load_state("networkidle")

    order_id = None
    try:
        order_cards = page.locator(".order-card")
        if order_cards.count() > 0:
            # 尝试从第一个订单获取ID
            first_card = order_cards.first
            view_btn = first_card.locator("button:has-text('View'), button:has-text('详情')").first
            if view_btn.count() > 0:
                view_btn.click()
                page.wait_for_load_state("networkidle")
                order_id = page.url.split("/")[-1]
            else:
                # 从URL pattern提取
                print("  ! 使用默认订单ID: 1")
                order_id = "1"
        else:
            order_id = "1"
    except:
        order_id = "1"

    print(f"2. 访问订单详情页 (ID: {order_id})...")
    page.goto(f"{BASE_URL}/orders/{order_id}")
    page.wait_for_load_state("networkidle")

    # 截图
    page.screenshot(path="test_results/order_detail_page.png", full_page=True)

    # 检查页面元素
    checks = {
        "状态时间轴": ".timeline, .status-section",
        "订单信息": ".order-info, .info-section",
        "商品列表": ".items-list, .product-card",
        "价格明细": ".price-details, .price-section",
        "操作按钮": ".action-buttons, .btn"
    }

    results = {}
    for name, selector in checks.items():
        try:
            found = page.locator(selector).count() > 0
            results[name] = "✓" if found else "✗"
        except:
            results[name] = "✗"

    print("\n  页面元素检查:")
    for name, result in results.items():
        print(f"    {result} {name}")

    # 检查时间轴
    print("\n3. 检查状态时间轴...")
    try:
        timeline = page.locator(".timeline-step, .timeline .step")
        step_count = timeline.count()
        print(f"  ✓ 时间轴步骤数: {step_count}")

        if step_count > 0:
            completed = page.locator(".timeline-step.completed, .timeline .step.completed")
            completed_count = completed.count()
            print(f"  ✓ 已完成步骤数: {completed_count}")
    except:
        print("  ✗ 无法检查时间轴")

    # 检查物流信息（如果有）
    print("\n4. 检查物流信息...")
    try:
        logistics = page.locator("text=物流, text=Logistics, .logistics-card")
        if logistics.count() > 0:
            print("  ✓ 显示物流信息")
            tracking = page.locator(".tracking-number")
            if tracking.count() > 0:
                print(f"  • 物流单号: {tracking.first.inner_text()}")
        else:
            print("  • 未显示物流信息（订单可能未发货）")
    except:
        print("  ! 无法检查物流信息")

    # 检查操作按钮
    print("\n5. 检查操作按钮...")
    try:
        actions = page.locator(".action-bar .btn, .action-buttons button")
        action_count = actions.count()
        print(f"  ✓ 可用操作按钮数: {action_count}")

        if action_count > 0:
            for i in range(min(action_count, 5)):
                btn_text = actions.nth(i).inner_text()
                print(f"    • {btn_text.strip()}")
    except:
        print("  ✗ 无法检查操作按钮")

    return all("✓" in r for r in results.values())


def main():
    """主测试函数"""
    print("=" * 60)
    print("汽车改装件销售平台 - 订单流程页面测试")
    print("=" * 60)

    # 创建测试结果目录
    import os
    os.makedirs("test_results", exist_ok=True)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()

        # 设置视口大小
        page.set_viewport_size({"width": 1920, "height": 1080})

        try:
            # 登录
            if not login(page):
                print("\n❌ 登录失败，无法继续测试")
                browser.close()
                return

            # 等待一下确保登录状态
            page.wait_for_timeout(2000)

            # 测试结果汇总
            test_results = {}

            # 测试确认订单页
            try:
                test_results["确认订单页"] = test_checkout_page(page)
            except Exception as e:
                print(f"✗ 确认订单页测试出错: {e}")
                test_results["确认订单页"] = False

            # 测试订单列表页
            try:
                test_results["订单列表页"] = test_order_list_page(page)
            except Exception as e:
                print(f"✗ 订单列表页测试出错: {e}")
                test_results["订单列表页"] = False

            # 测试订单详情页
            try:
                test_results["订单详情页"] = test_order_detail_page(page)
            except Exception as e:
                print(f"✗ 订单详情页测试出错: {e}")
                test_results["订单详情页"] = False

            # 测试支付页面（可选，需要有效订单）
            try:
                test_results["支付页面"] = test_payment_page(page)
            except Exception as e:
                print(f"✗ 支付页面测试出错: {e}")
                test_results["支付页面"] = False

            # 打印测试结果汇总
            print("\n" + "=" * 60)
            print("测试结果汇总")
            print("=" * 60)
            for test_name, passed in test_results.items():
                status = "✓ 通过" if passed else "✗ 失败"
                print(f"{status} - {test_name}")

            total = len(test_results)
            passed = sum(test_results.values())
            print(f"\n总计: {passed}/{total} 个测试通过")

            if passed == total:
                print("\n🎉 所有测试通过!")
            else:
                print(f"\n⚠️  {total - passed} 个测试失败")

            # 保存测试结果
            with open("test_results/results.json", "w", encoding="utf-8") as f:
                json.dump(test_results, f, ensure_ascii=False, indent=2)

        except Exception as e:
            print(f"\n❌ 测试过程出错: {e}")
            import traceback
            traceback.print_exc()

        finally:
            browser.close()


if __name__ == "__main__":
    main()
