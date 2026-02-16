import pandas as pd

class DataStorage:
    """
    Gerencia o salvamento dos dados extraídos.
    """
    def save_to_csv(self, data: list, filename: str):
        """
        Salva os dados em um arquivo CSV com os cabeçalhos: symbol, name, price.
        """
        import csv

        if not data:
            print("Nenhum dado para salvar.")
            return

        try:
            with open(filename, mode='w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=["symbol", "name", "price"])
                writer.writeheader()
                writer.writerows(data)
            print(f"Dados salvos com sucesso em: {filename}")
        except IOError as e:
            print(f"Erro ao salvar arquivo: {e}")
