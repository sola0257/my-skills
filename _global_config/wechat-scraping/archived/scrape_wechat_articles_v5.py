#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章数据抓取脚本 v5.0
基于完整录制流程优化
功能：
1. 自动登录（扫码）
2. 抓取所有已发表文章
3. 支持翻页
4. 提取标题、URL、发布时间等信息
"""

from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import json
import os
import time
from datetime import datetime
import re

# 配置
OUTPUT_FILE = '/Users/dj/Desktop/小静的skills/_global_config/wechat_articles_data.json'
SCREENSHOT_DIR = '/Users/dj/Desktop/小静的skills/_global_config/'

def wait_for_login(page):
    """等待用户扫码登录"""
    print("\n📱 请使用微信扫描二维码登录...")
    print("⏳ 等待扫码（最多60秒）...")

    # 截图保存二维码
    screenshot_path = os.path.join(SCREENSHOT_DIR, 'qrcode_login.png')
    page.screenshot(path=screenshot_path)
    print(f"📸 二维码已保存: {screenshot_path}")

    try:
        # 等待登录成功（URL 变化到首页）
        page.wait_for_url(lambda url: 'home' in url or 'cgi-bin' in url, timeout=60000)
        print("✅ 登录成功！")

        # 保存登录后的 cookies
        context = page.context
        cookies = context.cookies()
        cookies_file = os.path.join(SCREENSHOT_DIR, 'wechat_cookies.json')
        with open(cookies_file, 'w') as f:
            json.dump(cookies, f, indent=2)
        print(f"✅ Cookies 已保存: {cookies_file}")

        return True
    except:
        print("❌ 登录超时，请重试")
        return False

def navigate_to_published_list(page):
    """导航到已发表页面"""
    print("\n🔍 导航到已发表页面...")

    try:
        # 点击"内容管理"
        page.get_by_text("内容管理").click()
        time.sleep(1)

        # 点击"发表记录"
        page.get_by_role("link", name="发表记录").click()
        time.sleep(3)

        print("✅ 已进入发表记录页面")
        return True
    except Exception as e:
        print(f"❌ 导航失败: {e}")
        return False

def extract_articles_from_page(page):
    """从当前页面提取文章列表"""
    articles = []

    try:
        # 获取所有文章链接
        article_links = page.get_by_role("link").all()

        for link in article_links:
            try:
                text = link.inner_text()
                href = link.get_attribute('href')

                # 过滤条件：排除导航链接
                if not text or len(text) < 5:
                    continue

                # 排除导航和功能链接
                exclude_keywords = ['登录', '内容管理', '发表记录', '素材管理',
                                   '原创', '合集', '下一页', '上一页', '首页', '尾页']
                if any(keyword in text for keyword in exclude_keywords):
                    continue

                # 只保留文章链接（包含 appmsg 或 s?__biz）
                if href and ('appmsg' in href or 's?__biz' in href):
                    articles.append({
                        'title': text.strip(),
                        'url': href,
                        'extracted_at': datetime.now().isoformat()
                    })

            except Exception as e:
                continue

    except Exception as e:
        print(f"⚠️  提取文章失败: {e}")

    return articles

def scrape_all_articles():
    """抓取所有文章（支持翻页）"""
    print("=" * 60)
    print("微信公众号文章数据抓取 v5.0")
    print("=" * 60)

    all_articles = []

    with sync_playwright() as p:
        # 启动浏览器
        print("\n🚀 启动浏览器...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 访问登录页
        print("📄 访问微信公众号...")
        page.goto('https://mp.weixin.qq.com/')
        time.sleep(2)

        # 等待登录
        if not wait_for_login(page):
            browser.close()
            return None

        # 导航到已发表页面
        if not navigate_to_published_list(page):
            browser.close()
            return None

        # 抓取第一页
        print("\n📊 开始抓取文章...")
        page_num = 1
        
        while True:
            print(f"\n📄 正在抓取第 {page_num} 页...")
            
            # 提取当前页文章
            articles = extract_articles_from_page(page)
            
            if articles:
                print(f"  ✅ 找到 {len(articles)} 篇文章")
                all_articles.extend(articles)
                
                # 显示前3篇
                for i, article in enumerate(articles[:3], 1):
                    print(f"    {i}. {article['title'][:50]}...")
            else:
                print("  ⚠️  本页未找到文章")

            # 尝试翻页
            try:
                next_button = page.get_by_role("link", name="下一页")
                if next_button.is_visible() and next_button.is_enabled():
                    print("  ⏭️  翻到下一页...")
                    next_button.click()
                    time.sleep(3)
                    page_num += 1
                else:
                    print("  ✅ 已到最后一页")
                    break
            except:
                print("  ✅ 已到最后一页")
                break

        print(f"\n✅ 抓取完成！共 {len(all_articles)} 篇文章")

        # 保存数据
        if all_articles:
            with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
                json.dump(all_articles, f, ensure_ascii=False, indent=2)
            print(f"✅ 数据已保存: {OUTPUT_FILE}")

        # 截图
        screenshot_path = os.path.join(SCREENSHOT_DIR, 'final_page.png')
        page.screenshot(path=screenshot_path)
        print(f"📸 最终页面截图: {screenshot_path}")

        # 保持浏览器打开
        print("\n⏳ 浏览器将保持打开30秒...")
        time.sleep(30)

        browser.close()

    return all_articles

def main():
    try:
        articles = scrape_all_articles()
        
        if articles:
            print(f"\n" + "=" * 60)
            print(f"✅ 成功抓取 {len(articles)} 篇文章")
            print("=" * 60)
            
            print(f"\n💡 下一步：")
            print(f"  1. 查看 {OUTPUT_FILE}")
            print(f"  2. 提取更多字段（发布时间、合集等）")
            print(f"  3. 集成到飞书自动同步")
        else:
            print("\n⚠️  未抓取到文章")
            
    except Exception as e:
        print(f"\n❌ 抓取失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
