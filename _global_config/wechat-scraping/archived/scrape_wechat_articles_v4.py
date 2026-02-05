#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章数据抓取脚本 v4.0
基于 Playwright Codegen 录制的操作流程优化
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import json
import os
import time
from datetime import datetime

# 配置
STORAGE_STATE_FILE = '/Users/dj/Desktop/小静的skills/_global_config/wechat_storage_state.json'
OUTPUT_FILE = '/Users/dj/Desktop/小静的skills/_global_config/wechat_articles_data.json'
SCREENSHOT_DIR = '/Users/dj/Desktop/小静的skills/_global_config/'

def scrape_articles():
    """抓取微信公众号已发表文章"""
    print("=" * 60)
    print("微信公众号文章数据抓取 v4.0")
    print("基于录制的操作流程")
    print("=" * 60)

    with sync_playwright() as p:
        # 启动浏览器
        print("\n🚀 启动浏览器...")
        browser = p.chromium.launch(headless=False)

        # 加载 storage state（包含 cookies）
        print("🔑 加载已保存的登录状态...")
        context = browser.new_context(storage_state=STORAGE_STATE_FILE)
        page = context.new_page()

        # 访问已发表页面
        print("📄 访问已发表页面...")
        page.goto("https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list")

        # 等待页面加载
        print("⏳ 等待页面加载...")
        time.sleep(5)

        # 检查是否需要登录
        try:
            login_link = page.get_by_role("link", name="登录")
            if login_link.is_visible():
                print("⚠️  检测到需要登录，请在浏览器中手动登录...")
                print("⏳ 等待登录（60秒）...")
                time.sleep(60)
        except:
            print("✅ 已登录")

        # 尝试导航到发表记录（如果需要）
        try:
            print("\n🔍 查找发表记录...")
            # 点击"内容管理"
            content_mgmt = page.get_by_title("内容管理")
            if content_mgmt.is_visible():
                content_mgmt.click()
                time.sleep(1)

            # 点击"发表记录"
            publish_record = page.get_by_role("link", name="发表记录")
            if publish_record.is_visible():
                publish_record.click()
                time.sleep(3)
        except Exception as e:
            print(f"⚠️  导航操作失败: {e}")
            print("💡 可能已经在正确的页面")

        # 截图当前页面
        screenshot_path = os.path.join(SCREENSHOT_DIR, 'articles_list_v4.png')
        page.screenshot(path=screenshot_path)
        print(f"📸 页面截图已保存: {screenshot_path}")

        # 提取所有文章链接
        print("\n📊 提取文章列表...")
        articles = []

        try:
            # 获取所有文章链接
            # 根据录制的代码，文章标题是 role="link" 的元素
            article_links = page.get_by_role("link").all()

            print(f"✅ 找到 {len(article_links)} 个链接")

            # 过滤出文章链接（包含"原创"或其他特征）
            for link in article_links:
                try:
                    text = link.inner_text()
                    href = link.get_attribute('href')

                    # 过滤条件：文本不为空，且不是导航链接
                    if text and len(text) > 5 and href:
                        # 排除导航链接
                        if any(keyword in text for keyword in ['登录', '内容管理', '发表记录', '素材管理']):
                            continue

                        articles.append({
                            'title': text,
                            'url': href,
                            'extracted_at': datetime.now().isoformat()
                        })
                        print(f"  - {text[:50]}...")
                except Exception as e:
                    continue

            print(f"\n✅ 成功提取 {len(articles)} 篇文章")

        except Exception as e:
            print(f"❌ 提取失败: {e}")

            # 保存页面HTML用于调试
            html_path = os.path.join(SCREENSHOT_DIR, 'page_debug_v4.html')
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(page.content())
            print(f"📝 页面HTML已保存: {html_path}")

        # 保存数据
        if articles:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(articles, f, ensure_ascii=False, indent=2)
            print(f"\n✅ 文章数据已保存: {OUTPUT_FILE}")

            # 显示前3篇
            print("\n📝 前3篇文章：")
            for i, article in enumerate(articles[:3], 1):
                print(f"\n{i}. {article['title']}")
                print(f"   URL: {article['url'][:80]}...")

        # 保持浏览器打开
        print("\n⏳ 浏览器将保持打开30秒，请检查结果...")
        time.sleep(30)

        # 关闭
        context.close()
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
            print(f"  1. 查看 {OUTPUT_FILE} 中的数据")
            print(f"  2. 提取更多字段（发布时间、合集等）")
            print(f"  3. 集成到飞书自动同步")
        else:
            print(f"\n⚠️  未提取到文章数据")
            print(f"  1. 查看截图 articles_list_v4.png")
            print(f"  2. 查看调试HTML page_debug_v4.html")
            print(f"  3. 手动检查页面结构")

    except Exception as e:
        print(f"\n❌ 抓取失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
