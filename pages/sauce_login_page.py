from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class SauceLoginPage(BasePage):
    URL = "https://www.saucedemo.com"

    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    INVENTORY_CONTAINER = (By.ID, "inventory_container")

    def navigate(self):
        self.open(self.URL)

    def login(self, username, password):
        self.navigate()
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def is_login_successful(self):
        return self.is_visible(self.INVENTORY_CONTAINER)

    def is_login_failed(self):
        return self.is_visible(self.ERROR_MESSAGE)

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)