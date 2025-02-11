import os
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from langchain_qdrant import QdrantVectorStore
from langchain.retrievers.document_compressors import FlashrankRerank
from langchain.retrievers import ContextualCompressionRetriever
from langchain.chains import RetrievalQA

class ChatAgent:
    def __init__(self, vector_store: QdrantVectorStore):
        self.llm = ChatOpenAI(temperature=0.0, model="gpt-4o-mini-2024-07-18", api_key=os.getenv('OPENAI_KEY'))
        retriever = vector_store.as_retriever(search_kwargs={"k": 5})
        compressor = FlashrankRerank(model="ms-marco-MiniLM-L-12-v2")

        self.compression_retriever = ContextualCompressionRetriever(
            base_compressor=compressor, base_retriever=retriever
        )

        prompt_template = """
            Use the following pieces of information to answer the user's question.
            If you don't know the answer, just say that you don't know, don't try to make up an answer.

            Context: {context}
            Question: {question}

            Answer the question and provide additional helpful information,
            based on the pieces of information, if applicable. Be succinct.

            Responses should be properly formatted to be easily read.
        """

        self.prompt = PromptTemplate(
            template=prompt_template,
            input_variables=["context", "question"]
        )
    
    def send_message(self, query):
        qa = RetrievalQA.from_chain_type(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.compression_retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": self.prompt, "verbose": True},
        )


        response = qa.invoke(query)

        return response

        
    
    