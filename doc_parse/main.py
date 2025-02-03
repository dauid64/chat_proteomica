from langchain_community.document_loaders import PyPDFLoader
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from uuid import uuid4
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path=".env", override=True)

embeddings = OpenAIEmbeddings(model="text-embedding-3-large", api_key=os.getenv('OPENAI_KEY'))

qdrant_client = QdrantClient(
    url=os.getenv('QDRANT_URL'),     
    api_key=os.getenv('QDRANT_KEY'),
)

if qdrant_client.collection_exists("proteomica"):
    qdrant_client.delete_collection("proteomica")
qdrant_client.create_collection(
    collection_name="proteomica",
    vectors_config=VectorParams(size=3072, distance=Distance.COSINE),
)


vector_store = QdrantVectorStore(
    client=qdrant_client,
    embedding=embeddings,
    collection_name="proteomica",
)

caminho_artigos= "./data/articles"
text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

for artigo in os.listdir(caminho_artigos):
    if artigo.endswith('.pdf'):
        try:
            caminho_completo = os.path.join(caminho_artigos, artigo)

            loader = PyPDFLoader(caminho_completo)

            docs = loader.load()

            splits = text_splitter.split_documents(docs)

            uuids = [str(uuid4()) for _ in range(len(splits))]

            vector_store.add_documents(splits, ids=uuids)

            print(f"✅ Processado: {caminho_completo}")

        except Exception as e:
            print(f"❌ Erro ao processar: {caminho_completo}: {e}")
            continue



