# Yahoo Finance Crawler

Este é um projeto modular e orientado a objetos em Python para extração de dados do Yahoo Finance. O objetivo é navegar pela página de "Equity Screener", aplicar filtros de região e extrair dados fundamentais das ações listadas.

## 🚀 Funcionalidades

- **Scraping**: Automação de navegador com Selenium para acessar o Screener e aplicar filtros.
- **Parsing**: Processamento de HTML com BeautifulSoup para extrair dados da tabela.
- **Armazenamento**: Exportação dos dados extraídos para arquivos CSV.
- **CLI**: Interface de linha de comando para fácil execução com parâmetros.

## 🛠️ Pré-requisitos

- Python 3.8+
- Google Chrome (ou outro navegador compatível com Selenium)

## 📦 Instalação

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/yahoo-finance-crawler.git
   cd yahoo-finance-crawler
   ```

2. Crie um ambiente virtual (opcional, mas recomendado):
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```

3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## 💻 Uso

Para executar o crawler, utilize o script principal informando a região desejada:

```bash
python src/main.py --region "United States"
```

Isso irá:
1. Abrir o navegador e acessar o Screener.
2. Filtrar pela região "United States".
3. Extrair os dados da tabela (Símbolo, Nome, Preço).
4. Salvar os resultados em um arquivo CSV.

## 🧪 Testes

O projeto utiliza `pytest` para testes automatizados. Para rodar a suíte de testes:

```bash
pytest
```

## 📂 Estrutura do Projeto

```
yahoo-finance-crawler/
├── src/
│   ├── scraper.py  # Automação do navegador (Selenium)
│   ├── parser.py   # Extração de dados (BeautifulSoup)
│   ├── storage.py  # Salvamento de arquivos (CSV)
│   └── main.py     # Ponto de entrada e orquestração
├── tests/          # Testes automatizados
├── requirements.txt
└── README.md
```
