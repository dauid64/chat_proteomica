import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_core.messages import SystemMessage
from langchain_qdrant import QdrantVectorStore
from langchain_openai import ChatOpenAI
import streamlit as st

load_dotenv(dotenv_path=".env", override=True)

base_prompt = PromptTemplate.from_template(
    """
    Responda a pergunta abaixo de acordo com base no contexto passado para você. O contexto será passado em formato JSON
    onde teremos 3 referências para sua resposta, as chaves "source" indica o caminho do arquivo juntamente com
    o nome do arquivo PDF, "page" que é a página localizada no arquivo PDF e "page_label" que é a página que está
    sendo indicada no próprio texto, "page_content" é o conteúdo do arquivo, 
    caso tenha alguma outra chave pode somente ignorar. Lembre-se de sempre que usar
    uma referência do contexto que está utilizando e responder em formato markdown.

    Contexto: {context}

    Pergunta: {question}
    """
)

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": "Você é um assistente de pesquisa que ajuda a encontrar informações sobre proteomica"
        }
    ]

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

    resposta = model.invoke(st.session_state.messages)
    st.session_state.messages.append({"role": "assistant", "content": resposta.content})

    st.chat_message("assistant").markdown(resposta.content)