import argparse
from src.scraper import YahooFinanceScraper
from src.parser import YahooFinanceParser
from src.storage import DataStorage

def main():
    """
    Ponto de entrada principal do crawler.
    Uso: python src/main.py --region "United States"
    """
    parser = argparse.ArgumentParser(description="Crawler do Yahoo Finance Equity Screener")
    parser.add_argument("--region", type=str, required=True, help="Região para filtrar (ex: 'United States')")

    args = parser.parse_args()

    # 1. Scrape
    scraper = YahooFinanceScraper()
    # Implementation pending...

    # 2. Parse
    # Implementation pending...

    # 3. Store
    # Implementation pending...
