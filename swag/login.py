from playwright.sync_api import Page,expect


class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.account = page.locator("input#user-name")
        self.password = page.locator("input#password")
        self.login_btn = page.locator("input#login-button")


class Login(LoginPage):
    def login(self,account,password):
        self.page.goto("https://www.saucedemo.com/")
        self.account.fill(account)
        self.password.fill(password)
        self.login_btn.click()
        title = self.page.locator("div.app_logo")
        expect(title).to_have_text("Swag Labs")

