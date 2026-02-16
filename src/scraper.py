from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class YahooFinanceScraper:
    """
    Gerencia a automação do navegador para acessar o Yahoo Finance.
    """
    def __init__(self, driver_config=None):
        chrome_options = Options()
        # chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.page_load_strategy = 'eager'
        chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")

        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.maximize_window()
        self.wait = WebDriverWait(self.driver, 15)

    def fetch_screener_page(self):
        self.driver.get("https://finance.yahoo.com/research-hub/screener/equity/")

    def apply_region_filter(self, region: str):
        print("\n--- INICIANDO NAVEGAÇÃO NA URL DIRETA ---")
        try:
            # Passo 0: Pop-ups
            try:
                popups = self.driver.find_elements(By.XPATH, "//button[contains(., 'Accept') or contains(@name, 'agree')]")
                if popups: popups[0].click()
            except:
                pass

            time.sleep(3)

            # Passo 1: Clicar no botão 'Region'
            print("Passo 1: Procurando botão de filtro 'Region'...")
            region_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Region') or contains(., 'region')]")))
            self.driver.execute_script("arguments[0].click();", region_btn)
            print("-> Menu de Região aberto!")
            time.sleep(1)

            # Passo 2: Limpar filtros padrão (United States)
            print("Passo 2: Removendo 'United States' se estiver selecionado...")
            try:
                # Tenta achar o botão de remover específico
                remove_us = self.driver.find_elements(By.XPATH, "//button[contains(@title, 'Remove United States') or contains(@aria-label, 'Remove United States')]")
                if remove_us:
                    self.driver.execute_script("arguments[0].click();", remove_us[0])
                else:
                    us_check = self.driver.find_elements(By.XPATH, "//input[@type='checkbox' and @value='us']")
                    if us_check and us_check[0].is_selected():
                        self.driver.execute_script("arguments[0].click();", us_check[0])
            except:
                pass
            time.sleep(1)

            # Passo 3: Buscar a Região
            print(f"Passo 3: Buscando região: {region}...")
            search_input = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search...']")))
            search_input.clear()
            search_input.send_keys(region)
            time.sleep(1.5)

            # Selecionar a região na lista
            print(f"-> Selecionando '{region}' na lista...")
            try:
                checkbox_xpath = f"//label[contains(., '{region}')]//input[@type='checkbox']"
                region_checkbox = self.wait.until(EC.presence_of_element_located((By.XPATH, checkbox_xpath)))
                if not region_checkbox.is_selected():
                    self.driver.execute_script("arguments[0].click();", region_checkbox)
            except:
                region_item = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//label[contains(., '{region}')]")))
                self.driver.execute_script("arguments[0].click();", region_item)

            time.sleep(1)

            # Passo 4: Clicar em Apply
            print("Passo 4: Clicando em Apply...")
            try:
                apply_btn = self.driver.find_element(By.XPATH, "//button[contains(., 'Apply')]")
                self.driver.execute_script("arguments[0].click();", apply_btn)
            except Exception as e:
                print(f"Aviso: Botão Apply não encontrado ou não necessário ({e})")

            # Passo 5: Atualizar a tabela principal
            print("Passo 5: Filtro aplicado! Aguardando carregamento...")
            time.sleep(4)

        except Exception as e:
            print(f"\n[ERRO] Falha no Selenium: {e}")
            self.driver.save_screenshot("debug_erro_direto.png")
            raise e

    def get_page_source(self) -> str:
        return self.driver.page_source

    def close(self):
        if self.driver:
            self.driver.quit()
