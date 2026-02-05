#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章数据抓取脚本 v3.0
改进：增加页面加载等待时间，处理动态内容
"""

from playwright.sync_api import sync_playwright
import json
import os
import time

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
        # 等待登录成功
        page.wait_for_url(lambda url: 'home' in url or 'cgi-bin' in url, timeout=60000)
        print("✅ 登录成功！")
        # 登录成功后等待一下，确保 session 稳定
        page.wait_for_timeout(2000)
        return True
    except:
        print("❌ 登录超时，请重试")
        return False

def scrape_articles():
    """抓取微信公众号已发表文章"""
    print("=" * 60)
    print("微信公众号文章数据抓取 v3.0")
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
        need_login = True

        if cookies:
            print("🔑 尝试使用已保存的 cookies...")
            context.add_cookies(cookies)

            # 先访问首页，确保 cookies 生效
            page.goto('https://mp.weixin.qq.com/')
            page.wait_for_timeout(3000)

            # 检查是否需要登录
            if 'login' not in page.url.lower():
                print("✅ Cookies 有效，已登录")
                need_login = False
            else:
                print("⚠️  Cookies 已过期")

        if need_login:
            print("\n📱 需要扫码登录...")
            page.goto('https://mp.weixin.qq.com/')
            page.wait_for_timeout(2000)

            if not wait_for_login(page):
                browser.close()
                return None

            # 保存新的 cookies
            save_cookies(context)

        # 现在访问已发表页面
        print("\n📄 访问已发表页面...")
        page.goto('https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list')

        # 等待页面加载 - 增加等待时间
        print("⏳ 等待页面加载（10秒）...")
        page.wait_for_timeout(10000)

        # 截图当前页面
        page.screenshot(path=os.path.join(SCREENSHOT_DIR, 'articles_page.png'))
        print("📸 页面截图已保存: articles_page.png")

        # 检查页面内容
        page_text = page.content()

        if '请重新登录' in page_text or '请登录' in page_text:
            print("❌ 页面要求重新登录，session 可能已失效")
            print("💡 建议：关闭所有浏览器窗口，重新运行脚本")
            browser.close()
            return None

        # 保存完整的页面HTML用于分析
        with open(os.path.join(SCREENSHOT_DIR, 'full_page.html'), 'w', encoding='utf-8') as f:
            f.write(page_text)
        print("📝 完整页面HTML已保存: full_page.html")

        print("\n🔍 分析页面内容...")

        # 尝试执行 JavaScript 获取页面数据
        articles_data = page.evaluate('''() => {
            // 尝试从全局变量获取数据
            if (window.wx && window.wx.data) {
                return {
                    success: true,
                    source: 'window.wx.data',
                    data: window.wx.data
                };
            }

            // 尝试从 DOM 获取
            const scripts = document.querySelectorAll('script');
            for (const script of scripts) {
                const text = script.textContent;
                if (text.includes('list') || text.includes('article')) {
                    return {
                        success: true,
                        source: 'script_tag',
                        snippet: text.substring(0, 500)
                    };
                }
            }

            // 查找所有可能的文章容器
            const containers = document.querySelectorAll('[class*="list"], [class*="item"], [class*="card"]');

            return {
                success: containers.length > 0,
                source: 'dom_elements',
                count: containers.length,
                sample: containers.length > 0 ? containers[0].outerHTML.substring(0, 500) : null
            };
        }''')

        print(f"\n📊 页面分析结果：")
        print(f"  数据来源: {articles_data.get('source')}")
        print(f"  成功: {articles_data.get('success')}")

        if articles_data.get('data'):
            print(f"  找到全局数据对象")
            print(f"  数据内容: {str(articles_data['data'])[:200]}...")

        if articles_data.get('snippet'):
            print(f"  找到相关脚本片段")
            print(f"  片段内容: {articles_data['snippet'][:200]}...")

        if articles_data.get('count'):
            print(f"  找到 {articles_data['count']} 个可能的容器元素")

        # 保存分析结果
        save_articles_data(articles_data)

        # 保持浏览器打开，让用户可以手动检查
        print("\n⏳ 浏览器将保持打开60秒，请手动检查页面...")
        print("💡 你可以：")
        print("  1. 在浏览器中右键点击文章标题 → 检查元素")
        print("  2. 查看元素的 class 名称和结构")
        print("  3. 告诉我正确的选择器")
        page.wait_for_timeout(60000)

        browser.close()

    print("\n" + "=" * 60)
    print("✅ 分析完成！")
    print("=" * 60)

    return articles_data

def main():
    try:
        result = scrape_articles()
        if result:
            print(f"\n💡 下一步：")
            print(f"  1. 查看 full_page.html 了解完整页面结构")
            print(f"  2. 查看 articles_page.png 确认页面内容")
            print(f"  3. 在浏览器中手动检查元素，找到正确的选择器")
            print(f"  4. 告诉我正确的选择器，我来更新脚本")
    except Exception as e:
        print(f"\n❌ 抓取失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
