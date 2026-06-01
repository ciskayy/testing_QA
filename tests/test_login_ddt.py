import pytest
from pages.login_page import LoginPage


LOGIN_DATA = [
    ("tomsmith", "SuperSecretPassword!", True, "valid_credentials"),
    ("tomsmith", "wrongpassword", False, "invalid_password"),
    ("wronguser", "SuperSecretPassword!", False, "invalid_username"),
    ("", "SuperSecretPassword!", False, "empty_username"),
    ("tomsmith", "", False, "empty_password"),
    ("", "", False, "both_empty"),
]


class TestLoginDDT:

    @pytest.mark.parametrize(
        "username, password, expected_success, test_id",
        LOGIN_DATA,
        ids=[data[3] for data in LOGIN_DATA]
    )
    def test_login(self, driver, username, password, expected_success, test_id):
        page = LoginPage(driver)
        page.login(username, password)

        if expected_success:
            assert page.is_login_successful(), f"[{test_id}] Login seharusnya BERHASIL"
        else:
            assert page.is_login_failed(), f"[{test_id}] Login seharusnya GAGAL"