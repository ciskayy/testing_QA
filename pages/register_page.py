from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pages.base_page import BasePage


class RegisterPage(BasePage):
    URL = "https://demoqa.com/register"

    FIRST_NAME = (By.ID, "firstname")
    LAST_NAME = (By.ID, "lastname")
    USERNAME = (By.ID, "userName")
    PASSWORD = (By.ID, "password")
    REGISTER_BUTTON = (By.ID, "register")
    MESSAGE = (By.ID, "name")

    def navigate(self):
        self.open(self.URL)

    def register(self, first_name, last_name, username, password):
        self.navigate()

        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)

        button = self.find(self.REGISTER_BUTTON)

        # Scroll tombol ke tengah layar agar tidak ketutup footer
        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )

        # Klik pakai JavaScript supaya tidak kena element click intercepted
        self.driver.execute_script("arguments[0].click();", button)

    def get_message(self):
        try:
            return self.wait.until(
                EC.visibility_of_element_located(self.MESSAGE)
            ).text
        except TimeoutException:
            return ""

    def get_alert_text_if_exists(self):
        try:
            alert = self.wait.until(EC.alert_is_present())
            alert_text = alert.text
            alert.accept()
            return alert_text
        except TimeoutException:
            return ""

    def is_field_invalid(self, locator):
        try:
            element = self.find(locator)
            class_value = element.get_attribute("class")
            validation_message = element.get_attribute("validationMessage")

            return (
                "is-invalid" in class_value
                or validation_message != ""
            )
        except Exception:
            return False

    def has_invalid_field(self):
        return (
            self.is_field_invalid(self.FIRST_NAME)
            or self.is_field_invalid(self.LAST_NAME)
            or self.is_field_invalid(self.USERNAME)
            or self.is_field_invalid(self.PASSWORD)
        )