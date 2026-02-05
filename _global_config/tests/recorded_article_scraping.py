import re
from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context(storage_state="wechat_storage_state.json")
    page = context.new_page()
    page.goto("https://mp.weixin.qq.com/cgi-bin/appmsgpublish?sub=list")
    page.get_by_role("link", name="登录").click()
    page.get_by_title("内容管理").click()
    page.get_by_role("link", name="发表记录").click()
    with page.expect_popup() as page1_info:
        page.get_by_role("link", name="君子兰冬季养护：温差管理与烂心预防完全指南 原创").click()
    page1 = page1_info.value

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)
