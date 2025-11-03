from .embeddings import get_embeddings_handler
from .settings import Settings

from langchain_community.document_loaders import PyPDFLoader
from langchain_postgres import PGVector
from langchain.text_splitter import RecursiveCharacterTextSplitter

settings = Settings()
embeddings = get_embeddings_handler()

def ingest_pdf():
  try:
    loader = PyPDFLoader(settings.database.pdf_path)
    documents = loader.load()
    print(f"Loaded {len(documents)} pages from the PDF.")

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
    texts = text_splitter.split_documents(documents)
    print(f"Split into {len(texts)} chunks.")

    print("Generating embeddings and storing in PostgreSQL...")
    PGVector.from_documents(
      embedding=embeddings,
      documents=texts,
      collection_name=settings.database.collection_name,
      connection=settings.database.url,
      pre_delete_collection=True,
    )
    print("PDF ingested successfully.")
  except Exception as e:
    print(f"Error during PDF ingestion: {e}")

if __name__ == "__main__":
    ingest_pdf()