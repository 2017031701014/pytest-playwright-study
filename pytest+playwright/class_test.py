import time

from playwright.sync_api import Page

class TestClass:
    def test1(self,page:Page):
        page.evaluate('location.href="https://www.1688.com/"')
        time.sleep(1)

