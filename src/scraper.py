from selenium import webdriver

class YahooFinanceScraper:
    """
    Gerencia a automação do navegador para acessar o Yahoo Finance.
    """
    def __init__(self, driver_config=None):
        """
        Inicializa o WebDriver do Selenium.
        """
        from selenium.webdriver.chrome.service import Service
        from selenium.webdriver.chrome.options import Options
        from webdriver_manager.chrome import ChromeDriverManager
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC

        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.wait = WebDriverWait(self.driver, 10)

    def fetch_screener_page(self):
        """
        Acessa a página do Screener de ações do Yahoo Finance.
        """
        self.driver.get("https://finance.yahoo.com/research-hub/screener/equity/")

    def apply_region_filter(self, region: str):
        """
        Aplica o filtro de região na interface usando o Selenium.
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC
        import time

        # 1. Localizar e clicar no botão de Região
        region_button_xpath = "//button[contains(., 'Region')]"
        region_btn = self.wait.until(EC.element_to_be_clickable((By.XPATH, region_button_xpath)))

        # 2. Remover filtro padrão (ex: United States) se existir
        try:
            # Tenta encontrar o botão 'Remove Filter' próximo ao botão de região
            remove_btn_xpath = "//button[contains(., 'Region')]/parent::div//button[@aria-label='Remove Filter']"
            remove_btn = self.driver.find_element(By.XPATH, remove_btn_xpath)
            remove_btn.click()
            time.sleep(1)
        except Exception:
            pass

        # 3. Abrir o dropdown de região
        region_btn.click()

        # 4. Digitar a nova região na busca
        search_input_css = "input[placeholder='Search...']"
        search_input = self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, search_input_css)))
        search_input.clear()
        search_input.send_keys(region)

        # 5. Selecionar a região na lista (Checkbox/Label)
        region_item_xpath = f"//label[contains(., '{region}')]"
        region_label = self.wait.until(EC.element_to_be_clickable((By.XPATH, region_item_xpath)))
        region_label.click()

        # 6. Clicar em Apply (se necessário - alguns dropdowns aplicam ao clicar, outros precisam de confirmação)
        region_btn.click()

        # 7. Aguardar a tabela atualizar
        table_css = "div.table-container table"
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, table_css)))
        time.sleep(2)

    def get_page_source(self) -> str:
        """
        Retorna o código HTML da página atual.
        """
        return self.driver.page_source

    def close(self):
        """
        Fecha o navegador e libera os recursos.
        """
        if self.driver:
            self.driver.quit()
