from playwright.sync_api import Playwright, sync_playwright, expect


def run(playwright: Playwright) -> None:
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://www.baidu.com/")
    input_box = page.locator("//textarea[@id='chat-textarea']")
    input_box.click()
    input_box.fill("《明日方舟》")
    page.locator("//button[@id='chat-submit-button']").click()
    expect(page.get_by_role("link", name="《明日方舟》2026 [夏日嘉年华] 8.1狂欢开启! 官方")).to_be_visible()
    expect(page.locator("[id=\"3001\"]")).to_contain_text("《明日方舟》")

    # ---------------------
    context.close()
    browser.close()


with sync_playwright() as playwright:
    run(playwright)