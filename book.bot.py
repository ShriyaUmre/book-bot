from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import csv
import time

def setup_driver():
    """Sets up the Chrome driver automatically. Interviewers LOVE this."""
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.maximize_window()
    return driver

def test_book_scraper():
    """The main function that does everything."""
    driver = setup_driver()
    try:
        # 1. Navigate to the target website (We'll use Books to Scrape)
        driver.get("http://books.toscrape.com/")
        print("✅ Website opened successfully")

        # 2. Handle a pop-up (a common interview question)
        # This site doesn't have one, but let's pretend we waited for the page to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        print("✅ Page loaded completely")

        # 3. Find and click on a category (e.g., Travel)
        # We use a precise CSS selector - another key interview topic.
        travel_category_link = driver.find_element(By.CSS_SELECTOR, 'a[href="catalogue/category/books/travel_2/index.html"]')
        travel_category_link.click()
        print("✅ Clicked on 'Travel' category")

        # 4. Extract data from the page
        # Find all book elements
        book_elements = driver.find_elements(By.CSS_SELECTOR, 'article.product_pod')
        print(f"✅ Found {len(book_elements)} books")

        book_data = []
        # Loop through each book element to get its details
        for book in book_elements:
            title = book.find_element(By.CSS_SELECTOR, 'h3 a').get_attribute('title')
            price = book.find_element(By.CSS_SELECTOR, 'p.price_color').text
            # For a real project, you'd also get the link here.
            book_data.append({"Title": title, "Price": price})
            print(f"   - Extracted: {title} ({price})")

        # 5. Save the extracted data to a CSV file
        # This shows you can do more than just click buttons.
        with open('travel_books.csv', 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Title', 'Price']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(book_data)
        print("✅ Data saved to 'travel_books.csv'")

        # 6. (BONUS) Go to the next page - shows handling pagination
        # next_button = driver.find_element(By.CSS_SELECTOR, 'li.next a')
        # next_button.click()
        # print("Clicked next page")

    except Exception as e:
        print(f"❌ An error occurred: {e}")
    finally:
        # Always quit the driver, even if there's an error
        input("Press Enter to close the browser...") # This keeps the browser open so you can see the result
        driver.quit()
        print("✅ Browser closed.")

if __name__ == "__main__":
    test_book_scraper()