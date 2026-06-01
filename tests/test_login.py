# tests/test_login.py

class TestLogin:

    def test_user_can_logout_after_success_login(self, login_page, dashboard_page):
        login_page.login("tomsmith", "SuperSecretPassword!")

        assert dashboard_page.is_on_dashboard(), "User harus berada di dashboard setelah login"

        dashboard_page.logout()

        assert login_page.is_login_successful(), "User harus berhasil logout dan kembali ke halaman login"