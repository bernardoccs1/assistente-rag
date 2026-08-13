import os

# Define User Agent Global a fim de evitar bloqueios do WebBaseLoader
os.environ["USER_AGENT"] = "AssistenteRAG-DevOps/1.0"

from langchain_chroma import Chroma
from langchain_community.document_loaders import (
    DirectoryLoader,
    PyMuPDFLoader,
    WebBaseLoader,
)
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Caminhos onde ficam os arquivos do projeto
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
PROCESSED_DATA_DIR = os.path.join(BASE_DIR, "data", "processed")
CHROMA_PATH = os.path.join(PROCESSED_DATA_DIR, "chroma")


def ingest_docs():
    print("Iniciando a indexação de docs de Infraestrutura...")

    # Extração de dados WEB via Url
    web_urls = [
        "https://docs.aws.amazon.com/pt_br/index.html",
        "https://docs.docker.com/get-started/",
        "https://git-scm.com/doc",
    ]

    web_loader = WebBaseLoader(web_urls)
    web_docs = web_loader.load()

    # Extração de dados de PDFs locais vindos da pasta data/raw/
    pdf_loader = DirectoryLoader(
        RAW_DATA_DIR,
        glob="**/*.pdf",
        loader_cls=PyMuPDFLoader
    )
    pdf_docs = pdf_loader.load()

    all_docs = web_docs + pdf_docs

    if not all_docs:
        print("Nenhum documento para referência encontrado para processar")
        return

    # Chunking: Divide textos longos em pedaços menores (chunks)
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=100,
    )
    chunks = text_splitter.split_documents(all_docs)

    # Vetorização Local
    print("Carregando modelo de embeddings local (HuggingFace)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Armazenamento no ChromaDB
    print(f"Salvando {len(chunks)} pedaços de texto no ChromaDB...")
    Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=CHROMA_PATH
    )
    print("Indexação concluída com sucesso!")


if __name__ == "__main__":
    ingest_docs()