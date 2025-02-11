import os
from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore
from model.chat_agent import ChatAgent
import streamlit as st

load_dotenv(dotenv_path=".env", override=True)

# Interface do ChatBot
st.title('Chat LAMFO x Proteômica')
st.logo('./assets/logo-lamfo.png', size='large')
input = st.chat_input("Digite sua pergunta")

# Configuração ChatBot
# if "messages_for_model" not in st.session_state:
#     st.session_state.messages_for_model = []
if "messages" not in st.session_state:
    st.session_state.messages = []
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def tratar_referencias(source_documents):
    texto = "\n\nReferências: \n"
    referencias = {}
    for source_document in source_documents:
        referencia = os.path.splitext(os.path.basename(source_document.metadata['source']))[0]
        if referencia not in referencias:
            texto += f"* {os.path.splitext(os.path.basename(source_document.metadata['source']))[0]} \n"
            referencias[referencia] = True

    return texto

embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=os.getenv('OPENAI_KEY'))
vector_store = QdrantVectorStore.from_existing_collection(
    url=os.getenv('QDRANT_URL'),
    api_key=os.getenv('QDRANT_KEY'),
    embedding=embeddings,
    collection_name='proteomica',
)

agent = ChatAgent(vector_store=vector_store)

if input:
    st.chat_message("user").markdown(input)
    st.session_state.messages.append({"role": "user", "content": input})

    response = agent.send_message(input)
    # st.session_state.messages_for_model.append({"role": "user", "content": prompt})
    response["result"] += tratar_referencias(response["source_documents"])

    st.session_state.messages.append({"role": "assistant", "content": response["result"]})
    with st.chat_message("assistant"):
        st.markdown(response["result"])