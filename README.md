# 📈 Yahoo Finance Crawler

Olá! Bem-vindo ao **Yahoo Finance Crawler**.

Este projeto é uma ferramenta que desenvolvi para resolver um desafio comum, mas chato: extrair dados financeiros de um site que muda o tempo todo e usa tecnologias complexas (como React e carregamento dinâmico).

---

## 🚀 Como Rodar o Projeto (Passo a Passo)

Vamos direto ao que interessa. Para ver esse robô funcionando na sua máquina, siga os passos abaixo:

### 1. Pré-requisitos
Você vai precisar ter instalado:
*   **Python 3.10+**
*   **Google Chrome** (o navegador que o robô controla)

### 2. Instalação
Primeiro, baixe o código e prepare o terreno:

```bash
# Clone este repositório
git clone https://github.com/wlsanjos/yahoo-finance-crawler.git
cd yahoo-finance-crawler

# Crie um ambiente virtual (Recomendado para não bagunçar seu Python global)
python -m venv venv

# Ative o ambiente virtual
# No Linux/Mac:
source venv/bin/activate
# No Windows:
# venv\Scripts\activate

# Instale as dependências
pip install -r requirements.txt
```

### 3. Executando o Robô
O comando é super simples. Você só precisa dizer qual região (país) você quer analisar.

Para buscar ações da **Argentina**, por exemplo:
```bash
python -m src.main --region "Argentina"
```

Para buscar dos **Estados Unidos**:
```bash
python -m src.main --region "United States"
```

### O que vai acontecer?
1.  O **Chrome vai abrir** (você verá ele navegando sozinho).
2.  Ele vai entrar no "Classic Screener" do Yahoo Finance.
3.  Vai **selecionar a região** que você pediu e remover os filtros padrão.
4.  Vai percorrer **página por página**, coletando dados de cada ação.
5.  No final, ele salva tudo em um arquivo `.csv` na pasta do projeto (ex: `Argentina_stocks.csv`).

---

## 🧪 Como Rodar os Testes

Para garantir que tudo está funcionando direitinho, criei uma bateria de testes automatizados. Você pode rodar eles para conferir a integridade do código.

1. Configure o caminho do projeto (para o Python achar os módulos):
   ```bash
   export PYTHONPATH=$PYTHONPATH:.
   ```

2. Execute os testes com o `pytest`:
   ```bash
   pytest
   ```

**O que está sendo testado?**
*   **Parser**: Se o HTML está sendo lido corretamente e se ignora dados ruins.
*   **Scraper**: Simula a navegação (sem abrir o navegador de verdade) para testar a lógica dos botões.
*   **Storage**: Verifica se o arquivo CSV é criado e salvo certinho.

---

## 🧠 Como Funciona por Baixo dos Panos

Se você é técnico ou recrutador, aqui estão alguns detalhes legais sobre como resolvi os problemas:

*   **Não é só um script**: O código está organizado como um software de verdade (Orientação a Objetos), separado em módulos (`Scraper` para navegar, `Parser` para ler HTML, `Storage` para salvar). Isso facilita muito dar manutenção.
*   **Paginação que funciona**: Sites modernos (SPA) muitas vezes não mudam a URL quando você clica em "Próxima". Eu implementei uma lógica que "lê" o DOM para ter certeza que a tabela mudou antes de seguir, evitando loops infinitos ou dados duplicados.
*   **Resiliência**: O robô sabe lidar com erros. Se um elemento demorar para carregar ou um botão mudar de lugar (usei `data-testid` para garantir), ele tenta se recuperar ao invés de simplesmente travar.
*   **Limpeza de Dados**: O Yahoo entrega números com vírgulas, sufixos (M, B) e símbolos. O `Parser` cuida de tudo isso para entregar dados prontos para análise.

### Estrutura dos Arquivos
*   `src/main.py`: O chefe da operação. Lê seus comandos e orquestra tudo.
*   `src/scraper.py`: O "motorista". É quem controla o Selenium e clica nos botões.
*   `src/parser.py`: O "tradutor". Pega o HTML bagunçado e transforma em dados úteis.
*   `src/storage.py`: O "escrivão". Salva tudo no CSV.

---
*Fique à vontade para explorar o código, rodar os testes (`pytest`) ou me mandar uma dúvida!*
