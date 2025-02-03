import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage
from langchain_qdrant import QdrantVectorStore
from langchain_openai import ChatOpenAI
import streamlit as st

load_dotenv(dotenv_path=".env", override=True)

base_prompt_content = open("./prompts/base.md").read()

base_prompt = PromptTemplate.from_template(base_prompt_content)

if "messages_for_ia" not in st.session_state:
    st.session_state.messages_for_ia = [
        {
            "role": "system",
            "content": "Você é um assistente de pesquisa que ajuda a encontrar informações sobre proteomica"
        }
    ]

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

model = ChatOpenAI(model="gpt-4o-mini", api_key=os.getenv('OPENAI_KEY'))

embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=os.getenv('OPENAI_KEY'))

vector_store = QdrantVectorStore.from_existing_collection(
    url=os.getenv('QDRANT_URL'),
    api_key=os.getenv('QDRANT_KEY'),
    embedding=embeddings,
    collection_name='proteomica',
)

input = st.chat_input("Digite sua pergunta:")

if input:
    st.chat_message("user").markdown(input)
    st.session_state.messages.append({"role": "user", "content": input})
    documentos = vector_store.similarity_search(input, k=3)

    documentos_json = []
    for documento in documentos:
        documento_json = {
            "page_content": documento.page_content,
            "source": documento.metadata['source'],
            "page_label": documento.metadata["page_label"],
            "page": documento.metadata["page"],
        }
        documentos_json.append(documento_json)

    prompt = base_prompt.format(context=documentos_json, question=input)

    st.session_state.messages_for_ia.append({"role": "assistant", "content": prompt})

    resposta = model.invoke(st.session_state.messages_for_ia)
    st.session_state.messages.append({"role": "assistant", "content": resposta.content})
    st.session_state.messages_for_ia.append({"role": "assistant", "content": resposta.content})
    st.chat_message("assistant").markdown(resposta.content)