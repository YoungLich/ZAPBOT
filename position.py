import pyautogui
import time

try:
    while True:
        posicao = pyautogui.position()
        print(f"A posição atual do mouse é: x={posicao.x}, y={posicao.y}")
        time.sleep(3)  # Aguardar 1 segundo antes de verificar novamente
except KeyboardInterrupt:
    print("Programa interrompido.")
