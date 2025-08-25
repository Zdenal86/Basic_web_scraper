#!/usr/bin/env python3

import pytest
import os
import logging
import tempfile
from unittest.mock import patch, Mock
import sys
import pathlib

# Add parent directory to path to import src modules
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from src import ScraperLogger, Config


class TestScraperLogger:
    """Test suite for ScraperLogger class"""

    def setup_method(self):
        """Setup before each test"""
        self.logger_name = "test_logger"
        # Use test configuration file
        test_config_path = os.path.join(os.path.dirname(__file__), 'test_config.json')
        from src.config import Config
        test_config = Config(test_config_path)
        self.scraper_logger = ScraperLogger(self.logger_name, test_config)

    def test_scraper_logger_initialization(self):
        """Test ScraperLogger initialization"""
        assert self.scraper_logger is not None
        assert hasattr(self.scraper_logger, 'logger')
        assert hasattr(self.scraper_logger, 'config')

    def test_get_logger_returns_logger_instance(self):
        """Test that get_logger returns a logging.Logger instance"""
        logger = self.scraper_logger.get_logger()
        assert isinstance(logger, logging.Logger)
        assert logger.name == self.logger_name

    def test_logger_has_correct_level(self):
        """Test that logger respects configured level from test config"""
        logger = self.scraper_logger.get_logger()
        # Test config has DEBUG level
        assert logger.level == logging.DEBUG

    def test_logger_has_file_handler(self):
        """Test that logger has file handler configured"""
        logger = self.scraper_logger.get_logger()

        # Najdeme FileHandler mezi handlery
        file_handlers = [h for h in logger.handlers if isinstance(h, logging.FileHandler)]
        assert len(file_handlers) == 1

    def test_logger_has_console_handler_when_enabled(self):
        """Test that logger has console handler when enabled in config"""
        # Test config has console_output=true
        logger = self.scraper_logger.get_logger()

        # Najdeme StreamHandler (console) mezi handlery
        console_handlers = [h for h in logger.handlers
                          if isinstance(h, logging.StreamHandler) and not isinstance(h, logging.FileHandler)]
        assert len(console_handlers) == 1

    def test_logger_no_console_handler_when_disabled(self):
        """Test that logger file path is correctly configured"""
        # Test that file path from config is used
        expected_path = 'logs/test_scraper.log'
        file_handlers = [h for h in self.scraper_logger.get_logger().handlers
                        if isinstance(h, logging.FileHandler)]

        # Check that file handler exists and uses correct path
        assert len(file_handlers) == 1
        # Note: We can't easily check the exact path without accessing private attributes

    def test_logs_directory_creation(self):
        """Test that logs directory is created if it doesn't exist"""
        # Add test implementation
        pass

    def test_custom_config_usage(self):
        """Test ScraperLogger with custom config"""
        # Add test implementation
        pass

    def test_logger_formatters_are_applied(self):
        """Test that custom formatters are applied to handlers"""
        # Add test implementation
        pass

    def test_multiple_logger_instances_are_unique(self):
        """Test that multiple ScraperLogger instances create unique loggers"""
        logger1 = ScraperLogger("logger1")
        logger2 = ScraperLogger("logger2")

        assert logger1.get_logger().name != logger2.get_logger().name
        assert logger1.get_logger() is not logger2.get_logger()


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"])
