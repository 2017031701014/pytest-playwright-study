from playwright.sync_api import Page,expect


class ProductPage:
    def __init__(self, page: Page):
        self.page = page
        self.shopping_cart = page.locator("a.shopping_cart_link")


class Product(ProductPage):
    def add_products_to_cart(self,prducts: list,shopping_cart_num:int = -1):
        shopping_cart = self.page.locator("span.shopping_cart_badge")
        current_num = 0 if shopping_cart.count() == 0 else int(shopping_cart.inner_text())
        if shopping_cart_num != -1:
            if shopping_cart_num > 0:
                assert current_num == shopping_cart_num,(
                    f"number is incorrect in shopping cart, expect to be{shopping_cart_num} but got {current_num}"
                )
            else:
                expect(shopping_cart).to_have_count(0)
        for product in prducts:
            product_id = "add-to-cart-" + product.lower().replace(" ", "-")
            add_btn = self.page.locator(f"#{product_id}")
            add_btn.click()
            add_num = int(shopping_cart.inner_text())
            assert add_num == current_num + 1,(
                f"number is incorrect in shopping cart, expect to be {current_num + 1} but got {add_num}"
            )
            current_num+=1

    def click_shopping_cart(self):
        self.shopping_cart.click()