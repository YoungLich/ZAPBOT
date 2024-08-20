from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote
import openpyxl
import time
import pytz
from datetime import datetime
import os

# Caminho para o diretório de perfil do Chrome
PROFILE_PATH = "profile"

def get_driver():
    chrome_options = Options()
    chrome_options.add_argument(f"user-data-dir={PROFILE_PATH}")  # Diretório do perfil do usuário
    chrome_options.add_argument("--profile-directory=Default")  # Diretório do perfil padrão
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    # Atualize o caminho para o chromedriver
    service = Service(executable_path="C:\\Program Files\\chromedriver.exe")
    driver = webdriver.Chrome(service=service, options=chrome_options)
    return driver

def send_whatsapp_messages():
    driver = get_driver()
    driver.get('https://web.whatsapp.com/')
    
    # Espera até que o usuário tenha escaneado o QR Code uma vez
    WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="pane-side"]'))
    )

    workbook = openpyxl.load_workbook('clientes.xlsx')
    pagina_clientes = workbook['Plan1']

    for linha in pagina_clientes.iter_rows(min_row=2):
        nome = linha[0].value
        telefone = linha[1].value
        mensagem = f'Olá {nome}, é apenas um teste'
        link_mens_whats = f'https://web.whatsapp.com/send?phone={telefone}&text={quote(mensagem)}'

        driver.get(link_mens_whats)
        time.sleep(10)

        try:
            send_button = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span'))
            )
            send_button.click()
            time.sleep(5)
        except Exception as e:
            print(f'Não foi possível enviar a mensagem para {nome}: {str(e)}')
            with open('erros.csv', 'a', newline='', encoding='UTF-8') as arquivo:
                arquivo.write(f'{nome}, {telefone}\n')

    driver.quit()

def send_scheduled_message(phone, message, send_time):
    # Define o fuso horário de Brasília
    brt = pytz.timezone('America/Sao_Paulo')

    # Converte o tempo de envio para um objeto datetime com fuso horário
    send_time = datetime.strptime(send_time, '%H:%M').replace(tzinfo=brt)
    print(f'Tempo agendado: {send_time}')

    while True:
        # Obtém o tempo atual em Brasília
        now = datetime.now(brt)
        print(f'Tempo atual: {now}')

        if now >= send_time:
            break

        # Espera até o próximo minuto
        time.sleep(30)

    driver = get_driver()
    driver.get(f'https://web.whatsapp.com/send?phone={phone}&text={quote(message)}')
    time.sleep(15)

    try:
        send_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span'))
        )
        send_button.click()
        time.sleep(5)
    except Exception as e:
        print(f'Não foi possível enviar a mensagem: {str(e)}')
    finally:
        driver.quit()

def send_file(phone, file_path):
    driver = get_driver()
    driver.get(f'https://web.whatsapp.com/send?phone={phone}')
    time.sleep(15)

    try:
        attach_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/header/div[3]/div/div[2]/div/span'))
        )
        attach_button.click()
        time.sleep(2)

        # Botão para selecionar arquivos
        file_input = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="main"]/header/div[3]/div/div[2]/div/span/input'))
        )
        file_input.send_keys(file_path)
        time.sleep(5)

        send_button = WebDriverWait(driver, 30).until(
            EC.element_to_be_clickable((By.XPATH, '//*[@id="main"]/footer/div[1]/div/span[2]/div/div[2]/div[2]/button/span'))
        )
        send_button.click()
        time.sleep(5)
    except Exception as e:
        print(f'Não foi possível enviar o arquivo para {phone}: {str(e)}')
    finally:
        driver.quit()
