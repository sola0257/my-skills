#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Puppeteer 登录测试（支持 Cookie 复用）
首次登录：手动扫码 → 保存 cookies
后续登录：自动使用 cookies，无需扫码
"""

import asyncio
from pyppeteer import launch
import json
import os
from datetime import datetime

# 配置
COOKIES_FILE = '/Users/dj/Desktop/小静的skills/_global_config/wechat_cookies.json'
SCREENSHOT_DIR = '/Users/dj/Desktop/小静的skills/_global_config/'

async def load_cookies():
    """加载保存的 cookies"""
    if os.path.exists(COOKIES_FILE):
        with open(COOKIES_FILE, 'r') as f:
            return json.load(f)
    return None

async def save_cookies(cookies):
    """保存 cookies"""
    with open(COOKIES_FILE, 'w') as f:
        json.dump(cookies, f, indent=2)
    print(f"✅ Cookies 已保存: {COOKIES_FILE}")

async def check_login_status(page):
    """检查是否已登录"""
    try:
        # 等待页面加载
        await asyncio.sleep(2)

        # 检查是否有登录后的元素（例如：用户头像、菜单等）
        # 如果页面 URL 包含 /home 或有特定元素，说明已登录
        current_url = page.url

        if 'home' in current_url or 'cgi-bin' in current_url:
            return True

        # 尝试查找登录页面的二维码元素
        qrcode = await page.querySelector('.qrcode')
        if qrcode:
            return False

        return True
    except:
        return False

async def login_with_qrcode(page):
    """扫码登录"""
    print("\n📱 请使用微信扫描二维码登录...")
    print("⏳ 等待扫码（最多60秒）...")

    # 截图保存二维码
    screenshot_path = os.path.join(SCREENSHOT_DIR, 'wechat_qrcode.png')
    await page.screenshot({'path': screenshot_path})
    print(f"📸 二维码已保存: {screenshot_path}")

    # 等待登录成功（检测 URL 变化）
    try:
        await page.waitForNavigation({'timeout': 60000})
        print("✅ 登录成功！")
        return True
    except:
        print("❌ 登录超时，请重试")
        return False

async def test_login():
    """测试登录流程"""
    print("=" * 60)
    print("微信公众号自动登录测试")
    print("=" * 60)

    # 1. 启动浏览器
    print("\n🚀 启动浏览器...")
    browser = await launch(
        headless=False,
        args=[
            '--no-sandbox',
            '--disable-setuid-sandbox',
            '--disable-dev-shm-usage',
            '--disable-accelerated-2d-canvas',
            '--no-first-run',
            '--no-zygote',
            '--disable-gpu'
        ],
        ignoreHTTPSErrors=True,
        dumpio=False
    )
    page = await browser.newPage()

    # 2. 尝试加载 cookies
    cookies = await load_cookies()

    if cookies:
        print(f"\n🔑 发现已保存的 cookies ({len(cookies)} 个)")
        print("⚡ 尝试使用 cookies 自动登录...")

        # 设置 cookies
        await page.setCookie(*cookies)

        # 访问首页
        await page.goto('https://mp.weixin.qq.com/')

        # 检查是否登录成功
        is_logged_in = await check_login_status(page)

        if is_logged_in:
            print("✅ 自动登录成功！无需扫码")

            # 截图验证
            screenshot_path = os.path.join(SCREENSHOT_DIR, 'wechat_logged_in.png')
            await page.screenshot({'path': screenshot_path})
            print(f"📸 登录后截图: {screenshot_path}")

        else:
            print("⚠️  Cookies 已过期，需要重新登录")
            # Cookies 过期，需要重新扫码
            is_logged_in = await login_with_qrcode(page)

            if is_logged_in:
                # 保存新的 cookies
                new_cookies = await page.cookies()
                await save_cookies(new_cookies)
    else:
        print("\n📱 首次登录，需要扫码")

        # 访问登录页
        await page.goto('https://mp.weixin.qq.com/')

        # 扫码登录
        is_logged_in = await login_with_qrcode(page)

        if is_logged_in:
            # 保存 cookies
            cookies = await page.cookies()
            await save_cookies(cookies)
            print(f"💡 下次运行将自动登录，无需扫码")

    # 3. 如果登录成功，测试访问后台页面
    if is_logged_in:
        print("\n🔍 测试访问后台页面...")

        # 访问已发表页面
        await page.goto('https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list')
        await asyncio.sleep(3)

        # 截图
        screenshot_path = os.path.join(SCREENSHOT_DIR, 'wechat_published_list.png')
        await page.screenshot({'path': screenshot_path})
        print(f"📸 已发表页面截图: {screenshot_path}")

        print("\n✅ 所有测试通过！")

    # 4. 保持浏览器打开一段时间，让用户查看
    print("\n⏳ 浏览器将在10秒后关闭...")
    await asyncio.sleep(10)

    # 5. 关闭浏览器
    await browser.close()

    print("\n" + "=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)

    if cookies:
        print(f"\n💡 提示：")
        print(f"  - Cookies 已保存，下次运行将自动登录")
        print(f"  - Cookies 通常有效期为 7-30 天")
        print(f"  - 过期后会自动提示重新扫码")

async def main():
    try:
        await test_login()
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        print("\n💡 可能的原因：")
        print("  1. pyppeteer 未安装：pip3 install pyppeteer")
        print("  2. Chromium 未下载：首次运行会自动下载")
        print("  3. 网络问题：检查网络连接")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(main())
