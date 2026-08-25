import time

from playwright.sync_api import Page, expect


def test_search(page:Page):
    print("url:" + page.url)
    # 因为 conftest 中已经 goto 了百度，这里直接操作
    input_box = page.locator("//textarea[@id='chat-textarea']")
    time.sleep(1)
    input_box.click()
    time.sleep(1)
    input_box.fill("《明日方舟》")
    # page.locator("//button[@id='chat-submit-button']").click()
    page.evaluate('location.href="https://qq.com"')
    time.sleep(1)
    page.screenshot(path="./screenshot.png")
