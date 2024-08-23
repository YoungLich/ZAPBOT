from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import openpyxl
from openpyxl import Workbook
from time import sleep
import sys
from pathlib import Path

def formatar_processo(proc):
    s = ''.join(filter(str.isdigit, proc))
    if len(s) < 20:
        s = s.zfill(20)
    return f"{s[:7]}-{s[7:9]}.{s[9:13]}.{s[13:14]}.{s[14:16]}.{s[16:20]}"

def ler_arquivos_exclusao(arquivo_exclusao):
    processos = []
    try:
        workbook = openpyxl.load_workbook(arquivo_exclusao)
        planilha = workbook.active
        for linha in planilha.iter_rows(min_row=2, values_only=True):
            processo = formatar_processo(linha[0])
            processos.append(processo)
    except FileNotFoundError:
        print(f"Arquivo '{arquivo_exclusao}' não encontrado.")
        sys.exit(1)
    return processos

def escrever_arquivo(processo, msg):
    arquivo_resultado = Path(__file__).parent / 'Excluidos.xlsx'
    try:
        if arquivo_resultado.exists():
            wb = openpyxl.load_workbook(arquivo_resultado)
        else:
            wb = Workbook()
            wb.active.title = "Excluídos"
            wb.active.append(["Processo", "Mensagem"])

        planilha = wb.active
        planilha.append([processo, msg])
        wb.save(arquivo_resultado)
        print(f"{processo}: {msg}")
    except Exception as e:
        print(f"Erro ao escrever no arquivo: {e}")

def excluir_processos(username, password, arquivo_exclusao):
    pass
    # Configurações do navegador
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.page_load_strategy = 'normal'
    options.add_experimental_option("detach", True)

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(options=options, service=service)

    # Abrindo Site e fazendo login
    url_pje = "https://pje1g.trf3.jus.br/pje/login.seam"
    url_push = "https://pje1g.trf3.jus.br/pje/Push/listView.seam"

    driver.get(url_pje)
    frame_correto = driver.find_element(By.XPATH, '//*[@id="ssoFrame"]')
    driver.switch_to.frame(frame_correto)

    driver.find_element(By.ID, 'username').send_keys(username)
    driver.find_element(By.ID, 'password').send_keys(password)
    sleep(2)
    driver.find_element(By.ID, 'kc-login').click()

    try:
        WebDriverWait(driver, 10).until(EC.url_to_be(url_push))
        print("Login bem-sucedido e redirecionado para a página do Push.")
    except Exception as e:
        print(f"Erro durante o login ou redirecionamento: {e}")
        driver.quit()
        sys.exit(1)

    driver.get(url_push)
    print(f"Redirecionado para {url_push}")

    processos_para_excluir = ler_arquivos_exclusao(arquivo_exclusao)

    for processo in processos_para_excluir:
        try:
            driver.get(url_push)
            input_processo = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[@id="j_id169:j_id173:j_id178"]'))
            )
            input_processo.send_keys(processo)
            input_processo.send_keys(Keys.RETURN)

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, f'//*[contains(text(), "{processo}")]'))
            )
            botao_excluir = driver.find_element(By.XPATH, '//*[@id="j_id169:j_id173:j_id178"]')
            botao_excluir.click()

            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "Operação concluída com sucesso.")]'))
            )
            escrever_arquivo(processo, "Excluído com sucesso")
        except Exception as e:
            escrever_arquivo(processo, f'Erro ao excluir: {e}')

    driver.quit()
