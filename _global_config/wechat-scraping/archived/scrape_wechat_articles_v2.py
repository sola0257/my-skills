#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章数据抓取脚本 v2.0
改进：自动检测登录状态，支持重新登录
"""

from playwright.sync_api import sync_playwright
import json
import os
from datetime import datetime

# 配置
COOKIES_FILE = '/Users/dj/Desktop/小静的skills/_global_config/wechat_cookies.json'
OUTPUT_FILE = '/Users/dj/Desktop/小静的skills/_global_config/wechat_articles_data.json'
SCREENSHOT_DIR = '/Users/dj/Desktop/小静的skills/_global_config/'

def load_cookies():
    """加载保存的 cookies"""
    if os.path.exists(COOKIES_FILE):
        with open(COOKIES_FILE, 'r') as f:
            return json.load(f)
    return None

def save_cookies(context):
    """保存 cookies"""
    cookies = context.cookies()
    with open(COOKIES_FILE, 'w') as f:
        json.dump(cookies, f, indent=2)
    print(f"✅ Cookies 已保存: {COOKIES_FILE}")

def save_articles_data(articles):
    """保存抓取的文章数据"""
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"✅ 文章数据已保存: {OUTPUT_FILE}")

def wait_for_login(page):
    """等待用户扫码登录"""
    print("\n📱 请使用微信扫描二维码登录...")
    print("⏳ 等待扫码（最多60秒）...")

    # 截图保存二维码
    screenshot_path = os.path.join(SCREENSHOT_DIR, 'wechat_qrcode.png')
    page.screenshot(path=screenshot_path)
    print(f"📸 二维码已保存: {screenshot_path}")

    try:
        # 等待登录成功（URL 变化）
        page.wait_for_url(lambda url: 'home' in url or 'cgi-bin' in url, timeout=60000)
        print("✅ 登录成功！")
        return True
    except:
        print("❌ 登录超时，请重试")
        return False

def check_login_status(page):
    """检查是否需要重新登录"""
    current_url = page.url

    # 检查是否在登录页面
    if 'login' in current_url.lower():
        return False

    # 检查页面内容
    try:
        # 查找"请重新登录"文本
        relogin_text = page.locator('text=请重新登录').count()
        if relogin_text > 0:
            return False
    except:
        pass

    return True

def scrape_articles():
    """抓取微信公众号已发表文章"""
    print("=" * 60)
    print("微信公众号文章数据抓取 v2.0")
    print("=" * 60)

    with sync_playwright() as p:
        # 启动浏览器
        print("\n🚀 启动浏览器...")
        browser = p.chromium.launch(
            headless=False,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )

        context = browser.new_context()
        page = context.new_page()

        # 尝试加载 cookies
        cookies = load_cookies()
        if cookies:
            print("🔑 加载已保存的 cookies...")
            context.add_cookies(cookies)

        # 访问已发表页面
        print("📄 访问已发表页面...")
        page.goto('https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list')
        page.wait_for_timeout(3000)

        # 检查登录状态
        if not check_login_status(page):
            print("⚠️  需要重新登录")

            # 如果不在登录页面，先跳转到登录页
            if 'login' not in page.url.lower():
                page.goto('https://mp.weixin.qq.com/')
                page.wait_for_timeout(2000)

            # 等待用户扫码登录
            if not wait_for_login(page):
                browser.close()
                return None

            # 保存新的 cookies
            save_cookies(context)

            # 重新访问已发表页面
            print("\n📄 重新访问已发表页面...")
            page.goto('https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list')
            page.wait_for_timeout(3000)
        else:
            print("✅ 登录状态有效")

        print("\n🔍 开始分析页面结构...")

        # 先获取页面的 HTML 结构，帮助我们找到正确的选择器
        page_content = page.content()

        # 保存 HTML 用于调试
        with open(os.path.join(SCREENSHOT_DIR, 'page_structure.html'), 'w', encoding='utf-8') as f:
            f.write(page_content)
        print("📝 页面结构已保存: page_structure.html")

        # 截图当前页面
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, 'current_page.png'))
        print("📸 页面截图已保存: current_page.png")

        # 尝试多种可能的选择器
        print("\n🔎 尝试查找文章列表...")

        # 获取所有可能的文章容器
        articles_data = page.evaluate('''() => {
            // 尝试多种可能的选择器
            const selectors = [
                '.appmsg-list-item',
                '.appmsg_item',
                '.publish_card',
                '[class*="publish"]',
                '[class*="article"]',
                '[class*="msg"]'
            ];

            let items = [];
            for (const selector of selectors) {
                const elements = document.querySelectorAll(selector);
                if (elements.length > 0) {
                    console.log(`找到 ${elements.length} 个元素，选择器: ${selector}`);
                    items = Array.from(elements);
                    break;
                }
            }

            if (items.length === 0) {
                return {
                    success: false,
                    message: '未找到文章列表',
                    html: document.body.innerHTML.substring(0, 1000)
                };
            }

            // 提取文章信息
            const articles = items.map(item => {
                return {
                    html: item.innerHTML.substring(0, 500),
                    text: item.textContent.trim().substring(0, 200)
                };
            });

            return {
                success: true,
                count: articles.length,
                articles: articles
            };
        }''')

        if not articles_data['success']:
            print(f"❌ {articles_data['message']}")
            print("\n💡 建议：")
            print("  1. 查看 page_structure.html 了解页面结构")
            print("  2. 查看 current_page.png 确认页面内容")
            print("  3. 手动在浏览器中检查元素，找到正确的选择器")

            # 保持浏览器打开，让用户可以手动检查
            print("\n⏳ 浏览器将保持打开30秒，请手动检查页面...")
            page.wait_for_timeout(30000)
        else:
            print(f"✅ 找到 {articles_data['count']} 篇文章")
            print("\n📝 前3篇文章的HTML片段：")
            for i, article in enumerate(articles_data['articles'][:3], 1):
                print(f"\n--- 文章 {i} ---")
                print(f"文本内容: {article['text'][:100]}...")

            # 保存原始数据
            save_articles_data(articles_data)

            print("\n⏳ 浏览器将保持打开30秒，请查看结果...")
            page.wait_for_timeout(30000)

        browser.close()

    print("\n" + "=" * 60)
    print("✅ 抓取完成！")
    print("=" * 60)

    return articles_data

def main():
    try:
        result = scrape_articles()
        if result and result.get('success'):
            print(f"\n💡 下一步：")
            print(f"  1. 查看 page_structure.html 了解页面结构")
            print(f"  2. 根据实际结构编写精确的数据提取逻辑")
            print(f"  3. 提取标题、发布时间、合集等字段")
            print(f"  4. 集成到飞书自动同步")
    except Exception as e:
        print(f"\n❌ 抓取失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
