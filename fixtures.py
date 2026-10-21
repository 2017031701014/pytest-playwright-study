from playwright.sync_api import Page

from swag.login import Login
from swag.product import Product
from swag.your_cart import YourCart


import pytest

@pytest.fixture
def login(page:Page) -> Login:
    return Login(page)

@pytest.fixture
def product(page:Page) -> Product:
    return Product(page)

@pytest.fixture
def yc(page:Page) -> YourCart:
    return YourCart(page)