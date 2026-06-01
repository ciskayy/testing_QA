from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pages.base_page import BasePage
import time


class CheckoutPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")

    CONTINUE_BUTTON = (By.ID, "continue")
    FINISH_BUTTON = (By.ID, "finish")

    SUCCESS_MESSAGE = (By.CLASS_NAME, "complete-header")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    SUMMARY_SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")

    def fill_checkout_info(self, first_name, last_name, postal_code):
        self.wait.until(EC.url_contains("checkout-step-one"))

        first_input = self.find_visible(self.FIRST_NAME)
        first_input.clear()
        if first_name:
            first_input.send_keys(first_name)

        last_input = self.find_visible(self.LAST_NAME)
        last_input.clear()
        if last_name:
            last_input.send_keys(last_name)

        postal_input = self.find_visible(self.POSTAL_CODE)
        postal_input.clear()
        if postal_code:
            postal_input.send_keys(postal_code)

        time.sleep(0.5)

    def click_continue(self):
        self.wait.until(EC.url_contains("checkout-step-one"))

        button = self.wait.until(
            EC.element_to_be_clickable(self.CONTINUE_BUTTON)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )

        try:
            ActionChains(self.driver).move_to_element(button).click().perform()
        except:
            try:
                button.click()
            except:
                self.driver.execute_script("arguments[0].click();", button)

        time.sleep(1)

    def click_finish(self):
        self.wait.until(EC.url_contains("checkout-step-two"))

        button = self.wait.until(
            EC.element_to_be_clickable(self.FINISH_BUTTON)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )

        try:
            ActionChains(self.driver).move_to_element(button).click().perform()
        except:
            try:
                button.click()
            except:
                self.driver.execute_script("arguments[0].click();", button)

        self.wait.until(EC.url_contains("checkout-complete"))

    def is_order_successful(self):
        return self.is_visible(self.SUCCESS_MESSAGE)

    def get_success_message(self):
        return self.get_text(self.SUCCESS_MESSAGE)

    def is_error_visible(self):
        try:
            error_elements = self.driver.find_elements(*self.ERROR_MESSAGE)
            return len(error_elements) > 0 and error_elements[0].is_displayed()
        except:
            return False

    def get_error_message(self):
        return self.get_text(self.ERROR_MESSAGE)

    def get_item_total_from_products(self):
        self.wait.until(EC.url_contains("checkout-step-two"))
        self.wait.until(EC.presence_of_all_elements_located(self.ITEM_PRICES))

        price_elements = self.driver.find_elements(*self.ITEM_PRICES)
        total = 0

        for element in price_elements:
            total += float(element.text.replace("$", ""))

        return total

    def get_summary_subtotal(self):
        self.wait.until(EC.url_contains("checkout-step-two"))

        subtotal_text = self.get_text(self.SUMMARY_SUBTOTAL)
        subtotal_value = subtotal_text.replace("Item total: $", "")

        return float(subtotal_value)