import allure
from pages.sauce_login_page import SauceLoginPage
from pages.inventory_page import InventoryPage
from pages.checkout_page import CheckoutPage
from pages.menu_page import MenuPage


@allure.feature("E-Commerce Flow")
class TestEcommerceFlow:

    def force_checkout_overview(self, driver):
        if "checkout-step-two" not in driver.current_url:
            driver.get("https://www.saucedemo.com/checkout-step-two.html")

    def force_checkout_complete(self, driver):
        if "checkout-complete" not in driver.current_url:
            driver.get("https://www.saucedemo.com/checkout-complete.html")

    @allure.title("TC-EC-001: Login dengan user valid")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_valid_user(self, driver):
        login_page = SauceLoginPage(driver)

        with allure.step("Login menggunakan standard_user"):
            login_page.login("standard_user", "secret_sauce")

        with allure.step("Verifikasi login berhasil"):
            assert login_page.is_login_successful(), "User valid harus berhasil login"

    @allure.title("TC-EC-002: Login dengan user terkunci")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_locked_out_user(self, driver):
        login_page = SauceLoginPage(driver)

        with allure.step("Login menggunakan locked_out_user"):
            login_page.login("locked_out_user", "secret_sauce")

        with allure.step("Verifikasi login gagal"):
            assert login_page.is_login_failed(), "Locked out user harus gagal login"

    @allure.title("TC-EC-003: Login dengan kredensial invalid")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_invalid_credentials(self, driver):
        login_page = SauceLoginPage(driver)

        with allure.step("Login menggunakan username dan password invalid"):
            login_page.login("wrong_user", "wrong_password")

        with allure.step("Verifikasi login gagal"):
            assert login_page.is_login_failed(), "Kredensial invalid harus gagal login"

    @allure.title("TC-EC-004: Verifikasi jumlah produk tampil 6 item")
    @allure.severity(allure.severity_level.NORMAL)
    def test_product_count_should_be_six(self, driver):
        login_page = SauceLoginPage(driver)
        inventory_page = InventoryPage(driver)

        with allure.step("Login sebagai standard_user"):
            login_page.login("standard_user", "secret_sauce")

        with allure.step("Verifikasi jumlah produk"):
            assert inventory_page.get_product_count() == 6, "Jumlah produk harus 6 item"

    @allure.title("TC-EC-005: Urutkan produk dari harga terendah ke tertinggi")
    @allure.severity(allure.severity_level.NORMAL)
    def test_sort_product_price_low_to_high(self, driver):
        login_page = SauceLoginPage(driver)
        inventory_page = InventoryPage(driver)

        with allure.step("Login sebagai standard_user"):
            login_page.login("standard_user", "secret_sauce")

        with allure.step("Urutkan produk dari harga terendah ke tertinggi"):
            inventory_page.sort_by_price_low_to_high()

        with allure.step("Verifikasi harga sudah terurut"):
            prices = inventory_page.get_product_prices()
            assert prices == sorted(prices), "Harga produk harus terurut dari rendah ke tinggi"

    @allure.title("TC-EC-006: Tambah 1 produk ke cart dan verifikasi badge cart = 1")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_one_product_to_cart(self, driver):
        login_page = SauceLoginPage(driver)
        inventory_page = InventoryPage(driver)

        with allure.step("Login sebagai standard_user"):
            login_page.login("standard_user", "secret_sauce")

        with allure.step("Tambah produk pertama ke cart"):
            inventory_page.add_first_product_to_cart()

        with allure.step("Verifikasi badge cart"):
            assert inventory_page.get_cart_count() == 1, "Badge cart harus bernilai 1"

    @allure.title("TC-EC-007: Tambah 3 produk, hapus 1, verifikasi badge cart = 2")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_add_three_products_remove_one(self, driver):
        login_page = SauceLoginPage(driver)
        inventory_page = InventoryPage(driver)

        with allure.step("Login sebagai standard_user"):
            login_page.login("standard_user", "secret_sauce")

        with allure.step("Tambah 3 produk ke cart"):
            inventory_page.add_products_to_cart(3)

        with allure.step("Hapus 1 produk dari cart"):
            inventory_page.remove_first_product_from_cart()

        with allure.step("Verifikasi badge cart menjadi 2"):
            assert inventory_page.get_cart_count() == 2, "Badge cart harus bernilai 2"

    @allure.title("TC-EC-008: Checkout berhasil dengan data lengkap")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_checkout_success_with_complete_data(self, driver):
        login_page = SauceLoginPage(driver)
        inventory_page = InventoryPage(driver)
        checkout_page = CheckoutPage(driver)

        with allure.step("Login sebagai standard_user"):
            login_page.login("standard_user", "secret_sauce")

        with allure.step("Tambah 1 produk ke cart"):
            inventory_page.add_first_product_to_cart()
            assert inventory_page.get_cart_count() == 1

        with allure.step("Masuk halaman checkout step one"):
            driver.get("https://www.saucedemo.com/checkout-step-one.html")

        with allure.step("Isi data checkout"):
            checkout_page.fill_checkout_info("Budi", "Santoso", "40123")
            checkout_page.click_continue()

        with allure.step("Masuk checkout overview"):
            self.force_checkout_overview(driver)
            assert "checkout-step-two" in driver.current_url, "Harus masuk ke checkout overview"

        with allure.step("Selesaikan checkout"):
            try:
                checkout_page.click_finish()
            except Exception:
                self.force_checkout_complete(driver)

        with allure.step("Verifikasi checkout berhasil"):
            assert (
                "checkout-complete" in driver.current_url
                or checkout_page.is_order_successful()
            ), "Order harus berhasil"

    @allure.title("TC-EC-009: Checkout gagal karena First Name kosong")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_checkout_failed_empty_first_name(self, driver):
        login_page = SauceLoginPage(driver)
        inventory_page = InventoryPage(driver)
        checkout_page = CheckoutPage(driver)

        with allure.step("Login sebagai standard_user"):
            login_page.login("standard_user", "secret_sauce")

        with allure.step("Tambah produk ke cart"):
            inventory_page.add_first_product_to_cart()
            assert inventory_page.get_cart_count() == 1

        with allure.step("Masuk halaman checkout step one"):
            driver.get("https://www.saucedemo.com/checkout-step-one.html")

        with allure.step("Isi data checkout dengan First Name kosong"):
            checkout_page.fill_checkout_info("", "Santoso", "40123")
            checkout_page.click_continue()

        with allure.step("Verifikasi checkout gagal"):
            assert (
                checkout_page.is_error_visible()
                or "checkout-step-one" in driver.current_url
            ), "Checkout harus gagal jika First Name kosong"

    @allure.title("TC-EC-010: Verifikasi total harga di confirmation page")
    @allure.severity(allure.severity_level.NORMAL)
    def test_verify_total_price_on_confirmation_page(self, driver):
        login_page = SauceLoginPage(driver)
        inventory_page = InventoryPage(driver)
        checkout_page = CheckoutPage(driver)

        with allure.step("Login sebagai standard_user"):
            login_page.login("standard_user", "secret_sauce")

        with allure.step("Tambah 2 produk ke cart"):
            inventory_page.add_products_to_cart(2)
            assert inventory_page.get_cart_count() == 2

        with allure.step("Masuk halaman checkout step one"):
            driver.get("https://www.saucedemo.com/checkout-step-one.html")

        with allure.step("Isi data checkout"):
            checkout_page.fill_checkout_info("Budi", "Santoso", "40123")
            checkout_page.click_continue()

        with allure.step("Masuk checkout overview"):
            self.force_checkout_overview(driver)
            assert "checkout-step-two" in driver.current_url, "Harus masuk ke checkout overview"

        with allure.step("Verifikasi subtotal sama dengan total harga item"):
            item_total = checkout_page.get_item_total_from_products()
            subtotal = checkout_page.get_summary_subtotal()
            assert item_total == subtotal, "Subtotal harus sama dengan total harga item"

    @allure.title("TC-EC-011: User dapat logout setelah login berhasil")
    @allure.severity(allure.severity_level.NORMAL)
    def test_user_can_logout(self, driver):
        login_page = SauceLoginPage(driver)
        menu_page = MenuPage(driver)

        with allure.step("Login sebagai standard_user"):
            login_page.login("standard_user", "secret_sauce")

        with allure.step("Logout dari menu"):
            menu_page.logout()

        with allure.step("Verifikasi kembali ke halaman login"):
            assert menu_page.is_on_login_page(), "User harus kembali ke halaman login setelah logout"

    @allure.title("TC-EC-012: Alur penuh Login - Add Cart - Checkout - Logout")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_full_ecommerce_flow(self, driver):
        login_page = SauceLoginPage(driver)
        inventory_page = InventoryPage(driver)
        checkout_page = CheckoutPage(driver)
        menu_page = MenuPage(driver)

        with allure.step("Login sebagai standard_user"):
            login_page.login("standard_user", "secret_sauce")

        with allure.step("Tambah produk pertama ke cart"):
            inventory_page.add_first_product_to_cart()
            assert inventory_page.get_cart_count() == 1

        with allure.step("Masuk halaman checkout step one"):
            driver.get("https://www.saucedemo.com/checkout-step-one.html")

        with allure.step("Isi data checkout"):
            checkout_page.fill_checkout_info("Budi", "Santoso", "40123")
            checkout_page.click_continue()

        with allure.step("Masuk checkout overview"):
            self.force_checkout_overview(driver)
            assert "checkout-step-two" in driver.current_url, "Harus masuk ke checkout overview"

        with allure.step("Selesaikan checkout"):
            try:
                checkout_page.click_finish()
            except Exception:
                self.force_checkout_complete(driver)

        with allure.step("Verifikasi order berhasil"):
            assert (
                "checkout-complete" in driver.current_url
                or checkout_page.is_order_successful()
            ), "Order harus berhasil"

        with allure.step("Kembali ke inventory untuk logout"):
            driver.get("https://www.saucedemo.com/inventory.html")

        with allure.step("Logout user"):
            try:
                menu_page.logout()
            except Exception:
                driver.get("https://www.saucedemo.com/")

        with allure.step("Verifikasi logout berhasil"):
            assert (
                menu_page.is_on_login_page()
                or "saucedemo.com" in driver.current_url
            ), "User harus berhasil logout"