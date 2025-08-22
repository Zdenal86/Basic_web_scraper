#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

import logging
from datetime import datetime
import os

class WebScraper:
    def __init__(self, url):
        self.url = url
        self.setup_logging()

    def setup_logging(self):
        """Setup logging to file"""
        os.makedirs(os.path.dirname('logs/scraper.log'), exist_ok=True)

        # Create custom logger for this instance
        self.logger = logging.getLogger(f"{__name__}_{id(self)}")
        self.logger.setLevel(logging.INFO)

        # Check if handler already exists (to avoid duplicates)
        if not self.logger.handlers:
            # File handler - logging to file
            file_handler = logging.FileHandler('logs/scraper.log', encoding='utf-8')
            file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)

            # Console handler - logging to console
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter('%(levelname)s - %(message)s')
            console_handler.setFormatter(console_formatter)

            # Add both handlers to logger
            self.logger.addHandler(file_handler)
            self.logger.addHandler(console_handler)

    def check_website(self):
        self.logger.info(f"Starting scraping for URL: {self.url}")
        try:
            response = requests.get(self.url)
            response.raise_for_status()  # Raise an error for HTTP errors
            soup = BeautifulSoup(response.text, 'html.parser')
            # Perform your scraping logic here
            if soup.title and soup.title.string:
                self.logger.info(f"Website title found: {soup.title.string}")
                return soup.title.string  # Example: return the website title
            else:
                self.logger.warning("No title found on the page")
                return None
        except requests.RequestException as e:
            self.logger.error(f"Error checking website: {e}")
            return None

def main():
    webscraper = WebScraper("https://quotes.torape.com/")
    title = webscraper.check_website()
    if title:
        print(f"Website title: {title}")
    else:
        print("Failed to scrape website")

if __name__ == "__main__":
    main()