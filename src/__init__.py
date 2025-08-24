"""
Basic Web Scraper Package

A simple web scraping tool with logging capabilities.
"""

from .scraper import WebScraper
from .logger import ScraperLogger
from .config import Config

__version__ = "1.0.0"
__author__ = "Zdeněk Amler"
__all__ = ["WebScraper", "ScraperLogger", "Config"]

__all__ = ["WebScraper"]
