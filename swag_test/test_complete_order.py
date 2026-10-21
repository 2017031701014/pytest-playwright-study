import allure
import pytest

@pytest.mark.test_id("FTM-101016")
def test_swag_page(data,login,product,yc):
    account = data["user_name"]
    password = data["password"]
    # 取前两行的写法
    product_data = data.loc[0:1,"product"].to_list()
    with allure.step("login"):
        login.login(account[0],password[0])
    with allure.step("add product"):
        product.add_products_to_cart(product_data,0)
    with allure.step("enter your cart and validate product"):
        product.click_shopping_cart()
        yc.validate_product_list(product_data)
