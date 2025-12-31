"""
Real-Time Quotes Scraper using Selenium
Website: quotes.toscrape.com (No login required)
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json


class QuotesScraper:
    def __init__(self, headless=False):
        """Initialize the Chrome driver with options"""
        chrome_options = Options()

        if headless:
            chrome_options.add_argument('--headless')

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument(
            '--disable-blink-features=AutomationControlled')
        chrome_options.add_argument(
            'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=chrome_options
        )
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 10)

    def scrape_quotes(self, num_pages=3):
        """Scrape quotes from multiple pages"""
        all_quotes = []
        base_url = "https://quotes.toscrape.com"

        try:
            print(f"\n{'='*60}")
            print("Starting Quotes Scraper")
            print(f"{'='*60}\n")

            for page in range(1, num_pages + 1):
                url = f"{base_url}/page/{page}/"
                print(f"📄 Scraping page {page}: {url}")

                self.driver.get(url)
                time.sleep(2)

                # Wait for quotes to load
                self.wait.until(
                    EC.presence_of_all_elements_located(
                        (By.CLASS_NAME, "quote"))
                )

                # Find all quote elements
                quotes = self.driver.find_elements(By.CLASS_NAME, "quote")

                for idx, quote in enumerate(quotes, 1):
                    try:
                        text = quote.find_element(By.CLASS_NAME, "text").text
                        author = quote.find_element(
                            By.CLASS_NAME, "author").text
                        tags = [tag.text for tag in quote.find_elements(
                            By.CLASS_NAME, "tag")]

                        quote_data = {
                            "quote": text,
                            "author": author,
                            "tags": tags,
                            "page": page
                        }

                        all_quotes.append(quote_data)

                        print(f"\n  Quote #{idx}:")
                        print(f"  Text: {text}")
                        print(f"  Author: {author}")
                        print(f"  Tags: {', '.join(tags)}")

                    except Exception as e:
                        print(f"  ⚠️  Error extracting quote: {e}")

                print(
                    f"\n✅ Page {page} completed - {len(quotes)} quotes extracted")

            return all_quotes

        except Exception as e:
            print(f"\n❌ Error during scraping: {e}")
            return all_quotes

    def scrape_author_details(self, author_name):
        """Scrape detailed information about a specific author"""
        try:
            print(f"\n{'='*60}")
            print(f"Fetching details for author: {author_name}")
            print(f"{'='*60}\n")

            # Go to main page first
            self.driver.get("https://quotes.toscrape.com")
            time.sleep(1)

            # Find and click on the author link
            author_links = self.driver.find_elements(By.CLASS_NAME, "author")

            for link in author_links:
                if link.text == author_name:
                    # Find the "about" link next to this author
                    parent = link.find_element(By.XPATH, "..")
                    about_link = parent.find_element(By.LINK_TEXT, "(about)")
                    about_link.click()
                    break

            time.sleep(2)

            # Extract author details
            author_info = {}
            author_info['name'] = self.driver.find_element(
                By.CLASS_NAME, "author-title").text
            author_info['born'] = self.driver.find_element(
                By.CLASS_NAME, "author-born-date").text
            author_info['location'] = self.driver.find_element(
                By.CLASS_NAME, "author-born-location").text
            author_info['description'] = self.driver.find_element(
                By.CLASS_NAME, "author-description").text

            print(f"Name: {author_info['name']}")
            print(f"Born: {author_info['born']}")
            print(f"Location: {author_info['location']}")
            print(f"Description: {author_info['description'][:200]}...")

            return author_info

        except Exception as e:
            print(f"❌ Error fetching author details: {e}")
            return None

    def filter_quotes_by_tag(self, tag_name):
        """Filter and scrape quotes by specific tag"""
        try:
            url = f"https://quotes.toscrape.com/tag/{tag_name}/"
            print(f"\n{'='*60}")
            print(f"Filtering quotes by tag: '{tag_name}'")
            print(f"URL: {url}")
            print(f"{'='*60}\n")

            self.driver.get(url)
            time.sleep(2)

            quotes = self.driver.find_elements(By.CLASS_NAME, "quote")
            filtered_quotes = []

            for idx, quote in enumerate(quotes, 1):
                text = quote.find_element(By.CLASS_NAME, "text").text
                author = quote.find_element(By.CLASS_NAME, "author").text

                quote_data = {
                    "quote": text,
                    "author": author,
                    "tag": tag_name
                }

                filtered_quotes.append(quote_data)
                print(f"Quote #{idx}: {text}")
                print(f"Author: {author}\n")

            print(
                f"✅ Found {len(filtered_quotes)} quotes with tag '{tag_name}'")
            return filtered_quotes

        except Exception as e:
            print(f"❌ Error filtering by tag: {e}")
            return []

    def save_to_json(self, data, filename="quotes_data.json"):
        """Save scraped data to JSON file"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print(f"\n💾 Data saved to {filename}")
        except Exception as e:
            print(f"❌ Error saving to JSON: {e}")

    def close(self):
        """Close the browser"""
        if self.driver:
            self.driver.quit()
            print("\n🔒 Browser closed successfully")


def main():
    """Main execution function"""
    scraper = None

    try:
        # Initialize scraper (set headless=True to run without browser window)
        scraper = QuotesScraper(headless=False)

        # Example 1: Scrape quotes from multiple pages
        quotes = scraper.scrape_quotes(num_pages=2)

        # Example 2: Get details about a specific author
        if quotes:
            first_author = quotes[0]['author']
            scraper.scrape_author_details(first_author)

        # Example 3: Filter quotes by tag
        scraper.filter_quotes_by_tag("inspirational")

        # Example 4: Save all data to JSON
        scraper.save_to_json(quotes)

        print(f"\n{'='*60}")
        print(f"✨ Scraping completed! Total quotes: {len(quotes)}")
        print(f"{'='*60}\n")

    except Exception as e:
        print(f"\n❌ Fatal error: {e}")

    finally:
        if scraper:
            scraper.close()


if __name__ == "__main__":
    main()
