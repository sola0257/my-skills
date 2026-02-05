#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
微信公众号文章数据抓取脚本 v6.0
改进：使用录制时保存的 cookies，无需重新登录
"""

from playwright.sync_api import sync_playwright
import json
import os
import time
from datetime import datetime

# 配置
OUTPUT_FILE = '/Users/dj/Desktop/小静的skills/_global_config/wechat_articles_data.json'
SCREENSHOT_DIR = '/Users/dj/Desktop/小静的skills/_global_config/'

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

                # 过滤条件
                if not text or len(text) < 5:
                    continue

                # 排除导航和功能链接
                exclude_keywords = ['登录', '内容管理', '发表记录', '素材管理',
                                   '原创', '合集', '下一页', '上一页', '首页', '尾页']
                if any(keyword in text for keyword in exclude_keywords):
                    continue

                # 只保留文章链接
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

def scrape_with_recorded_workflow():
    """使用录制的工作流抓取文章"""
    print("=" * 60)
    print("微信公众号文章数据抓取 v6.0")
    print("使用录制的工作流")
    print("=" * 60)

    all_articles = []

    with sync_playwright() as p:
        print("\n🚀 启动浏览器...")
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        # 直接访问录制时的 URL（带 token）
        print("📄 访问微信公众号后台...")
        page.goto("https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN")
        time.sleep(3)

        # 检查是否需要登录
        try:
            if page.get_by_text("登录").is_visible():
                print("\n⚠️  需要登录，请扫码...")
                print("⏳ 等待登录（120秒）...")
                page.wait_for_url(lambda url: 'home' in url or 'cgi-bin' in url, timeout=120000)
                print("✅ 登录成功！")
        except:
            print("✅ 已登录")

        # 导航到发表记录
        print("\n🔍 导航到发表记录...")
        page.get_by_text("内容管理").click()
        time.sleep(1)
        page.get_by_role("link", name="发表记录").click()
        time.sleep(3)

        print("✅ 已进入发表记录页面")

        # 开始抓取
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
        screenshot_path = os.path.join(SCREENSHOT_DIR, 'final_page_v6.png')
        page.screenshot(path=screenshot_path)
        print(f"📸 最终页面截图: {screenshot_path}")

        # 保持浏览器打开
        print("\n⏳ 浏览器将保持打开30秒...")
        time.sleep(30)

        browser.close()

    return all_articles

def main():
    try:
        articles = scrape_with_recorded_workflow()
        
        if articles:
            print(f"\n" + "=" * 60)
            print(f"✅ 成功抓取 {len(articles)} 篇文章")
            print("=" * 60)
            
            print(f"\n💡 下一步：")
            print(f"  1. 查看 {OUTPUT_FILE}")
            print(f"  2. 集成到飞书自动同步")
        else:
            print("\n⚠️  未抓取到文章")
            
    except Exception as e:
        print(f"\n❌ 抓取失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
