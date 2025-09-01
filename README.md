# Web Scraper

[![Tests](https://github.com/Zdenal86/Basic_web_scraper/workflows/Tests/badge.svg)](https://github.com/Zdenal86/Basic_web_scraper/actions)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Coverage](https://img.shields.io/badge/coverage-84%25-brightgreen.svg)](https://github.com/Zdenal86/Basic_web_scraper)

Professional web scraping tool with comprehensive logging, error handling, and configuration management.

## 🚀 Features

- **Configurable timeout and retry logic**
- **Professional logging** (file + console output)
- **JSON-based configuration**
- **Comprehensive test suite** (27 tests with 84% coverage)
- **Clean architecture** with separated concerns
- **Error handling** for network issues

## 📁 Project Structure

```
Basic_web_scraper/
├── src/
│   ├── __init__.py
│   ├── scraper.py      # Main WebScraper class
│   ├── logger.py       # Logging configuration
│   └── config.py       # Configuration management
├── tests/
│   ├── test_scraper.py # Comprehensive test suite
│   ├── test_config.py  # Configuration tests
│   └── test_logger.py  # Logger tests
├── logs/               # Log files
├── config.json         # Runtime configuration
├── main.py            # Entry point
└── requirements.txt   # Dependencies
```

## 🛠️ Installation

```bash
# Clone repository
git clone <your-repo-url>
cd Basic_web_scraper

# Create virtual environment
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

## 💾 Configuration

Create `config.json` with your settings:

```json
{
  "scraping": {
    "timeout": 10,
    "max_retries": 3,
    "retry_delay": 1.0
  },
  "logging": {
    "level": "INFO",
    "console_output": true,
    "file_path": "logs/scraper.log",
    "console_log_format": "%(levelname)s - %(message)s",
    "file_log_format": "%(asctime)s - %(levelname)s - %(message)s"
  }
}
```

## 🎯 Usage

```python
from src import WebScraper

# Basic usage
scraper = WebScraper("https://example.com")
title = scraper.check_website()
print(f"Website title: {title}")

# With custom config
scraper = WebScraper("https://example.com", config_file="my_config.json")
title = scraper.check_website()
```

## 🧪 Testing

```bash
# Run all tests
python -m pytest

# Run with coverage
python -m pytest --cov=src

# Run with verbose output
python -m pytest -v

# Run specific test file
python -m pytest tests/test_scraper.py
```

## 📊 Test Coverage

- **27 comprehensive tests**
- **84% code coverage**
- Unit tests with mocking
- Configuration isolation
- Error handling validation
- Retry logic testing

## 🔧 Technologies Used

- **Python 3.11+**
- **requests** - HTTP library
- **beautifulsoup4** - HTML parsing
- **pytest** - Testing framework
- **pytest-cov** - Coverage reporting
- **JSON** - Configuration management

## 🏗️ Architecture

- **Separation of concerns** - Logger, Config, Scraper classes
- **Dependency injection** - Configurable components
- **Error handling** - Comprehensive exception management
- **Testing** - Mocked dependencies, isolated tests

## 🔄 Continuous Integration

- **GitHub Actions** - Automated testing on every push/PR
- **Multi-Python testing** - Tests run on Python 3.11, 3.12, and 3.13
- **Quality assurance** - All 27 tests must pass before merge

## 👨‍💻 Author & AI Collaboration

This project was developed in collaboration with **GitHub Copilot AI assistant**. The AI helped with:

- **Code architecture** and design patterns
- **Test implementation** and comprehensive coverage
- **Documentation** and best practices
- **Code review** and optimization suggestions
- **Professional Python** development standards

The collaboration demonstrates effective **human-AI partnership** in software development, combining human creativity and problem-solving with AI's knowledge of best practices and code patterns.

## 📝 License

MIT License
