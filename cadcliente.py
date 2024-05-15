import PySimpleGUI as sg
import sqlite3
import os
import platform
import mysql.connector
import re
import platform
import subprocess
import pywhatkit
import time
import pyautogui
import threading
import ctypes
import subprocess

# Funções
def clear_screen():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def msg(cursor, conexao, mensagem):
    cursor.execute("INSERT INTO msg (msg) VALUES (?)", (mensagem,))
    conexao.commit()
    return "Mensagem cadastrada com sucesso!"

def exibir_clientes(cursor):
    cursor.execute("SELECT * FROM clientes")
    clientes = cursor.fetchall()
    return clientes

def exibir_mensagens(cursor):
    cursor.execute("SELECT * FROM msg")
    mensagens = cursor.fetchall()
    return mensagens

def inserir_manualmente(cursor, conexao):
    nome = sg.popup_get_text('Digite o nome:', title='Inserir Manualmente', icon='imagens/REDE.ico')
    if nome is None:  # O usuário cancelou a operação
        return
    telefone = sg.popup_get_text('Digite o telefone:', title='Inserir Manualmente', icon='imagens/REDE.ico')
    if telefone is None:  # O usuário cancelou a operação
        return

    # Aplicar máscara no telefone (XX) XXXXX-XXXX
    telefone_formatado = re.sub(r'(\d{2})(\d{5})(\d{4})', r'(\1) \2-\3', telefone)

    if nome and telefone:
        cursor.execute("INSERT INTO clientes (nome, telefone) VALUES (?, ?)",
                       (nome.upper(), telefone_formatado.upper()))
        conexao.commit()
        return "Dados inseridos com sucesso!"
    elif not nome:
        return "O campo nome é obrigatório!"
    elif not telefone:
        return "O campo telefone é obrigatório!"
#**************************************************************************************
def display_records(table):
    with sqlite3.connect('db/lib.db') as conn:
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table}")
        records = cursor.fetchall()
        return records

def delete_records(table, record_ids):
    with sqlite3.connect('db/lib.db') as conn:
        cursor = conn.cursor()
        for record_id in record_ids:
            cursor.execute(f"DELETE FROM {table} WHERE id=?", (record_id,))
        conn.commit()

def update_record(table, record_id, field1, field2=None):
    with sqlite3.connect('db/lib.db') as conn:
        cursor = conn.cursor()
        if table == 'clientes':
            cursor.execute(f"UPDATE {table} SET nome=?, telefone=? WHERE id=?", (field1, field2, record_id))
        elif table == 'msg':
            cursor.execute(f"UPDATE {table} SET msg=? WHERE id=?", (field1, record_id))
        conn.commit()

def manage_records_app():
    records_listbox = sg.Listbox(values=[], select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE, key='-RECORDS-', enable_events=True, size=(60, 10))

    layout = [[sg.Button('Show Clientes'), sg.Button('Show Mensagens')],
              [sg.Column([[records_listbox]], expand_x=True, expand_y=True)],
              [sg.Button('Edit Selected'), sg.Button('Delete Selected'), sg.Button('Exit')]]

    window = sg.Window("Dra Alicya Mendes", layout, icon='imagens/REDE.ico', resizable=True)

    current_table = None  # keep track of the current table being displayed

    while True:
        event, values = window.read()
        if event == sg.WINDOW_CLOSED or event == 'Exit':
            break
        if event == 'Show Clientes':
            current_table = 'clientes'
            window['-RECORDS-'].update(values=display_records(current_table))  # refresh the listbox
        if event == 'Show Mensagens':
            current_table = 'msg'
            window['-RECORDS-'].update(values=display_records(current_table))  # refresh the listbox
        if event == 'Delete Selected' and current_table:
            if values['-RECORDS-']:
                record_ids = [record[0] for record in values['-RECORDS-']]  # get the ids of the selected records
                delete_records(current_table, record_ids)
                window['-RECORDS-'].update(values=display_records(current_table))  # refresh the listbox
        if event == 'Edit Selected' and current_table:
            if values['-RECORDS-']:
                for record in values['-RECORDS-']:
                    if current_table == 'clientes':
                        record_id, nome, telefone = record
                        edit_layout = [[sg.Text('Nome'), sg.Input(default_text=nome, key='-FIELD1-')],
                                       [sg.Text('Telefone'), sg.Input(default_text=telefone, key='-FIELD2-')],
                                       [sg.Button('Save'), sg.Button('Cancel')]]
                    elif current_table == 'msg':
                        record_id, msg = record
                        edit_layout = [[sg.Text('Mensagem'), sg.Input(default_text=msg, key='-FIELD1-')],
                                       [sg.Button('Save'), sg.Button('Cancel')]]
                    edit_window = sg.Window('Edit Record', edit_layout, icon='imagens/REDE.ico')
                    while True:  # Event Loop
                        e, v = edit_window.read()
                        if e == sg.WINDOW_CLOSED or e == 'Cancel':
                            break
                        if e == 'Save':
                            if current_table == 'clientes':
                                update_record(current_table, record_id, v['-FIELD1-'], v['-FIELD2-'])
                            elif current_table == 'msg':
                                update_record(current_table, record_id, v['-FIELD1-'])
                            break
                    edit_window.close()
                window['-RECORDS-'].update(values=display_records(current_table))  # refresh the listbox

    window.close()
    
#*************************************************************************************

# Conexão com o SQLite
conexao = sqlite3.connect('db/lib.db')
cursor = conexao.cursor()

# Criação das tabelas
cursor.execute('''
CREATE TABLE IF NOT EXISTS clientes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    telefone TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS msg (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    msg TEXT NOT NULL
)
''')

conexao.commit()

# Interface Gráfica
layout = [
    [sg.Button("Cadastrar Mensagem"), sg.Button("Exibir Clientes"), sg.Button("Exibir Mensagens")],
    [sg.Button("Editar Cliente"), sg.Button("Enviar Mensagem"), sg.Button("Inserir Manualmente")],
    [sg.Output(size=(80, 20), key='-OUTPUT-')],
    [sg.Button('Limpar Output'), sg.Exit()]
]

window = sg.Window("Dra Alicya Mendes", layout, icon='imagens/REDE.ico')

while True:
    event, values = window.read()

    if event in (None, 'Exit'):
        break
    elif event == "Cadastrar Mensagem":
        print('Digite a mensagem + XXXX. Esse XXXX será substituído pelo nome do cliente.')
        mensagem = sg.popup_get_text('Digite a mensagem:', icon='imagens/REDE.ico')
        if mensagem:
            result = msg(cursor, conexao, mensagem)
            print(result)
        elif mensagem is None:
            continue
        else:
            print("Preencha a mensagem corretamente!")
    elif event == "Exibir Clientes":
        clientes = exibir_clientes(cursor)
        for cliente in clientes:
            print(cliente)
    elif event == "Exibir Mensagens":
        mensagens = exibir_mensagens(cursor)
        for mensagem in mensagens:
            print(mensagem)
    elif event == "Editar Cliente":
        if __name__ == '__main__':
            manage_records_app()
    elif event == "Enviar Mensagem":
        subprocess.Popen(['python', 'enviarmessagem.py'])
    elif event == "Inserir Manualmente":
        result = inserir_manualmente(cursor, conexao)
        if result is not None:
            print(result)
    elif event == 'Limpar Output':
        window['-OUTPUT-'].update('')

conexao.close()
window.close()