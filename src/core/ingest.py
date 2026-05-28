import os
# Define User Agent Global a fim de evitar bloqueios do WebBaseLoader
os.environ["USER_AGENT"] = "AssistenteRAG-DevOps/1.0"

from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader, WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings  # Local, gratuito e infalível
from langchain_chroma import Chroma

# Caminhos onde ficam os arquivos do projeto
RAW_DATA_DIR = "data/raw/"
PROCESSED_DATA_DIR = "data/processed/"
 
def ingest_docs():
    print("Iniciando a indexação de docs de Infraestrutura...")
    
    # Extração de dados WEB via Url
    web_urls = [
        "https://docs.aws.amazon.com/pt_br/index.html",
        "https://docs.docker.com/get-started/",
        "https://git-scm.com/doc"
    ]

    web_loader = WebBaseLoader(web_urls)
    web_docs = web_loader.load() # Carrega o HTML transformando em chunks de texto

    # Extração de dados de PDFs locais = vindos da pasta data/raw/
    pdf_loader = DirectoryLoader(RAW_DATA_DIR, glob="./*.pdf", loader_cls=PyPDFLoader)
    pdf_docs = pdf_loader.load()

    all_docs = web_docs + pdf_docs # Combina Web e Pdf em uma lista

    if not all_docs:
        print("Nenhum documento para referência encontrado para processar")
        return
    
    # Chunking: Divide textos longos em pedaços menores (chunks) para se adequar a LLM
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,  # Máx de caracteres por pedaço de texto
        chunk_overlap=150, # Manutenção de caracteres de sobreposição a fim de evitar perda de contexto
    )
       
    chunks = text_splitter.split_documents(all_docs)

    # Vetorização Local: Instancia  o modelo open-source no processador local para criar vetores numéricos
    print("Carregando modelo de embeddings local (HuggingFace)...")
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Armazenamento: Cria o DB Chroma, gera embeddings dos chunks e salva em disco
    print(f"Salvando {len(chunks)} pedaços de texto no ChromaDB...")
    db = Chroma.from_documents(
        documents = chunks,
        embedding = embeddings,
        persist_directory = PROCESSED_DATA_DIR # Pasta para base de dados vetorial
    )
    print("Indexação concluída com sucesso!")

if __name__ == "__main__":
    ingest_docs()