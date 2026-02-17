import pytest
from unittest.mock import MagicMock, patch
from src.scraper import YahooFinanceScraper

@pytest.fixture
def mock_driver():
    with patch('src.scraper.webdriver.Chrome') as mock_chrome:
        driver_instance = MagicMock()
        mock_chrome.return_value = driver_instance
        yield driver_instance

@pytest.fixture
def scraper(mock_driver):
    with patch('src.scraper.ChromeDriverManager'):
        return YahooFinanceScraper()

def test_initialization(scraper, mock_driver):
    assert scraper.driver == mock_driver
    mock_driver.maximize_window.assert_called_once()

def test_fetch_screener_page(scraper, mock_driver):
    scraper.fetch_screener_page()
    mock_driver.get.assert_called_with("https://finance.yahoo.com/research-hub/screener/equity/")

def test_close_driver(scraper, mock_driver):
    scraper.close()
    mock_driver.quit.assert_called_once()
