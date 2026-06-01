from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class MenuPage(BasePage):
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    LOGIN_BUTTON = (By.ID, "login-button")

    def logout(self):
        self.js_click(self.MENU_BUTTON)
        self.wait.until(EC.visibility_of_element_located(self.LOGOUT_LINK))
        self.js_click(self.LOGOUT_LINK)
        self.wait.until(EC.url_contains("saucedemo.com"))

    def is_on_login_page(self):
        return self.is_visible(self.LOGIN_BUTTON)