---
title: Chat Proteômica
emoji: 🤖
colorFrom: gray
colorTo: blue
sdk: streamlit
sdk_version: 1.41.1
app_file: app.py
pinned: false
---

# LAMFO X Lab Proteômica

A Colaboração entre os Laboratórios de Aprendizagem de Máquina em Finanças e Organização com o Laboratório de Proteômica teve como objetivo desenvolver um chat utilizando IA para responder perguntas sobre o assunto de Proteômica baseado em uma série de artigos ciêntificos que os pesquisadores do Laboratório de Proteômica coletaram.

## Estrutura
- 📂 model

    A pasta model é onde fica os objetos do projeto, no momento que foi escrito isso, somente tem o agente que se responsabiliza para realizar a conversa e recuperar os arquivos.

- 📄 app.py

    O arquivo app.py é o main do nosso projeto, ele contém a estrutura HTML e toda lógica está centrada nele.

## RAG Avançado

Utilizei a lógica de RAG Avançado para fazer a recuperação dos dados coletados, porém a lógica está separada em outro projeto chamado [doc_parse_chat_proteomica](https://github.com/dauid64/doc_parse_chat_proteomica)

