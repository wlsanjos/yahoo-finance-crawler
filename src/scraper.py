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

            time.sleep(5)

            # Passo 1: Clicar no botão 'Region'
            print("Passo 1: Procurando botão de filtro 'Region'...")
            region_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, "//button[contains(., 'Region') or contains(., 'region')]")))
            self.driver.execute_script("arguments[0].click();", region_btn)
            print("-> Menu de Região aberto!")
            time.sleep(1.5)

            # Passo 2: Clicar em 'Reset'
            print("Passo 2: Limpando filtros padrão...")
            try:
                reset_xpath = "//button[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), 'reset')]"
                reset_btns = self.driver.find_elements(By.XPATH, reset_xpath)

                if reset_btns:
                    self.driver.execute_script("arguments[0].click();", reset_btns[-1])
                    print("-> Botão 'Reset' acionado com sucesso!")
                    time.sleep(1.5)
                else:
                    print("-> Botão 'Reset' não encontrado. Tentando desmarcar 'United States' manualmente...")
                    us_label = self.driver.find_elements(By.XPATH, "//label[contains(., 'United States')]")
                    if us_label:
                        self.driver.execute_script("arguments[0].click();", us_label[0])
                        time.sleep(1)
            except Exception as e:
                print(f"-> Aviso ao tentar limpar filtros: {e}")

            # Passo 3: Buscar e Selecionar a Nova Região
            print(f"Passo 3: Buscando nova região: {region}...")
            search_input = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//input[@placeholder='Search...' or contains(@placeholder, 'Search')]")))
            search_input.clear()
            search_input.send_keys(region)
            time.sleep(1.5)

            # Selecionar a região na lista
            print(f"-> Selecionando '{region}' na lista...")
            try:
                region_item = self.wait.until(EC.presence_of_element_located((By.XPATH, f"//label[contains(., '{region}')]")))
                self.driver.execute_script("arguments[0].click();", region_item)
            except Exception as e:
                print(f"Erro ao selecionar a região: {e}")
            time.sleep(1)

            # Passo 4: Clicar em Apply
            print("Passo 4: Clicando em Apply...")
            try:
                apply_btn = self.driver.find_element(By.XPATH, "//button[contains(., 'Apply')]")
                self.driver.execute_script("arguments[0].click();", apply_btn)
            except Exception as e:
                print(f"Aviso: Botão Apply não encontrado ({e})")

            # Passo 5: Atualizar a tabela principal
            print("Passo 5: Filtro aplicado! Aguardando carregamento da tabela...")
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

    def go_to_next_page(self) -> bool:
        """
        Tenta localizar e clicar no botão de 'Próxima Página' (Next) usando data-testid.
        """
        from selenium.webdriver.common.by import By
        import time

        print("-> Verificando se há mais páginas...")
        try:
            # 1. Tentar capturar o texto de paginação ATUAL
            current_pagination_text = ""
            try:
                pag_elems = self.driver.find_elements(By.XPATH, "//div[contains(text(), 'of ')]")
                for el in pag_elems:
                    txt = el.text.strip()
                    if "of" in txt and any(c.isdigit() for c in txt):
                        current_pagination_text = txt
                        break
            except:
                pass

            next_btn = None
            btns = self.driver.find_elements(By.XPATH, "//button[@data-testid='next-page-button']")
            if not btns:
                btns = self.driver.find_elements(By.XPATH, "//button[@aria-label='Next' or @title='Next']")

            # 3. Interagir com o botão
            if btns:
                next_btn = btns[0]
                is_disabled = next_btn.get_attribute("disabled") is not None or "disabled" in next_btn.get_attribute("class")
                if is_disabled:
                    print("-> Botão Next desabilitado. Fim da lista alcançado.")
                    return False

                self.driver.execute_script("arguments[0].click();", next_btn)
                time.sleep(1.5)

                # 4. Aguardar a página mudar
                if current_pagination_text:
                    print(f"-> Clicado em Next. Aguardando a tabela mudar de '{current_pagination_text}'...")
                    for _ in range(10):
                        time.sleep(1)
                        if self._check_pagination_changed(current_pagination_text):
                            print("-> Página virou com sucesso!")
                            time.sleep(1)
                            return True

                    print("-> Aviso: O texto da paginação não mudou. Assumindo fim da lista por segurança.")
                    return False
                else:
                    time.sleep(4)
                    return True

            print("-> Botão de próxima página não encontrado no HTML. Assumindo página única.")
            return False

        except Exception as e:
            print(f"-> Erro ao tentar mudar de página: {e}")
            return False

    def _check_pagination_changed(self, old_text: str) -> bool:
        """
        Verifica se o texto do contador mudou usando as DIVs.
        """
        from selenium.webdriver.common.by import By
        try:
            pag_elems = self.driver.find_elements(By.XPATH, "//div[contains(text(), 'of ')]")
            for el in pag_elems:
                txt = el.text.strip()
                if "of" in txt and any(c.isdigit() for c in txt):
                    if txt != old_text:
                        return True
            return False
        except:
             return False

    def maximize_rows_per_page(self):
        """
        Altera a visualização da tabela para exibir 100 registros por página.
        """
        from selenium.webdriver.common.by import By
        from selenium.webdriver.support import expected_conditions as EC
        import time

        print("\n--- Otimizando a Paginação ---")
        print("-> Alterando visualização para 100 linhas por página...")
        try:
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(1)

            dropdown_xpath = "//*[contains(text(), 'Rows per page')]/parent::*//button"
            dropdown_btn = self.wait.until(EC.presence_of_element_located((By.XPATH, dropdown_xpath)))

            self.driver.execute_script("arguments[0].click();", dropdown_btn)
            time.sleep(1)

            option_100_xpath = "//span[text()='100'] | //div[text()='100'] | //li[contains(., '100')]"
            option_100 = self.wait.until(EC.presence_of_element_located((By.XPATH, option_100_xpath)))
            self.driver.execute_script("arguments[0].click();", option_100)

            print("-> Layout alterado para 100 linhas! Carregando a super tabela...")
            time.sleep(4)

            self.driver.execute_script("window.scrollTo(0, 0);")

        except Exception as e:
            print(f"-> Aviso: Não foi possível maximizar as linhas. Detalhe: {e}")
            self.driver.execute_script("window.scrollTo(0, 0);")
