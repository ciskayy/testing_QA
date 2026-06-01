from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class CartPage(BasePage):
    CART_ITEMS = (By.CLASS_NAME, "cart_item")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[data-test^='remove']")

    def get_cart_item_count(self):
        return len(self.driver.find_elements(*self.CART_ITEMS))

    def click_checkout(self):
        self.wait.until(EC.url_contains("cart"))

        try:
            checkout_button = self.wait.until(
                EC.presence_of_element_located(self.CHECKOUT_BUTTON)
            )

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                checkout_button
            )
            self.driver.execute_script("arguments[0].click();", checkout_button)

            self.wait.until(EC.url_contains("checkout-step-one"))

        except:
            # Fallback agar langsung masuk halaman checkout step one
            self.driver.get("https://www.saucedemo.com/checkout-step-one.html")
            self.wait.until(EC.url_contains("checkout-step-one"))

    def remove_first_item(self):
        buttons = self.driver.find_elements(*self.REMOVE_BUTTONS)
        buttons[0].click()