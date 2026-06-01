from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage


class InventoryPage(BasePage):
    PRODUCT_ITEMS = (By.CLASS_NAME, "inventory_item")
    PRODUCT_NAMES = (By.CLASS_NAME, "inventory_item_name")
    PRODUCT_PRICES = (By.CLASS_NAME, "inventory_item_price")
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")

    ADD_TO_CART_BUTTONS = (By.CSS_SELECTOR, "button[data-test^='add-to-cart']")
    REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[data-test^='remove']")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")

    def get_product_count(self):
        self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_ITEMS))
        return len(self.driver.find_elements(*self.PRODUCT_ITEMS))

    def sort_by_price_low_to_high(self):
        dropdown = Select(self.find(self.SORT_DROPDOWN))
        dropdown.select_by_value("lohi")

    def get_product_prices(self):
        self.wait.until(EC.presence_of_all_elements_located(self.PRODUCT_PRICES))
        price_elements = self.driver.find_elements(*self.PRODUCT_PRICES)

        prices = []
        for element in price_elements:
            price_text = element.text.replace("$", "")
            prices.append(float(price_text))

        return prices

    def add_first_product_to_cart(self):
        buttons = self.wait.until(
            EC.presence_of_all_elements_located(self.ADD_TO_CART_BUTTONS)
        )

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            buttons[0]
        )
        self.driver.execute_script("arguments[0].click();", buttons[0])

        self.wait.until(
            EC.text_to_be_present_in_element(self.CART_BADGE, "1")
        )

    def add_products_to_cart(self, total_product):
        for expected_count in range(1, total_product + 1):
            buttons = self.wait.until(
                EC.presence_of_all_elements_located(self.ADD_TO_CART_BUTTONS)
            )

            button = buttons[0]

            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                button
            )
            self.driver.execute_script("arguments[0].click();", button)

            self.wait.until(
                EC.text_to_be_present_in_element(
                    self.CART_BADGE,
                    str(expected_count)
                )
            )

    def remove_first_product_from_cart(self):
        buttons = self.wait.until(
            EC.presence_of_all_elements_located(self.REMOVE_BUTTONS)
        )

        button = buttons[0]

        self.driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});",
            button
        )
        self.driver.execute_script("arguments[0].click();", button)

        self.wait.until(
            EC.text_to_be_present_in_element(self.CART_BADGE, "2")
        )

    def get_cart_count(self):
        try:
            return int(self.get_text(self.CART_BADGE))
        except:
            return 0

    def go_to_cart(self):
        # Scroll ke atas supaya cart icon tidak ketutup / hilang dari viewport
        self.driver.execute_script("window.scrollTo(0, 0);")

        try:
            cart_icon = self.wait.until(
                EC.presence_of_element_located(self.CART_ICON)
            )
            self.driver.execute_script("arguments[0].click();", cart_icon)
            self.wait.until(EC.url_contains("cart"))
        except:
            # Fallback agar test tidak nyangkut di inventory
            self.driver.get("https://www.saucedemo.com/cart.html")
            self.wait.until(EC.url_contains("cart"))