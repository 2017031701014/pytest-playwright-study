from playwright.sync_api import Page
import re


# spec 给出了可范围
def test_assert_spec_char1(page:Page):
    yan_xuan = page.locator("//em[@class='ntes-nav-entry-lofter']")
    option = page.locator("//ul[@id='js_lofter_pop_url']/li")
    page.goto("https://www.163.com/")
    yan_xuan.hover()
    for i in range(option.count()):
        option_attr = option.nth(i).locator("//a/span")
        text = option_attr.inner_text()
        spec_char = ["!","~","#","$"]
        for char in text:
            assert char not in spec_char,f"option{i} has special character, its text is {text}"

def test_assert_spec_char2(page:Page):
    yan_xuan = page.locator("//em[@class='ntes-nav-entry-lofter']")
    option = page.locator("//ul[@id='js_lofter_pop_url']/li")
    page.goto("https://www.163.com/")
    yan_xuan.hover()
    for i in range(option.count()):
        option_attr = option.nth(i).locator("//a/span")
        text = option_attr.inner_text()
        normal_char = r'^[0-9a-zA-Z人价新特]*$'
        assert re.match(normal_char,text),f"option{i} has special character, its text is {text}"