#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup
import time
from typing import Optional

try:
    from .config import Config  # For relative import within package
    from .logger import ScraperLogger
except ImportError:
    from config import Config   # Fallback for direct execution
    from logger import ScraperLogger

class WebScraper:
    def __init__(self, url: str, config_file: Optional[str] = None):
        self.url = url
        self.config = Config(config_file)

        # Setup logger using the new ScraperLogger class
        logger_manager = ScraperLogger(f"{__name__}_{id(self)}", self.config)
        self.logger = logger_manager.get_logger()

    def check_website(self):
        """Check website with retry logic and configurable timeout"""
        timeout = self.config.fetch_config_value('scraping', 'timeout', 10)
        max_retries = self.config.fetch_config_value('scraping', 'max_retries', 3)
        retry_delay = self.config.fetch_config_value('scraping', 'retry_delay', 1)

        self.logger.info(f"Starting scraping for URL: {self.url}")

        for attempt in range(max_retries):
            try:
                self.logger.debug(f"Attempt {attempt + 1}/{max_retries}")

                response = requests.get(self.url, timeout=timeout)
                response.raise_for_status()  # Raise an error for HTTP errors

                soup = BeautifulSoup(response.text, 'html.parser')

                # Perform scraping logic here
                if soup.title and soup.title.string:
                    title = soup.title.string.strip()
                    self.logger.info(f"Website title found: {title}")
                    return title
                else:
                    self.logger.warning("No title found on the page")
                    return None

            except requests.Timeout:
                self.logger.warning(f"Timeout on attempt {attempt + 1}")
            except requests.ConnectionError:
                self.logger.warning(f"Connection error on attempt {attempt + 1}")
            except requests.HTTPError as e:
                self.logger.warning(f"HTTP error on attempt {attempt + 1}: {e}")
            except requests.RequestException as e:
                self.logger.warning(f"Request error on attempt {attempt + 1}: {e}")

            # Wait before next attempt (if not the last attempt)
            if attempt < max_retries - 1:
                self.logger.info(f"Retrying in {retry_delay} seconds...")
                import time
                time.sleep(retry_delay)

        # All attempts failed
        self.logger.error(f"Failed to scrape after {max_retries} attempts")
        return None

if __name__ == "__main__":
    scraper = WebScraper("https://example.com")
    title = scraper.check_website()
    testconfig = Config()
    print(testconfig.fetch_config_value('loging', 'file_path'))
    print(testconfig.get_section('logging'))
    if title:
        print(f"Website title is: {title}")
    else:
        print("Failed to retrieve website title.")