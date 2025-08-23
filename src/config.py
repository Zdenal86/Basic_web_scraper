#!/usr/bin/env python3

import json
import os
from typing import Any, Dict, Optional


class Config:
    """Configuration manager for web scraper"""

    def __init__(self, config_file: Optional[str] = 'config.json'):
        """
        Initialize configuration

        Args:
            config_file: Path to configuration JSON file (None uses default)
        """
        if config_file is None:
            config_file = 'config.json'
        self.config_file = config_file
        self.settings = self.load_config()

    def load_config(self) -> Dict[str, Any]:
        """
        Load configuration from JSON file

        Returns:
            Dictionary with configuration settings
        """
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                # Return default configuration if file doesn't exist
                return self._get_default_config()
        except (json.JSONDecodeError, FileNotFoundError, IOError) as e:
            print(f"Warning: Could not load config file {self.config_file}: {e}")
            print("Using default configuration")
            return self._get_default_config()

    def _get_default_config(self) -> Dict[str, Any]:
        """
        Get default configuration

        Returns:
            Default configuration dictionary
        """
        return {
            "logging": {
                "level": "INFO",
                "file_path": "logs/scraper.log",
                "console_output": True,
                "max_file_size_mb": 10
            }
        }

    def get(self, section: str, key: str, default: Any = None) -> Any:
        """
        Get specific configuration value

        Args:
            section: Configuration section name
            key: Configuration key name
            default: Default value if key not found

        Returns:
            Configuration value or default
        """
        try:
            return self.settings[section][key]
        except KeyError:
            return default

    def update(self, section: str, key: str, value: Any) -> None:
        """
        Update configuration value and save to file

        Args:
            section: Configuration section name
            key: Configuration key name
            value: New value
        """
        if section not in self.settings:
            self.settings[section] = {}

        self.settings[section][key] = value
        self._save_config()

    def _save_config(self) -> None:
        """Save current configuration to file"""
        try:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)

            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.settings, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Warning: Could not save config file {self.config_file}: {e}")

    def get_section(self, section: str) -> Dict[str, Any]:
        """
        Get entire configuration section

        Args:
            section: Section name

        Returns:
            Dictionary with section settings
        """
        return self.settings.get(section, {})

    def __str__(self) -> str:
        """String representation of configuration"""
        return f"Config({self.config_file}): {len(self.settings)} sections"

    def __repr__(self) -> str:
        """Detailed string representation"""
        return f"Config(file='{self.config_file}', sections={list(self.settings.keys())})"