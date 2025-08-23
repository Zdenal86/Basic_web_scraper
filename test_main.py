#!/usr/bin/env python3

import pytest
import os
import logging
import requests
from unittest.mock import patch, Mock, MagicMock
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

    def test_webscraper_initialization(self):
        """Test WebScraper initialization"""
        assert self.scraper.url == self.test_url
        assert hasattr(self.scraper, 'logger')
        assert isinstance(self.scraper.logger, logging.Logger)

    @patch('os.makedirs')
    def test_setup_logging_creates_logs_directory(self, mock_makedirs):
        """Test that setup_logging calls os.makedirs for logs directory"""
        WebScraper("https://test.com")
        mock_makedirs.assert_called_once_with(
            os.path.dirname('logs/scraper.log'),
            exist_ok=True
        )


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

    @patch('scr.scraper.requests.get')
    def test_check_website_success(self, mock_get):
        """Test successful website checking"""
        # Mock successful response
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = '<html><head><title>Test Title</title></head><body></body></html>'
        mock_get.return_value = mock_response

        # Test the method
        result = self.scraper.check_website()

        # Assertions
        assert result == "Test Title"
        mock_get.assert_called_once_with(self.test_url)
        mock_response.raise_for_status.assert_called_once()

    @patch('scr.scraper.requests.get')
    def test_check_website_no_title(self, mock_get):
        """Test website with no title"""
        # Mock response without title
        mock_response = Mock()
        mock_response.raise_for_status.return_value = None
        mock_response.text = '<html><head></head><body>No title here</body></html>'
        mock_get.return_value = mock_response

        # Test the method
        result = self.scraper.check_website()

        # Assertions
        assert result is None
        mock_get.assert_called_once_with(self.test_url)

    @patch('scr.scraper.requests.get')
    def test_check_website_request_exception(self, mock_get):
        """Test handling of request exceptions"""
        # Mock request exception
        mock_get.side_effect = requests.RequestException("Connection error")

        # Test the method
        result = self.scraper.check_website()

        # Assertions
        assert result is None
        mock_get.assert_called_once_with(self.test_url)

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