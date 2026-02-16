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
            # Encontrar a tabela (ajustar seletor conforme necessidade, geralmente a primeira tabela ou por classe)
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
                if len(cols) > 4: # Garantir que tem colunas suficientes
                    symbol = cols[1].get_text(strip=True)
                    name = cols[2].get_text(strip=True)
                    price = cols[3].get_text(strip=True) # Geralmente Price (Intraday) é a terceira ou quarta.
                    price = cols[3].get_text(strip=True) # Tentativa no indice 3

                    results.append({
                        "symbol": symbol,
                        "name": name,
                        "price": price
                    })
        except Exception as e:
            print(f"Erro ao extrair dados: {e}")
            return []

        return results
