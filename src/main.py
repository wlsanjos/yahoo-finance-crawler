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

    scraper = None
    try:
        print(f"Iniciando crawler para região: {args.region}")

        # 1. Scrape
        scraper = YahooFinanceScraper()
        scraper.fetch_screener_page()
        scraper.apply_region_filter(args.region)
        html = scraper.get_page_source()

        # 2. Parse
        parser_obj = YahooFinanceParser(html)
        data = parser_obj.extract_equity_data()

        print(f"Dados extraídos: {len(data)} registros.")

        # 3. Store
        if data:
            storage = DataStorage()
            # Sanitize filename
            safe_region = "".join(c for c in args.region if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_').lower()
            filename = f"{safe_region}_stocks.csv"
            storage.save_to_csv(data, filename)
        else:
            print("Nenhum dado encontrado para salvar.")

    except Exception as e:
        print(f"Erro fatal: {e}")
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main()
