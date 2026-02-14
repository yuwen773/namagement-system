from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()

    # 设置 viewport
    page.set_viewport_size({"width": 1280, "height": 720})

    print("1. 访问景点详情页面...")
    page.goto('http://localhost:5174/attractions/1/')
    page.wait_for_load_state('networkidle')
    time.sleep(2)

    # 截图查看页面状态
    page.screenshot(path='D:/work/code/personal/namagement-system/tourist-attraction-recommendation-system/verify_script/attraction_detail.png', full_page=True)
    print("页面截图已保存")

    # 检查是否有登录提示或收藏按钮
    print("\n2. 检查页面元素...")

    # 查找收藏按钮 - 使用 .first 属性
    favorite_btn = page.locator('.favorite-btn').first
    if favorite_btn.is_visible():
        print(f"收藏按钮可见，按钮文字: {favorite_btn.inner_text()}")
    else:
        print("收藏按钮不可见")

    # 检查是否需要登录
    login_prompt = page.locator('.login-prompt')
    if login_prompt.is_visible():
        print("需要登录，先进行登录...")

        # 访问登录页面
        page.goto('http://localhost:5174/login')
        page.wait_for_load_state('networkidle')

        # 输入用户名密码登录
        page.fill('input[type="text"]', 'user1')
        page.fill('input[type="password"]', 'password123')
        page.click('button[type="submit"]')
        page.wait_for_load_state('networkidle')
        time.sleep(1)

        # 再次访问景点详情页
        page.goto('http://localhost:5174/attractions/1/')
        page.wait_for_load_state('networkidle')
        time.sleep(2)

    # 再次检查收藏按钮状态
    favorite_btn = page.locator('.favorite-btn').first
    if favorite_btn.is_visible():
        is_favorited = favorite_btn.evaluate('el => el.classList.contains("active")')
        btn_text = favorite_btn.inner_text()
        print(f"\n3. 收藏按钮状态: {'已收藏' if is_favorited else '未收藏'}, 文字: {btn_text}")

        # 点击收藏按钮
        print("\n4. 点击收藏按钮...")
        favorite_btn.click()
        time.sleep(1)

        # 截图查看结果
        page.screenshot(path='D:/work/code/personal/namagement-system/tourist-attraction-recommendation-system/verify_script/after_favorite.png', full_page=True)

        # 检查按钮状态
        is_favorited = favorite_btn.evaluate('el => el.classList.contains("active")')
        btn_text = favorite_btn.inner_text()
        print(f"点击后收藏按钮状态: {'已收藏' if is_favorited else '未收藏'}, 文字: {btn_text}")

        # 再次点击测试取消收藏
        print("\n5. 再次点击测试取消收藏...")
        favorite_btn.click()
        time.sleep(1)

        is_favorited = favorite_btn.evaluate('el => el.classList.contains("active")')
        btn_text = favorite_btn.inner_text()
        print(f"取消收藏后状态: {'已收藏' if is_favorited else '未收藏'}, 文字: {btn_text}")

        page.screenshot(path='D:/work/code/personal/namagement-system/tourist-attraction-recommendation-system/verify_script/after_unfavorite.png', full_page=True)

    browser.close()
    print("\n测试完成!")
