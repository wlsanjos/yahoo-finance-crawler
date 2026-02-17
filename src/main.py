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

        # 1. Scrape (Setup inicial)
        scraper = YahooFinanceScraper()
        scraper.fetch_screener_page()
        scraper.apply_region_filter(args.region)
        scraper.maximize_rows_per_page()

        all_data = []
        page_num = 1

        while True:
            print(f"\n--- Extraindo dados da página {page_num} ---")
            html = scraper.get_page_source()

            # 2. Parse (Lê a tabela da página atual)
            parser_obj = YahooFinanceParser(html)
            page_data = parser_obj.extract_equity_data()
            all_data.extend(page_data)

            print(f"-> {len(page_data)} registros extraídos nesta página. Total acumulado: {len(all_data)}")

            if not scraper.go_to_next_page():
                break

            page_num += 1

        print(f"\n✅ Extração concluída! Total absoluto de {len(all_data)} registros capturados.")

        # 3. Salvando os dados no CSV
        if all_data:
            storage = DataStorage()
            safe_region = "".join(c for c in args.region if c.isalnum() or c in (' ', '_', '-')).strip().replace(' ', '_').lower()
            filename = f"{safe_region}_stocks.csv"
            storage.save_to_csv(all_data, filename)
        else:
            print("Nenhum dado encontrado para salvar.")

    except Exception as e:
        print(f"Erro fatal: {e}")
    finally:
        if scraper:
            scraper.close()

if __name__ == "__main__":
    main()
