import cassio
from langchain.vectorstores.cassandra import Cassandra
from langchain_huggingface import HuggingFaceEmbeddings
from backend.config import ASTRA_DB_TOKEN, ASTRA_DB_ID

def get_vectorstore():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    # Initialize and return Cassandra vector store
    cassio.init(token=ASTRA_DB_TOKEN, database_id=ASTRA_DB_ID)
    return Cassandra(
        embedding=embeddings,
        table_name="qa_table",
        session=None,
        keyspace=None
    )
