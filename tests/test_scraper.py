#!/usr/bin/env python3

import pytest
import os
import logging
import requests
from unittest.mock import patch, Mock, MagicMock
import sys
import pathlib

# Add parent directory to path to import src modules
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from src import WebScraper


class TestWebScraper:
    """Test suite for WebScraper class"""

    def setup_method(self):
        """Setup before each test"""
        self.test_url = "https://example.com"
        self.scraper = WebScraper(self.test_url)

    def teardown_method(self):
        """Cleanup after each test"""
        # Remove test log files if they exist
        if os.path.exists('logs/scraper.log'):
            try:
                os.remove('logs/scraper.log')
            except:
                pass

    def _setup_test_config(self, monkeypatch, timeout=5, max_retries=1, retry_delay=0.1):
        """Helper method to setup predictable test configuration"""
        def mock_config_get(section, key, default):
            config_map = {
                ('scraping', 'timeout'): timeout,
                ('scraping', 'max_retries'): max_retries,
                ('scraping', 'retry_delay'): retry_delay,
                ('logging', 'level'): 'INFO',
                ('logging', 'console_output'): True,
                ('logging', 'file_path'): 'logs/scraper.log',
                ('logging', 'console_log_format'): '%(levelname)s - %(message)s',
                ('logging', 'file_log_format'): '%(asctime)s - %(levelname)s - %(message)s'
            }
            return config_map.get((section, key), default)

        monkeypatch.setattr(self.scraper.config, 'get', mock_config_get)
        return timeout, max_retries, retry_delay

    def test_webscraper_initialization(self):
        """Test WebScraper initialization"""
        assert self.scraper.url == self.test_url
        assert hasattr(self.scraper, 'logger')
        assert isinstance(self.scraper.logger, logging.Logger)

    def test_logger_has_correct_handlers(self):
        """Test that logger has both file and console handlers"""
        handlers = self.scraper.logger.handlers
        assert len(handlers) == 2

        # Check handler types
        handler_types = [type(handler).__name__ for handler in handlers]
        assert 'FileHandler' in handler_types
        assert 'StreamHandler' in handler_types

    def test_logger_level_is_info(self):
        """Test that logger level is set to INFO"""
        assert self.scraper.logger.level == logging.INFO

    def test_check_website_success(self, monkeypatch):
        """Test successful website checking"""
        timeout, max_retries, retry_delay = self._setup_test_config(monkeypatch)

        with patch('src.scraper.requests.get') as mock_get:
            # Mock successful response
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.text = '<html><head><title>Test Title</title></head><body></body></html>'
            mock_get.return_value = mock_response

            # Test the method
            result = self.scraper.check_website()

            # Assertions
            assert result == "Test Title"
            mock_get.assert_called_once_with(self.test_url, timeout=timeout)
            mock_response.raise_for_status.assert_called_once()

    def test_check_website_no_title(self, monkeypatch):
        """Test website with no title"""
        timeout, max_retries, retry_delay = self._setup_test_config(monkeypatch)

        with patch('src.scraper.requests.get') as mock_get:
            # Mock response without title
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.text = '<html><head></head><body>No title here</body></html>'
            mock_get.return_value = mock_response

            # Test the method
            result = self.scraper.check_website()

            # Assertions
            assert result is None
            mock_get.assert_called_once_with(self.test_url, timeout=timeout)

    def test_check_website_request_exception(self, monkeypatch):
        """Test handling of request exceptions with retry logic"""
        timeout, max_retries, retry_delay = self._setup_test_config(monkeypatch, max_retries=3)

        with patch('src.scraper.requests.get') as mock_get, \
             patch('src.scraper.time.sleep') as mock_sleep:

            # Mock request exception
            mock_get.side_effect = requests.RequestException("Connection error")

            # Test the method
            result = self.scraper.check_website()

            # Assertions
            assert result is None
            assert mock_get.call_count == max_retries
            assert mock_sleep.call_count == max_retries - 1  # Sleep called between retries

    def test_retry_logic_with_eventual_success(self, monkeypatch):
        """Test that retry logic works when request succeeds on second attempt"""
        timeout, max_retries, retry_delay = self._setup_test_config(monkeypatch, max_retries=3)

        with patch('src.scraper.requests.get') as mock_get, \
             patch('src.scraper.time.sleep') as mock_sleep:

            # First call fails, second succeeds
            mock_response = Mock()
            mock_response.raise_for_status.return_value = None
            mock_response.text = '<html><head><title>Success Title</title></head><body></body></html>'

            mock_get.side_effect = [
                requests.ConnectionError("First attempt fails"),
                mock_response
            ]

            # Test the method
            result = self.scraper.check_website()

            # Assertions
            assert result == "Success Title"
            assert mock_get.call_count == 2  # Called twice
            assert mock_sleep.call_count == 1  # Sleep called once between retries

    def test_multiple_scrapers_have_different_loggers(self):
        """Test that multiple scrapers have unique loggers"""
        scraper1 = WebScraper("https://site1.com")
        scraper2 = WebScraper("https://site2.com")

        # Logger names should be different
        assert scraper1.logger.name != scraper2.logger.name
        assert scraper1.url != scraper2.url


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"])
