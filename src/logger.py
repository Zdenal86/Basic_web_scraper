#!/usr/bin/env python3

import logging
import os
from typing import Optional

try:
    from .config import Config
except ImportError:
    from config import Config


class ScraperLogger:
    """Handles logging configuration and setup for the scraper"""

    def __init__(self, name: str, config: Optional[Config] = None):
        self.config = config or Config()
        self.logger = self._setup_logger(name)

    def _setup_logger(self, name: str) -> logging.Logger:
        """Setup logging with configuration from config file"""
        # Load configuration values
        log_file = self.config.fetch_config_value('logging', 'file_path', 'logs/scraper.log')
        log_level = self.config.fetch_config_value('logging', 'level', 'INFO')
        console_output = self.config.fetch_config_value('logging', 'console_output', True)
        console_format = self.config.fetch_config_value('logging', 'console_log_format', '%(levelname)s - %(message)s')
        file_format = self.config.fetch_config_value('logging', 'file_log_format', '%(asctime)s - %(levelname)s - %(message)s')

        # Create logs directory
        os.makedirs(os.path.dirname(log_file), exist_ok=True)

        # Create custom logger
        logger = logging.getLogger(name)
        logger.setLevel(getattr(logging, log_level))

        # Clear existing handlers to avoid duplicates
        logger.handlers.clear()

        # File handler
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_formatter = logging.Formatter(file_format)
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        # Console handler (if enabled)
        if console_output:
            console_handler = logging.StreamHandler()
            console_formatter = logging.Formatter(console_format)
            console_handler.setFormatter(console_formatter)
            logger.addHandler(console_handler)

        return logger

    def get_logger(self) -> logging.Logger:
        """Get the configured logger instance"""
        return self.logger


if __name__ == "__main__":
    # Test the logger
    test_logger = ScraperLogger("test_logger")
    logger = test_logger.get_logger()
    logger.info("Test log message")
    logger.warning("Test warning message")
    logger.error("Test error message")
