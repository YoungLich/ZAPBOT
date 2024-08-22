import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
import time

# Configura o logging
logging.basicConfig(level=logging.INFO)

# Função para configurar o driver do Chrome com persistência de sessão
def get_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-infobars")
    
    # Persistência da sessão usando um diretório de dados do usuário
    user_data_dir = os.path.expanduser("~") + "/.chrome_user_data"
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

# Função para aguardar o escaneamento do QR code
def wait_for_qr_scan(driver):
    try:
        WebDriverWait(driver, 180).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]'))
        )
        logging.info("QR code escaneado com sucesso!")
    except Exception as e:
        logging.error("Erro ao esperar o escaneamento do QR code: " + str(e))
        driver.quit()

# Função para iniciar o WhatsApp Web
def start_whatsapp(driver):
    logging.info("Abrindo o WhatsApp Web...")
    driver.get('https://web.whatsapp.com/')
    wait_for_qr_scan(driver)

# Função para buscar um contato ou grupo
def buscar_contato(driver, contato):
    try:
        logging.info(f"Buscando o contato: {contato}")
        campo_pesquisa = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']"))
        )
        campo_pesquisa.click()
        campo_pesquisa.send_keys(contato)
        campo_pesquisa.send_keys(Keys.ENTER)
    except Exception as e:
        logging.error(f"Erro ao buscar contato: {e}")

# Função para enviar uma mensagem de texto
def enviar_mensagem(driver, mensagem):
    try:
        logging.info("Enviando mensagem...")
        campo_mensagem = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='10']"))
        )
        campo_mensagem.click()
        time.sleep(2)
        campo_mensagem.send_keys(mensagem)
        campo_mensagem.send_keys(Keys.ENTER)
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem: {e}")

# Função para enviar mídia
# Função para enviar mídia
def enviar_midia(driver, midia):
    try:
        logging.info("Iniciando o envio de mídia...")
        
        # Clicar no botão de anexo
        attach_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='plus']"))
        )
        attach_button.click()
        
        # Selecionar o arquivo de mídia
        attach_input = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        attach_input.send_keys(midia)
        logging.info(f"Mídia {midia} selecionada. Aguardando o upload...")
        
        # Aguardar o upload e o botão de envio ficar disponível
        time.sleep(5)  # Ajuste conforme necessário
        
        # Garantir que o botão de envio esteja visível e clicável
        send_button = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "span[data-icon='send']"))
        )
        send_button.click()
        time.sleep(3)
        # Usar JavaScript para clicar no botão de envio
        driver.execute_script("arguments[0].click();", send_button)
        logging.info("Mídia enviada com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao enviar mídia: {e}")

# Função principal para processar o envio
def processar_envio(phone_number, message, media_path=None):
    try:
        driver = get_driver()
        start_whatsapp(driver)

        buscar_contato(driver, phone_number)
        enviar_mensagem(driver, message)

        if media_path:
            enviar_midia(driver, media_path)

        driver.quit()  # Fecha o navegador

    except Exception as e:
        logging.error(f"Erro geral no processamento de envio: {e}")

# Exemplo de uso
# processar_envio("Número de Telefone", "Sua mensagem", "Caminho/para/midia")
