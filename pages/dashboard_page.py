# pages/dashboard_page.py

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class DashboardPage(BasePage):
    LOGOUT_BTN = (By.CSS_SELECTOR, "a.button.secondary.radius")
    SUCCESS_MSG = (By.CSS_SELECTOR, ".flash.success")

    def is_on_dashboard(self):
        return self.is_visible(self.LOGOUT_BTN)

    def logout(self):
        self.click(self.LOGOUT_BTN)