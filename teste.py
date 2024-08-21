from selenium import webdriver  # pip install selenium
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager  # pip install webdriver_manager
import time

# Configura o serviço do ChromeDriver
service = Service(ChromeDriverManager().install())

# Abre o Chrome
driver = webdriver.Chrome(service=service)
driver.get('https://web.whatsapp.com/')  # abre o site Whatsapp Web
time.sleep(15)  # dá um sleep de 15 segundos, tempo para escanear o QR CODE

# Contatos/Grupos - Informar o nome(s) de Grupos ou Contatos que serão enviadas as mensagens
contatos = ['Anotações', '11949919959']

# Mensagem - Mensagem que será enviada
mensagem = 'Bom dia grupo '
mensagem2 = ' que o dia de vocês seja iluminado'

# Mídia = imagem, pdf, documento, vídeo (caminho do arquivo, lembrando que mesmo no Windows o caminho deve ser passado com barra invertida)
midia = "C:/Users/52312819805/Desktop/eu.jpg"

#Funcao que pesquisa o Contato/Grupo
def buscar_contato(contato):
    try:
        # Espera até que o campo de pesquisa esteja visível e disponível
        campo_pesquisa = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true']"))
        )
        campo_pesquisa.click()
        campo_pesquisa.send_keys(contato)
        campo_pesquisa.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Erro ao buscar contato: {e}")

#Funcao que envia a mensagem
def enviar_mensagem(mensagem, mensagem2):
    try:
        # Espera até que o campo de mensagem esteja visível e disponível
        campo_mensagem = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div[contenteditable='true'][data-tab='10']"))
        )
        campo_mensagem.click()
        time.sleep(2)  # Espera um pouco antes de enviar a mensagem
        campo_mensagem.send_keys(mensagem + contato + mensagem2)
        campo_mensagem.send_keys(Keys.ENTER)
    except Exception as e:
        print(f"Erro ao enviar mensagem: {e}")

#Funcao que envia midia como mensagem
def enviar_midia(midia):
    try:
        driver.find_element(By.CSS_SELECTOR, "span[data-icon='plus']").click()
        attach = driver.find_element(By.CSS_SELECTOR, "input[type='file']")
        attach.send_keys(midia)
        time.sleep(3)  # Espera a mídia carregar
        send = driver.find_element(By.CSS_SELECTOR, "span[data-icon='send']")
        send.click()
    except Exception as e:
        print(f"Erro ao enviar mídia: {e}")

#Percorre todos os contatos/Grupos e envia as mensagens
for contato in contatos:
    buscar_contato(contato)
    enviar_mensagem(mensagem, mensagem2)
    enviar_midia(midia)
    time.sleep(1)
