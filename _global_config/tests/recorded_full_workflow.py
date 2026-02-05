import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://mp.weixin.qq.com/cgi-bin/home?t=home/index&lang=zh_CN&token=642932253")
    page.get_by_text("内容管理").click()
    page.get_by_text("内容管理").click()
    page.get_by_text("内容管理").click()
    page.get_by_role("link", name="发表记录").click()
    page.locator("div:nth-child(3) > .weui-desktop-block__main > .weui-desktop-block__content > .weui-desktop-mass__content > .publish_hover_content > .weui-desktop-mass__overview > div > div:nth-child(2) > .weui-desktop-mass__status > .weui-desktop-popover__wrp > .weui-desktop-popover__target > .weui-desktop-mass__status_text > .weui-desktop-mass__status_text_arrow").click()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="立春赏花图鉴：把春天最早的消息带给你 🌸").click()
    page1 = page1_info.value
    page1.get_by_role("button").filter(has_text=re.compile(r"^$")).click()
    page1.locator("button").nth(3).click()
    page1.locator("button").nth(3).click()
    page1.close()
    with page.expect_popup() as page2_info:
        page.get_by_role("link", name="立春就急着施肥？难怪你的花总是黄叶！（10").click()
    page2 = page2_info.value
    page2.close()
    page.get_by_role("link", name="原创", exact=True).click()
    page.get_by_role("link", name="下一页").click()
    page.get_by_role("link", name="下一页").click()
    page.get_by_role("link", name="发表记录").click()
    page.locator("label").filter(has_text="2").click()
    page.get_by_role("link", name="下一页").click()
    page.get_by_role("link", name="上一页").click()
    page.get_by_role("link", name="合集").click()
    page.get_by_role("button").filter(has_text=re.compile(r"^$")).click()
    page.get_by_role("listitem").filter(has_text=re.compile(r"^文章合集$")).click()
    page.get_by_role("listitem").filter(has_text="图文合集").click()

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
