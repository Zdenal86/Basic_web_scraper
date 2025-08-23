#!/usr/bin/env python3

import requests
from bs4 import BeautifulSoup

import logging
from datetime import datetime
import os
from typing import Optional

from .config import Config

class WebScraper:
    def __init__(self, url: str, config_file: Optional[str] = None):
        self.url = url
        self.config = Config(config_file)
        self.setup_logging()

    def setup_logging(self):
        """Setup logging to file using configuration"""
        # Load configuration values
        log_file = self.config.get('logging', 'file_path', 'logs/scraper.log')
        log_level = self.config.get('logging', 'level', 'INFO')
        console_output = self.config.get('logging', 'console_output', True)

        # Create logs directory
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Create custom logger for this instance
        self.logger = logging.getLogger(f"{__name__}_{id(self)}")
        self.logger.setLevel(getattr(logging, log_level))

        # Check if handler already exists (to avoid duplicates)
        if not self.logger.handlers:
            # File handler - logging to file
            file_handler = logging.FileHandler(log_file, encoding='utf-8')
            file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
            file_handler.setFormatter(file_formatter)

            # Add file handler
            self.logger.addHandler(file_handler)

            # Console handler - only if enabled in config
            if console_output:
                console_handler = logging.StreamHandler()
                console_formatter = logging.Formatter('%(levelname)s - %(message)s')
                console_handler.setFormatter(console_formatter)
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