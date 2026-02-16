import pytest
from src.scraper import YahooFinanceScraper
from src.parser import YahooFinanceParser

@pytest.fixture
def mock_html():
    return "<html><body><h1>Test Page</h1></body></html>"

@pytest.fixture
def scraper():
    return YahooFinanceScraper()

@pytest.fixture
def parser(mock_html):
    return YahooFinanceParser(mock_html)
