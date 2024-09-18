import time
import os
import pandas as pd
import json
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, StaleElementReferenceException
from webdriver_manager.chrome import ChromeDriverManager

def save_login_data(username, password):
    data = {"username": username, "password": password}
    with open("login_data.json", "w") as file:
        json.dump(data, file)

def load_login_data():
    try:
        with open("login_data.json", "r") as file:
            data = json.load(file)
            return data.get("username", ""), data.get("password", "")
    except FileNotFoundError:
        return "", ""

def carregar_processos(file_path):
    df = pd.read_excel(file_path)
    processos = df.iloc[:, 0].tolist()
    return processos

def incluir_processo(driver, numero_processo):
    try:
        wait = WebDriverWait(driver, 25)
        campo_busca = wait.until(EC.visibility_of_element_located((By.ID, 'j_id148:inputNumeroProcesso-inputNumeroProcessoDecoration:inputNumeroProcesso-inputNumeroProcesso')))
        campo_busca.clear()
        campo_busca.send_keys(numero_processo)
        campo_busca.send_keys(Keys.ENTER)
        while True:
            try:
                botao_incluir = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="j_id175:j_id179:0:incluiProcessoButton"]')))
                botao_incluir.click()
                break
            except StaleElementReferenceException:
                continue
        WebDriverWait(driver, 10).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        return f"Processo {numero_processo} incluído com sucesso"
    except TimeoutException as e:
        print(f"Erro ao incluir o processo {numero_processo}: {e}")
        return f"Erro ao incluir o processo {numero_processo}: {e}"
    except ElementNotInteractableException as e:
        print(f"Elemento não interativo para o processo {numero_processo}: {e}")
        return f"Elemento não interativo para o processo {numero_processo}: {e}"
    except Exception as e:
        print(f"Erro inesperado ao incluir o processo {numero_processo}: {e}")
        return f"Erro inesperado ao incluir o processo {numero_processo}: {e}"

def automatizar_pje(username, password, processos_planilha, result_path):
    options = Options()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    try:
        driver.get('https://pje1g.trf3.jus.br/pje/login.seam')
        frame_correta = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ssoFrame"]')))
        driver.switch_to.frame(frame_correta)

        username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'username')))
        username_input.send_keys(username)
        password_input = driver.find_element(By.ID, 'password')
        password_input.send_keys(password)
        driver.find_element(By.ID, 'kc-login').click()

        # Aguarda redirecionamento para a página principal
        WebDriverWait(driver, 10).until(EC.url_contains('pje1g.trf3.jus.br/pje/Push/listView.seam'))

        driver.get('https://pje1g.trf3.jus.br/pje/Push/listView.seam')
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="pushTab_lbl"]')))

        resultados = []

        for processo in processos_planilha:
            status = incluir_processo(driver, processo)
            resultados.append({"Processo": processo, "Status": status})

        df_resultados = pd.DataFrame(resultados)

        os.makedirs(os.path.dirname(result_path), exist_ok=True)

        try:
            df_resultados.to_excel(result_path, index=False)
            print(f"Planilha de resultados salva com sucesso em {result_path}.")
        except Exception as e:
            print(f"Erro ao salvar a planilha de resultados: {e}")

    finally:
        driver.quit()

def incluir_processos(username, password, planilha_path, result_path):
    processos_planilha = carregar_processos(planilha_path)
    automatizar_pje(username, password, processos_planilha, result_path)

if __name__ == "__main__":
    usuario, senha = load_login_data()
    if not usuario or not senha:
        usuario = ''  
        senha = ''     

    planilha_path = 'C:/Users/52312819805/Desktop/BITBOOP/Code/Pushnator/Incluir_Push.xlsx'
    result_path = 'C:/Users/52312819805/Desktop/BITBOOP/output/Incluidos/resultado_inclusao_processos.xlsx'
    incluir_processos(usuario, senha, planilha_path, result_path)
