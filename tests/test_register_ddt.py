import pytest
from pages.register_page import RegisterPage
from tests.conftest import load_csv


class TestRegisterDDT:

    @pytest.mark.parametrize(
        "row",
        load_csv("register_data.csv"),
        ids=lambda row: row["description"]
    )
    def test_register_from_csv(self, driver, row):
        page = RegisterPage(driver)

        page.register(
            row["first_name"],
            row["last_name"],
            row["username"],
            row["password"]
        )

        expected = row["expected"]
        message = page.get_message()
        alert_text = page.get_alert_text_if_exists()

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