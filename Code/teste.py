import time
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoAlertPresentException, UnexpectedAlertPresentException, StaleElementReferenceException, TimeoutException

# Função para ler a planilha Excel
def carregar_processos(file_path):
    df = pd.read_excel(file_path)  # Supondo que a primeira coluna contém os números dos processos
    processos = df.iloc[:, 0].tolist()  # Carregar a primeira coluna com os processos
    return processos

# Função para excluir um processo no site
def excluir_processo(driver, numero_processo):
    try:
        wait = WebDriverWait(driver, 10)
        
        # Localizar e interagir com o campo de busca
        campo_busca = wait.until(EC.presence_of_element_located((By.ID, 'j_id148:inputNumeroProcesso-inputNumeroProcessoDecoration:inputNumeroProcesso-inputNumeroProcesso')))
        campo_busca.clear()
        campo_busca.send_keys(numero_processo)
        campo_busca.send_keys(Keys.ENTER)

        # Aguarda o botão de exclusão aparecer e clicar
        botao_excluir = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="j_id175:j_id179:0:excluiProcessoButton"]')))
        botao_excluir.click()

        # Aguarda o alerta e clica em "OK"
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alerta = driver.switch_to.alert
        alerta.accept()  # Clica no "OK" no alerta

        return "Excluído com sucesso"
    except (StaleElementReferenceException, TimeoutException) as e:
        print(f"Erro ao tentar excluir o processo {numero_processo}: {e}")
        return "Erro: Tentando novamente..."
    except UnexpectedAlertPresentException:
        return "Erro: Alerta inesperado presente"
    except NoAlertPresentException:
        return "Erro: Nenhum alerta presente ao tentar excluir"
    except Exception as e:
        print(f"Erro ao excluir o processo {numero_processo}: {e}")
        return f"Erro: {str(e)}"

# Função principal para login e navegação
def automatizar_pje(username, password, processos_planilha, caminho_resultado):
    # Configura o ChromeDriver
    service = Service(executable_path=ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    # Acessa a página de login do PJe
    driver.get('https://pje1g.trf3.jus.br/pje/login.seam')

    # Troca para o iframe do Keycloak
    frame_correta = driver.find_element(By.XPATH, '//*[@id="ssoFrame"]')
    driver.switch_to.frame(frame_correta)

    wait = WebDriverWait(driver, 10)
    campo_usuario = wait.until(EC.presence_of_element_located((By.ID, 'username')))
    campo_senha = driver.find_element(By.ID, 'password')

    campo_usuario.send_keys(username)
    campo_senha.send_keys(password)

    # Clica no botão de login
    botao_login = driver.find_element(By.ID, 'kc-login')
    botao_login.click()

    # Espera pelo redirecionamento após o login
    time.sleep(5)

    # Acessa diretamente a página de Push após o login
    driver.get('https://pje1g.trf3.jus.br/pje/Push/listView.seam')

    # Criar uma lista para armazenar os resultados
    resultados = []

    # Itera sobre os processos da planilha e exclui no sistema
    for processo in processos_planilha:
        status = excluir_processo(driver, processo)
        resultados.append({"Processo": processo, "Status": status})

    # Converter a lista de resultados em DataFrame
    df_resultados = pd.DataFrame(resultados)

    # Salva a planilha de resultados
    try:
        df_resultados.to_excel(caminho_resultado, index=False)
        print(f"Planilha de resultados salva com sucesso em {caminho_resultado}.")
    except Exception as e:
        print(f"Erro ao salvar a planilha de resultados: {e}")

    # Fecha o navegador ao final
    driver.quit()

if __name__ == "__main__":
    # Substitua pelo caminho da sua planilha
    caminho_planilha = 'C:/Users/52312819805/Desktop/BITBOOP/Code/delete_push.xlsx'
    caminho_resultado = 'C:/Users/52312819805/Desktop/BITBOOP/Code/resultado_exclusao_processos.xlsx'
    
    # Carregar processos da planilha
    processos_planilha = carregar_processos(caminho_planilha)
    
    # Informações de login
    usuario = '52312819805'
    senha = 'Eg@5044326'

    # Chama a função principal
    automatizar_pje(usuario, senha, processos_planilha, caminho_resultado)
