#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章数据抓取脚本
功能：从已发表页面抓取文章列表，提取标题、发布时间、内容类型、合集等信息
"""

from playwright.sync_api import sync_playwright
import json
import os
from datetime import datetime

# 配置
COOKIES_FILE = '/Users/dj/Desktop/小静的skills/_global_config/wechat_cookies.json'
OUTPUT_FILE = '/Users/dj/Desktop/小静的skills/_global_config/wechat_articles_data.json'

def load_cookies():
    """加载保存的 cookies"""
    if os.path.exists(COOKIES_FILE):
        with open(COOKIES_FILE, 'r') as f:
            return json.load(f)
    return None

def save_articles_data(articles):
    """保存抓取的文章数据"""
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False, indent=2)
    print(f"✅ 文章数据已保存: {OUTPUT_FILE}")

def scrape_articles():
    """抓取微信公众号已发表文章"""
    print("=" * 60)
    print("微信公众号文章数据抓取")
    print("=" * 60)

    # 加载 cookies
    cookies = load_cookies()
    if not cookies:
        print("❌ 未找到 cookies 文件，请先运行 test_playwright_login.py 登录")
        return

    with sync_playwright() as p:
        # 启动浏览器
        print("\n🚀 启动浏览器...")
        browser = p.chromium.launch(
            headless=False,
            args=['--no-sandbox', '--disable-setuid-sandbox']
        )

        context = browser.new_context()
        page = context.new_page()

        # 设置 cookies
        print("🔑 加载 cookies...")
        context.add_cookies(cookies)

        # 访问已发表页面
        print("📄 访问已发表页面...")
        page.goto('https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list')
        page.wait_for_timeout(3000)

        # 检查是否登录成功
        current_url = page.url
        if 'login' in current_url.lower():
            print("❌ Cookies 已过期，请重新运行 test_playwright_login.py 登录")
            browser.close()
            return

        print("✅ 登录成功，开始抓取数据...")

        # 等待页面加载完成
        try:
            # 等待文章列表加载
            page.wait_for_selector('.appmsg-list', timeout=10000)
            print("✅ 文章列表加载完成")
        except:
            print("⚠️  未找到文章列表，可能页面结构已变化")
            # 截图保存当前页面
            page.screenshot(path='/Users/dj/Desktop/小静的skills/_global_config/debug_page.png')
            print("📸 已保存调试截图: debug_page.png")
            browser.close()
            return

        # 提取文章列表
        print("\n📊 提取文章数据...")
        articles = page.evaluate('''() => {
            const items = document.querySelectorAll('.appmsg-list-item');
            return Array.from(items).map(item => {
                // 提取标题
                const titleElem = item.querySelector('.title');
                const title = titleElem ? titleElem.textContent.trim() : '';

                // 提取发布时间
                const timeElem = item.querySelector('.time');
                const publishTime = timeElem ? timeElem.textContent.trim() : '';

                // 提取文章链接
                const linkElem = item.querySelector('a');
                const url = linkElem ? linkElem.href : '';

                // 提取内容类型（图文/长文）
                // 这个需要根据实际页面结构调整
                const typeElem = item.querySelector('.type');
                const contentType = typeElem ? typeElem.textContent.trim() : '未知';

                return {
                    title: title,
                    publishTime: publishTime,
                    url: url,
                    contentType: contentType
                };
            });
        }''')

        print(f"✅ 成功提取 {len(articles)} 篇文章")

        # 打印前3篇文章作为示例
        if articles:
            print("\n📝 示例数据（前3篇）：")
            for i, article in enumerate(articles[:3], 1):
                print(f"\n{i}. {article['title']}")
                print(f"   发布时间: {article['publishTime']}")
                print(f"   内容类型: {article['contentType']}")

        # 保存数据
        save_articles_data(articles)

        # 保持浏览器打开一段时间
        print("\n⏳ 浏览器将在5秒后关闭...")
        page.wait_for_timeout(5000)

        browser.close()

    print("\n" + "=" * 60)
    print("✅ 抓取完成！")
    print("=" * 60)

    return articles

def main():
    try:
        articles = scrape_articles()
        if articles:
            print(f"\n💡 下一步：")
            print(f"  1. 检查 {OUTPUT_FILE} 中的数据")
            print(f"  2. 根据实际页面结构调整选择器")
            print(f"  3. 实现合集信息抓取")
            print(f"  4. 集成到飞书自动同步")
    except Exception as e:
        print(f"\n❌ 抓取失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
