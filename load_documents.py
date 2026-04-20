import os
from dotenv import load_dotenv
from langchain.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from backend.services.vector_store import get_vectorstore

# Load environment variables
load_dotenv()

def load_and_process_documents():
    # URLs to load
    urls = [
        "https://lilianweng.github.io/posts/2023-06-23-agent/",
        "https://lilianweng.github.io/posts/2023-03-15-prompt-engineering/",
        "https://lilianweng.github.io/posts/2023-10-25-adv-attack-llm/",
        "https://www.w3schools.com/python/default.asp"
    ]

    print("Loading documents...")
    # Load documents
    docs = [WebBaseLoader(url).load() for url in urls]
    docs_list = [item for sublist in docs for item in sublist]

    print("Splitting documents...")
    # Split documents
    text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
        chunk_size=512,
        chunk_overlap=0
    )
    doc_splits = text_splitter.split_documents(docs_list)

    print("Creating embeddings...")
    # Create embeddings
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print("Inserting documents into Cassandra...")
    # Create vector store (Cassandra)
    vector_store = get_vectorstore()
    vector_store.add_documents(doc_splits)

    print("Document processing and storage complete.")

if __name__ == "__main__":
    load_and_process_documents()
