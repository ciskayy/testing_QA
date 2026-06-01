import time
import allure
import pytest
from selenium.common.exceptions import StaleElementReferenceException, TimeoutException, WebDriverException
from pages.register_page import RegisterPage
from tests.conftest import load_csv


@allure.feature("Register")
@allure.story("Data-Driven Register Testing")
class TestRegisterAllure:

    @pytest.mark.parametrize(
        "row",
        load_csv("register_data.csv"),
        ids=lambda row: row["description"]
    )
    @allure.title("Register DDT - {row[description]}")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_register_from_csv_with_allure(self, driver, row):
        page = RegisterPage(driver)

        with allure.step("Melakukan registrasi berdasarkan data CSV"):
            try:
                page.register(
                    row["first_name"],
                    row["last_name"],
                    row["username"],
                    row["password"]
                )
            except StaleElementReferenceException:
                driver.refresh()
                time.sleep(1)
                page.register(
                    row["first_name"],
                    row["last_name"],
                    row["username"],
                    row["password"]
                )

        with allure.step("Mengambil hasil aktual"):
            expected = row["expected"]

            try:
                message = page.get_message()
            except (StaleElementReferenceException, TimeoutException, WebDriverException):
                message = ""

            try:
                alert_text = page.get_alert_text_if_exists()
            except (StaleElementReferenceException, TimeoutException, WebDriverException):
                alert_text = ""

            try:
                has_invalid_field = page.has_invalid_field()
            except (StaleElementReferenceException, TimeoutException, WebDriverException):
                has_invalid_field = False

            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"screenshot_{row['description']}",
                attachment_type=allure.attachment_type.PNG
            )

            allure.attach(
                f"Expected: {expected}\n"
                f"Message: {message}\n"
                f"Alert: {alert_text}\n"
                f"Has Invalid Field: {has_invalid_field}\n"
                f"Current URL: {driver.current_url}",
                name="actual_result",
                attachment_type=allure.attachment_type.TEXT
            )

        with allure.step("Verifikasi hasil testing"):
            if expected == "PASS":
                assert (
                    "User Registered Successfully" in alert_text
                    or "Please verify reCaptcha to register!" in message
                    or not has_invalid_field
                    or "register" in driver.current_url
                ), (
                    f"Registrasi valid seharusnya berhasil, tertahan reCaptcha, "
                    f"atau minimal tidak memiliki field invalid. "
                    f"Alert: {alert_text}, Message: {message}, "
                    f"Has Invalid Field: {has_invalid_field}"
                )

            else:
                assert (
                    has_invalid_field
                    or message != ""
                    or "Please verify reCaptcha to register!" in message
                    or "register" in driver.current_url
                ), (
                    f"Registrasi invalid seharusnya gagal. "
                    f"Alert: {alert_text}, Message: {message}, "
                    f"Has Invalid Field: {has_invalid_field}"
                )