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
        # Use test configuration file
        test_config_path = os.path.join(os.path.dirname(__file__), 'test_config.json')
        self.scraper = WebScraper(self.test_url, config_file=test_config_path)

    def _get_test_config_values(self):
        """Helper to get expected test config values - simple and clear"""
        return {
            'timeout': 5,
            'max_retries': 2,
            'retry_delay': 0.1
        }

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

    def test_logger_level_is_debug(self):
        """Test that logger level is set to DEBUG from test config"""
        assert self.scraper.logger.level == logging.DEBUG

    def test_check_website_success(self):
        """Test successful website checking"""
        config_values = self._get_test_config_values()

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
            mock_get.assert_called_once_with(self.test_url, timeout=config_values['timeout'])
            mock_response.raise_for_status.assert_called_once()

    def test_check_website_no_title(self):
        """Test website with no title"""
        config_values = self._get_test_config_values()

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
            mock_get.assert_called_once_with(self.test_url, timeout=config_values['timeout'])

    def test_check_website_request_exception(self):
        """Test handling of request exceptions with retry logic"""
        config_values = self._get_test_config_values()

        with patch('src.scraper.requests.get') as mock_get, \
             patch('src.scraper.time.sleep') as mock_sleep:

            # Mock request exception
            mock_get.side_effect = requests.RequestException("Connection error")

            # Test the method
            result = self.scraper.check_website()

            # Assertions
            assert result is None
            assert mock_get.call_count == config_values['max_retries']
            assert mock_sleep.call_count == config_values['max_retries'] - 1  # Sleep called between retries

    def test_retry_logic_with_eventual_success(self):
        """Test that retry logic works when request succeeds on second attempt"""
        config_values = self._get_test_config_values()

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
        test_config_path = os.path.join(os.path.dirname(__file__), 'test_config.json')
        scraper1 = WebScraper("https://site1.com", config_file=test_config_path)
        scraper2 = WebScraper("https://site2.com", config_file=test_config_path)

        # Logger names should be different
        assert scraper1.logger.name != scraper2.logger.name
        assert scraper1.url != scraper2.url


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"])
