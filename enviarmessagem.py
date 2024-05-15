import sqlite3
import pywhatkit
import time
import pyautogui
import os
import platform
import threading
import ctypes
import re
import PySimpleGUI as sg

# Define o tamanho da janela de console para ocupar toda a tela
ctypes.windll.kernel32.SetConsoleDisplayMode(ctypes.windll.kernel32.GetStdHandle(-11), 1, None)

###########################################################
# VARIÁVEIS GLOBAIS
###########################################################

WAIT_TIME = 10

###########################################################
# FUNÇÃO ENVIAR MENSAGENS
###########################################################
def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def enviar_mensagens(window, msg_id, imagem):
    # Conectar ao banco de dados SQLite
    conexao = sqlite3.connect('db/lib.db')
    cursor = conexao.cursor()

    # Selecionar os dados dos clientes
    cursor.execute('SELECT id, nome, telefone FROM clientes')
    clientes = cursor.fetchall()

    # Selecionar as mensagens
    cursor.execute('SELECT id, msg FROM msg')
    mensagens = cursor.fetchall()

    mensagem_selecionada = None
    for mensagem in mensagens:
        if mensagem[0] == msg_id:
            mensagem_selecionada = mensagem[1]
            break

    if mensagem_selecionada is None:
        window.write_event_value('-THREAD-', "ID de mensagem inválido.")
        return

    # Cria uma thread para executar a função de envio de mensagens
    def enviar_mensagens_thread():
        for cliente in clientes:
            telefone = "+55" + re.sub(r'\s+|-|\(|\)', '', cliente[2])  # Adiciona o código do país

            mensagem_personalizada = mensagem_selecionada.replace("xxxx", cliente[1]).replace("XXXX", cliente[1])

            mensagem = f"""
###############################################
ID: {cliente[0]}
-----------------------------------------------
CLIENTE: {cliente[1]}
-----------------------------------------------
TELEFONE: {telefone}
-----------------------------------------------
MENSAGEM: {mensagem_personalizada}
-----------------------------------------------
IMAGEM: {imagem}
###############################################
            """
            window.write_event_value('-THREAD-', mensagem)

            pywhatkit.sendwhats_image(telefone, imagem, mensagem_personalizada)

            time.sleep(WAIT_TIME)

            # Localiza o botão de envio na tela e clica nele
            send_button_position = pyautogui.locateCenterOnScreen('send_button_image.png')
            if send_button_position:
                pyautogui.click(send_button_position)
            else:
                window.write_event_value('-THREAD-', "Botão de envio não encontrado na tela.")

            time.sleep(WAIT_TIME)

            pyautogui.hotkey('ctrl', 'w')

        window.write_event_value('-THREAD-', "Todas as Mensagens Foram Enviadas!!!")

    thread = threading.Thread(target=enviar_mensagens_thread)
    thread.start()

def main():
    # Conectar ao banco de dados SQLite
    conexao = sqlite3.connect('db/lib.db')
    cursor = conexao.cursor()

    # Selecionar as mensagens
    cursor.execute('SELECT id, msg FROM msg')
    mensagens = cursor.fetchall()

    # Criar layout para a janela do PySimpleGUI
    layout = [
        [sg.Text('Selecione a mensagem que deseja enviar:')],
        [sg.Listbox(values=[f"ID: {mensagem[0]} - Mensagem: {mensagem[1]}" for mensagem in mensagens], size=(50, 6), key='-MENSAGEM-', select_mode='LISTBOX_SELECT_MODE_SINGLE')],
        [sg.Text('Selecione a imagem que deseja enviar:')],
        [sg.Input(key='-IMAGEM-', size=(50, 1)), sg.FileBrowse()],
        [sg.Button('Enviar')],
        [sg.Output(size=(100, 20), key='-OUTPUT-')]
    ]

    # Criar janela do PySimpleGUI
    window = sg.Window("Dra Alicya Mendes", layout, icon='imagens/REDE.ico')

    while True:
        event, values = window.read()

        if event == sg.WINDOW_CLOSED:
            break

        if event == '-THREAD-':
            # Atualizar a área de output com a mensagem da thread
            window['-OUTPUT-'].update(values[event] + '\n', append=True)

        if event == 'Enviar':
            mensagem_selecionada = values['-MENSAGEM-']
            if mensagem_selecionada:
                mensagem_selecionada = mensagem_selecionada[0]
                imagem = values['-IMAGEM-']
                msg_id = int(re.search(r'ID: (\d+)', mensagem_selecionada).group(1))

                # Iniciar o envio de mensagens em uma nova thread
                enviar_mensagens(window, msg_id, imagem)
            else:
                sg.popup_error("Selecione uma mensagem antes de enviar.")

    window.close()

if __name__ == '__main__':
    main()