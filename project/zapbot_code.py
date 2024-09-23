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
import re

# Configura o logging
logging.basicConfig(level=logging.INFO)

# Função para configurar o driver do Chrome com persistência de sessão
def get_driver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
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
        WebDriverWait(driver, 120).until(
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

# Função para limpar caracteres especiais do nome do contato
def limpar_nome_contato(nome):
    # Remove caracteres especiais e espaços extras
    return re.sub(r'[^\w\s]', '', nome).strip()

# Função para buscar um contato ou grupo
def buscar_contato(driver, contato):
    try:
        contato = limpar_nome_contato(contato)
        logging.info(f"Buscando o contato: {contato}")
        
        # Localizar o campo de pesquisa
        campo_pesquisa = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']"))
        )
        campo_pesquisa.click()
        campo_pesquisa.clear()  # Limpar o campo de pesquisa antes de digitar
        campo_pesquisa.send_keys(contato)
        time.sleep(2)  # Pausa para garantir que o contato seja encontrado

        # Verificar se o contato foi encontrado e selecionado
        contato_elemento = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, f'//span[@title="{contato}"]'))
        )
        contato_elemento.click()
    except Exception as e:
        logging.error(f"Erro ao buscar contato: {e}")

# Função para enviar uma mensagem de texto
def enviar_mensagem(driver, mensagem):
    try:
        logging.info("Enviando mensagem...")
        campo_mensagem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='10']"))
        )
        campo_mensagem.click()
        campo_mensagem.send_keys(mensagem)
        campo_mensagem.send_keys(Keys.ENTER)
        time.sleep(4)
        logging.info("Mensagem enviada com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem: {e}")

# Função para enviar mídia
def enviar_midia(driver, midia):
    try:
        logging.info("Iniciando o envio de mídia...")
        
        # Clicar no botão de anexo
        attach_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='plus']"))
        )
        attach_button.click()
        time.sleep(5)
        # Selecionar o arquivo de mídia
        attach_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        attach_input.send_keys(midia)
        logging.info(f"Mídia {midia} selecionada. Aguardando o upload...")

        # Aguardar o upload e o botão de envio ficar disponível
        WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='send']"))
        ).click()
        time.sleep(5)
        logging.info("Mídia enviada com sucesso.")
    except Exception as e:
        logging.error(f"Erro ao enviar mídia: {e}")

# Função para carregar contatos salvos de um arquivo
def carregar_contatos_salvos():
    contatos = {}
    try:
        with open("saved_contacts.txt", "r") as file:
            for line in file:
                if "," in line:
                    name, number = line.strip().split(",", 1)
                    contatos[name.strip()] = number.strip()
    except FileNotFoundError:
        logging.warning("Arquivo de contatos salvos não encontrado.")
    except Exception as e:
        logging.error(f"Erro ao carregar contatos salvos: {e}")
    return contatos

# Função principal para processar o envio
def processar_envio(contact_names_or_numbers, message, media_path=None):
    if len(contact_names_or_numbers) > 50:
        logging.error("O número máximo de contatos é 50.")
        return

    try:
        # Carregar contatos salvos
        contatos_salvos = carregar_contatos_salvos()

        driver = get_driver()
        start_whatsapp(driver)

        for contact_name_or_number in contact_names_or_numbers:
            if contact_name_or_number in contatos_salvos:
                phone_number = contatos_salvos[contact_name_or_number]
                logging.info(f"Nome do contato encontrado: {contact_name_or_number} -> {phone_number}")
            else:
                phone_number = contact_name_or_number
                logging.info(f"Usando número de telefone direto: {phone_number}")

            buscar_contato(driver, phone_number)
            enviar_mensagem(driver, message)

            if media_path:
                enviar_midia(driver, media_path)
        
        # Fechar o navegador se apenas um contato for selecionado
        if len(contact_names_or_numbers) == 1:
            driver.quit()  # Fecha o navegador
        
    except Exception as e:
        logging.error(f"Erro geral no processamento de envio: {e}")

# Exemplo de uso
# processar_envio(["Nome do Contato 1", "Nome do Contato 2"], "Sua mensagem", "Caminho/para/midia")
