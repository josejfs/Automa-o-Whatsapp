# Projeto Automação Envio de Mensagens

Este projeto é uma aplicação para gerenciamento de mensagens e clientes usando PySimpleGUI e SQLite, com integração para envio de mensagens via WhatsApp.

## Funcionalidades

- Cadastrar mensagens personalizadas
- Exibir clientes e mensagens cadastradas
- Editar registros de clientes e mensagens
- Enviar mensagens do WhatsApp para clientes usando PyWhatKit
- Interface gráfica amigável usando PySimpleGUI

## Instalação

### Pré-requisitos

Certifique-se de ter o Python instalado (versão 3.6 ou superior).

Instale as dependências necessárias usando pip:

```bash
pip install PySimpleGUI sqlite3 mysql-connector pywhatkit pyautogui
```

###Interface Gráfica

A interface principal permite:

- Cadastrar Mensagens: Digitar e cadastrar uma nova mensagem.
- Exibir Clientes: Exibir todos os clientes cadastrados.
- Exibir Mensagens: Exibir todas as mensagens cadastradas.
- Editar Cliente: Abrir uma interface para editar registros de clientes e mensagens.
- Enviar Mensagem: Iniciar o processo de envio de mensagens do WhatsApp.
- Inserir Manualmente: Inserir um novo cliente manualmente.
- Limpar Output: Limpar a área de output.
- Envio de Mensagens
- Ao clicar em "Enviar Mensagem", uma nova janela será aberta onde você poderá selecionar a mensagem a ser enviada e a imagem opcional para ser anexada. O envio é automatizado utilizando PyWhatKit e PyAutoGUI para localizar o botão de envio do WhatsApp.

###Contribuição

Sinta-se à vontade para contribuir com este projeto enviando pull requests. Para grandes mudanças, abra uma issue primeiro para discutir o que você gostaria de mudar.
