#!/usr/bin/env python3

import pytest
import os
import json
import tempfile
from unittest.mock import patch, mock_open
import sys
import pathlib

# Add parent directory to path to import src modules
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))
from src import Config


class TestConfig:
    """Test suite for Config class"""

    def setup_method(self):
        """Setup before each test"""
        self.config = Config()

    def test_config_initialization_default(self):
        """Test Config initialization with default config"""
        config = Config()
        assert config is not None
        # Add more specific tests here

    def test_config_initialization_custom_file(self):
        """Test Config initialization with custom config file"""
        # Use our test config file
        test_config_path = os.path.join(os.path.dirname(__file__), 'test_config.json')
        config = Config(test_config_path)
        
        assert config is not None
        # Verify it loads test config values
        assert config.get('logging', 'level', 'INFO') == 'DEBUG'
        assert config.get('scraping', 'timeout', 10) == 5

    def test_get_method_returns_default_when_key_missing(self):
        """Test that get method returns default value when key is missing"""
        default_value = "default_test_value"
        result = self.config.get('nonexistent_section', 'nonexistent_key', default_value)
        assert result == default_value

    def test_get_method_returns_config_value_when_exists(self):
        """Test that get method returns actual config value when it exists"""
        # Use test config to verify existing values
        test_config_path = os.path.join(os.path.dirname(__file__), 'test_config.json')
        config = Config(test_config_path)
        
        # Test existing values from test_config.json
        assert config.get('logging', 'level', 'INFO') == 'DEBUG'
        assert config.get('scraping', 'max_retries', 1) == 2
        assert config.get('logging', 'console_output', False) == True

    def test_get_section_method(self):
        """Test get_section method functionality"""
        test_config_path = os.path.join(os.path.dirname(__file__), 'test_config.json')
        config = Config(test_config_path)
        
        # Get entire logging section
        logging_section = config.get_section('logging')
        assert isinstance(logging_section, dict)
        assert 'level' in logging_section
        assert 'console_output' in logging_section
        assert logging_section['level'] == 'DEBUG'
        
        # Test nonexistent section
        nonexistent = config.get_section('nonexistent_section')
        assert nonexistent == {}

    def test_update_method(self):
        """Test config update functionality"""
        original_value = self.config.get('test_section', 'test_key', 'original')
        
        # Update config
        self.config.update('test_section', 'test_key', 'updated_value')
        
        # Verify update
        updated_value = self.config.get('test_section', 'test_key', 'original')
        assert updated_value == 'updated_value'

    def test_load_config_with_invalid_json(self):
        """Test loading config with invalid JSON"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as tmp_file:
            # Write invalid JSON
            tmp_file.write('{ invalid json content }')
            temp_path = tmp_file.name
            
        try:
            # Should not raise exception, should fall back to defaults
            config = Config(temp_path)
            assert config is not None
            
            # Should return defaults since JSON is invalid
            result = config.get('any_section', 'any_key', 'default')
            assert result == 'default'
        finally:
            try:
                os.unlink(temp_path)
            except (OSError, PermissionError):
                # Ignore cleanup errors on Windows
                pass

    def test_load_config_with_missing_file(self):
        """Test loading config when file doesn't exist"""
        nonexistent_file = "/nonexistent/path/config.json"
        
        # Should not raise exception, should fall back to defaults
        config = Config(nonexistent_file)
        assert config is not None
        
        # Should return defaults since file doesn't exist
        result = config.get('any_section', 'any_key', 'default')
        assert result == 'default'


if __name__ == "__main__":
    # Run tests if script is executed directly
    pytest.main([__file__, "-v"])
