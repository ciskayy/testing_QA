from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, StaleElementReferenceException
from pages.base_page import BasePage
import time


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

        self.click_register_button()

    def click_register_button(self):
        for attempt in range(3):
            try:
                button = self.wait.until(
                    EC.presence_of_element_located(self.REGISTER_BUTTON)
                )

                self.driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});",
                    button
                )

                time.sleep(0.5)

                button = self.wait.until(
                    EC.presence_of_element_located(self.REGISTER_BUTTON)
                )

                self.driver.execute_script("arguments[0].click();", button)
                return

            except StaleElementReferenceException:
                time.sleep(1)

        button = self.wait.until(
            EC.presence_of_element_located(self.REGISTER_BUTTON)
        )
        self.driver.execute_script("arguments[0].click();", button)

    def get_message(self):
        try:
            message_element = self.wait.until(
                EC.visibility_of_element_located(self.MESSAGE)
            )
            return message_element.text
        except TimeoutException:
            return ""
        except StaleElementReferenceException:
            try:
                message_element = self.wait.until(
                    EC.visibility_of_element_located(self.MESSAGE)
                )
                return message_element.text
            except Exception:
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
            element = self.wait.until(
                EC.presence_of_element_located(locator)
            )

            class_value = element.get_attribute("class") or ""
            validation_message = element.get_attribute("validationMessage") or ""

            return (
                "is-invalid" in class_value
                or validation_message != ""
            )

        except StaleElementReferenceException:
            try:
                element = self.wait.until(
                    EC.presence_of_element_located(locator)
                )

                class_value = element.get_attribute("class") or ""
                validation_message = element.get_attribute("validationMessage") or ""

                return (
                    "is-invalid" in class_value
                    or validation_message != ""
                )
            except Exception:
                return False

        except Exception:
            return False

    def has_invalid_field(self):
        return (
            self.is_field_invalid(self.FIRST_NAME)
            or self.is_field_invalid(self.LAST_NAME)
            or self.is_field_invalid(self.USERNAME)
            or self.is_field_invalid(self.PASSWORD)
        )