from playwright.sync_api import Page
from collections import Counter

class YourCartPage:
    def __init__(self, page: Page):
        self.page = page
        self.product_names =page.locator("div.inventory_item_name")


class YourCart(YourCartPage):
    def validate_product_list(self,product_list:list):
        """
        校验页面上显示的所有商品是否与传入的列表一致（忽略顺序）
        """
        # all_inner_texts() 返回的是一个 纯 Python 列表（list），里面装的是页面上匹配到的所有元素的可见文本字符串（str）
        actual_products = self.product_names.all_inner_texts()
        assert Counter(actual_products) == Counter(product_list), (
            f"\n商品列表与预期不符！\n预期: {product_list}\n实际: {actual_products}"
        )