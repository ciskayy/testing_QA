import csv
import os
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture(scope="function")
def driver():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")

    if os.getenv("CI"):
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def login_page(driver):
    from pages.login_page import LoginPage
    return LoginPage(driver)


@pytest.fixture(scope="function")
def dashboard_page(driver):
    from pages.dashboard_page import DashboardPage
    return DashboardPage(driver)


def load_csv(filename):
    filepath = os.path.join("data", filename)

    with open(filepath, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        driver = item.funcargs.get("driver")

        if driver:
            os.makedirs("reports/screenshots", exist_ok=True)

            screenshot_name = (
                item.nodeid
                .replace("/", "_")
                .replace("\\", "_")
                .replace("::", "_")
                .replace("[", "_")
                .replace("]", "_")
                .replace(" ", "_")
            )

            screenshot_path = f"reports/screenshots/{screenshot_name}.png"
            driver.save_screenshot(screenshot_path)
            print(f"\nScreenshot disimpan: {screenshot_path}")