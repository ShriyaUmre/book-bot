import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# This is a Fixture - A VERY important interview topic.
# It sets up and tears down the driver for each test.
@pytest.fixture
def browser():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    yield driver  # This is where the test runs
    driver.quit() # This runs after the test is done

# Test Case 1: Does the page title contain "Books"?
def test_page_title(browser):
    browser.get("http://books.toscrape.com/")
    assert "Books" in browser.title

# Test Case 2: Can we navigate to the Travel category?
def test_travel_category_exists(browser):
    browser.get("http://books.toscrape.com/")
    travel_link = browser.find_element(By.CSS_SELECTOR, 'a[href="catalogue/category/books/travel_2/index.html"]')
    assert travel_link.is_displayed()
    travel_link.click()
    # Now assert that we are on the travel page
    assert "travel" in browser.current_url.lower()

# Run this with `pytest test_book_bot.py -v` in the terminal