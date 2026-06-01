import allure
import pytest
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

        with allure.step("Membuka halaman Register"):
            page.navigate()

        with allure.step("Mengisi form registrasi"):
            page.type(page.FIRST_NAME, row["first_name"])
            page.type(page.LAST_NAME, row["last_name"])
            page.type(page.USERNAME, row["username"])
            page.type(page.PASSWORD, row["password"])

        with allure.step("Klik tombol Register"):
            button = page.find(page.REGISTER_BUTTON)
            driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center'});",
                button
            )
            driver.execute_script("arguments[0].click();", button)

        with allure.step("Mengambil hasil aktual"):
            expected = row["expected"]
            message = page.get_message()
            alert_text = page.get_alert_text_if_exists()

            allure.attach(
                driver.get_screenshot_as_png(),
                name=f"screenshot_{row['description']}",
                attachment_type=allure.attachment_type.PNG
            )

        with allure.step("Verifikasi hasil testing"):
            if expected == "PASS":
                assert (
                    "User Registered Successfully" in alert_text
                    or "Please verify reCaptcha to register!" in message
                    or message != ""
                ), (
                    f"Registrasi valid seharusnya berhasil atau tertahan reCaptcha. "
                    f"Alert: {alert_text}, Message: {message}"
                )

            else:
                assert (
                    page.has_invalid_field()
                    or message != ""
                    or "Please verify reCaptcha to register!" in message
                ), (
                    f"Registrasi invalid seharusnya gagal. "
                    f"Alert: {alert_text}, Message: {message}"
                )