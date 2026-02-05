#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Puppeteer MCP 基础测试
测试是否能够正常使用 Puppeteer 控制浏览器
"""

import asyncio
from pyppeteer import launch
import os

async def test_basic():
    """基础测试：打开网页并截图"""
    print("=" * 60)
    print("Puppeteer MCP 基础测试")
    print("=" * 60)

    print("\n🚀 启动浏览器...")
    browser = await launch(
        headless=False,  # 显示浏览器窗口
        args=['--no-sandbox', '--disable-setuid-sandbox']
    )

    page = await browser.newPage()

    print("📄 访问微信公众号登录页...")
    await page.goto('https://mp.weixin.qq.com/')

    # 等待页面加载
    await asyncio.sleep(3)

    print("📸 截图...")
    screenshot_path = '/Users/dj/Desktop/小静的skills/_global_config/wechat_login.png'
    await page.screenshot({'path': screenshot_path})

    print(f"✅ 截图已保存: {screenshot_path}")
    print("\n💡 提示：")
    print("  1. 浏览器窗口将保持打开30秒")
    print("  2. 您可以手动扫码登录测试")
    print("  3. 登录成功后，我们将保存 cookies")

    # 等待用户操作
    print("\n⏳ 等待30秒...")
    await asyncio.sleep(30)

    # 尝试获取 cookies
    cookies = await page.cookies()
    if cookies:
        print(f"\n✅ 获取到 {len(cookies)} 个 cookies")
        # 保存 cookies
        import json
        cookies_file = '/Users/dj/Desktop/小静的skills/_global_config/wechat_cookies.json'
        with open(cookies_file, 'w') as f:
            json.dump(cookies, f, indent=2)
        print(f"✅ Cookies 已保存: {cookies_file}")
    else:
        print("\n⚠️  未获取到 cookies（可能未登录）")

    print("\n🔒 关闭浏览器...")
    await browser.close()

    print("\n" + "=" * 60)
    print("✅ 测试完成！")
    print("=" * 60)

if __name__ == "__main__":
    try:
        asyncio.run(test_basic())
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        print("\n💡 可能的原因：")
        print("  1. pyppeteer 未安装：pip3 install pyppeteer")
        print("  2. Chromium 未下载：首次运行会自动下载")
        print("  3. 网络问题：检查网络连接")
