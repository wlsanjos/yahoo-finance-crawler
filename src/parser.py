from bs4 import BeautifulSoup

class YahooFinanceParser:
    """
    Analisa o conteúdo HTML do Yahoo Finance.
    """
    def __init__(self, html_content: str):
        """
        Inicializa o parser com o conteúdo HTML.
        """
        self.soup = BeautifulSoup(html_content, 'html.parser')

    def extract_equity_data(self) -> list:
        """
        Extrai símbolo, nome e preço (intraday) da tabela de resultados.
        """
        results = []
        try:
            table = self.soup.find('table')
            if not table:
                print("Erro: Tabela não encontrada.")
                return results

            tbody = table.find('tbody')
            if not tbody:
                print("Erro: Corpo da tabela não encontrado.")
                return results

            rows = tbody.find_all('tr')
            for row in rows:
                cols = row.find_all('td')
                if len(cols) > 4:

                    # Indices identificados via debug:
                    # [0]: Checkbox/Num (ex: "1")
                    # [1]: Symbol (ex: "NNVDA.BA")
                    # [2]: Name (ex: "NVIDIA Corporation")
                    # [3]: Vazio/Graph
                    # [4]: Price (ex: "11,230.00")

                    try:
                        symbol = cols[1].get_text(strip=True)
                        name = cols[2].get_text(strip=True)
                        price = cols[4].get_text(strip=True)

                        results.append({
                            "symbol": symbol,
                            "name": name,
                            "price": price
                        })
                    except IndexError:
                        continue
        except Exception as e:
            print(f"Erro ao extrair dados: {e}")
            return []

        return results
