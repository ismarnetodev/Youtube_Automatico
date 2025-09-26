import pyautogui 
import webbrowser
from time import sleep
import json

try:
    with open('user.json', 'r', encoding='utf-8') as arquivo:
        dados = json.load(arquivo)
        print("Dados carregados com sucesso:")
        print(dados)

except FileNotFoundError:
    print("ERRO: O arquivo 'nomes.json' não foi encontrado. Certifique-se de que ele está na mesma pasta do script.")

except json.JSONDecodeError:
    print("ERRO: O arquivo 'nomes.json' não é um JSON válido. Verifique a sintaxe (chaves, aspas, vírgulas).")

except Exception as e:
    print(f"Ocorreu um erro inesperado durante a leitura: {e}")


webbrowser.open('https://www.tiktok.com/messages?lang=pt-BR')
sleep(15)

coordenadas = {
    'botao_login': (100, 150),
    'campo_usuario': (150, 250),
    'campo_senha': (150, 300),
    'botao_entrar': (100, 350)
}

sleep(3)
pyautogui.moveTo(coordenadas['botao_login'], duration=1)

pyautogui.click(coordenadas['botao_login'])

pyautogui.click(100, 200)  # X, Y

