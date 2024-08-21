from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import quote
import time
import pytz
from datetime import datetime
import logging
import os

logging.basicConfig(level=logging.INFO)

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--remote-debugging-port=9222")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-software-rasterizer")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-infobars")
    
    # Use a user profile to persist session data
    user_data_dir = os.path.expanduser("~") + "/.chrome_user_data"
    chrome_options.add_argument(f"--user-data-dir={user_data_dir}")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def wait_for_qr_scan(driver):
    try:
        WebDriverWait(driver, 180).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]'))
        )
        logging.info("QR code escaneado com sucesso!")
    except Exception as e:
        logging.error("Erro ao esperar o escaneamento do QR code: " + str(e))
        driver.quit()

def buscar_contato(driver, contato):
    try:
        search_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"copyable-text selectable-text")]'))
        )
        search_box.click()
        search_box.send_keys(contato)
        search_box.send_keys(Keys.ENTER)
    except Exception as e:
        logging.error(f"Erro ao buscar contato: {str(e)}")

def enviar_mensagem(driver, mensagem, contato, mensagem2):
    try:
        message_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//div[contains(@class,"copyable-text selectable-text")]'))
        )
        message_box.click()
        time.sleep(3)
        message_box.send_keys(f"{mensagem} {contato} {mensagem2}")
        message_box.send_keys(Keys.ENTER)
    except Exception as e:
        logging.error(f"Erro ao enviar mensagem: {str(e)}")

def enviar_midia(driver, midia):
    try:
        attach_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='clip']"))
        )
        attach_button.click()
        file_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
        )
        file_input.send_keys(midia)
        time.sleep(3)
        send_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='send']"))
        )
        send_button.click()
    except Exception as e:
        logging.error(f"Erro ao enviar mídia: {str(e)}")

def send_scheduled_message(phone, message, send_time):
    brt = pytz.timezone('America/Sao_Paulo')
    send_time = datetime.strptime(send_time, '%H:%M').replace(tzinfo=brt)

    while True:
        now = datetime.now(brt)
        if now >= send_time:
            break
        time.sleep(30)

    driver = get_driver()
    driver.get('https://web.whatsapp.com/')
    
    wait_for_qr_scan(driver)  # Aguarda o QR code ser escaneado antes de prosseguir

    try:
        driver.get(f'https://web.whatsapp.com/send?phone={phone}&text={quote(message)}')
        time.sleep(15)

        text_box = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[1]/div/div/p'))
        )
        text_box.send_keys(message)
        
        send_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[1]/div/div/div[2]/div[4]/div/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span'))
        )
        send_button.click()
        logging.info(f"Mensagem enviada para {phone} com sucesso!")
        time.sleep(5)
    except Exception as e:
        logging.error(f'Erro ao enviar a mensagem: {str(e)}')
    finally:
        driver.quit()

def send_file(phone, file_paths):
    driver = get_driver()
    driver.get('https://web.whatsapp.com/')
    
    wait_for_qr_scan(driver)  # Aguarda o QR code ser escaneado antes de prosseguir

    try:
        for file_path in file_paths:
            driver.get(f'https://web.whatsapp.com/send?phone={phone}')
            time.sleep(15)

            attach_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='clip']"))
            )
            attach_button.click()
            time.sleep(2)

            file_input = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file']"))
            )
            file_input.send_keys(file_path)
            time.sleep(5)

            send_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "span[data-icon='send']"))
            )
            send_button.click()
            time.sleep(5)
    except Exception as e:
        logging.error(f'Erro ao enviar o arquivo: {str(e)}')
    finally:
        driver.quit()


def send_whatsapp_messages(phone, message, message2):
    driver = get_driver()
    driver.get('https://web.whatsapp.com/')
    
    wait_for_qr_scan(driver)  # Aguarda o QR code ser escaneado antes de prosseguir

    try:
        buscar_contato(driver, phone)
        time.sleep(5)
        enviar_mensagem(driver, message, phone, message2)
    except Exception as e:
        logging.error(f'Erro ao enviar a mensagem: {str(e)}')
    finally:
        driver.quit()
