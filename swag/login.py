import pytest
from playwright.sync_api import Page

def login(account,password):
    pass

@pytest.mark.test_id("FTM-101016")
def test_swag_page(page:Page,data):
    page.goto("https://www.saucedemo.com/")