import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import PromptTemplate
from langchain_qdrant import QdrantVectorStore
from langchain_openai import ChatOpenAI
import streamlit as st

load_dotenv(dotenv_path=".env", override=True)

# Interface do ChatBot
st.title('Chat LAMFO x Proteômica')
st.logo('./assets/logo-lamfo.png', size='large')
input = st.chat_input("Digite sua pergunta")

# Configuração ChatBot
base_prompt_content = open("./prompts/base.md").read()
base_prompt = PromptTemplate.from_template(base_prompt_content)
if "messages_for_model" not in st.session_state:
    st.session_state.messages_for_model = [
        {
            "role": "system",
            "content": "Você é um assistente de pesquisa que ajuda a encontrar informações sobre proteômica"
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

def processa_mensagem():
    resposta = ''
    for chunk in model.stream(st.session_state.messages_for_model):
        resposta += chunk.content
        yield chunk
    st.session_state.messages.append({"role": "assistant", "content": resposta})
    st.session_state.messages_for_model.append({"role": "assistant", "content": resposta})
    

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
    st.session_state.messages_for_model.append({"role": "user", "content": prompt})
    
    with st.chat_message("assistant"):
        st.write_stream(processa_mensagem())

    # st.session_state.messages.append({"role": "assistant", "content": resposta})
    # st.session_state.messages_for_model.append({"role": "assistant", "content": resposta})
    # st.chat_message("assistant").markdown(resposta)