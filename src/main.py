import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from loguru import logger

from src.api.routes import router as rotas_do_assistente

# Configuração de Logs
logger.add(
    "logs/app.log",
    rotation="10 MB",
    retention="7 days",
    level="INFO",
    enqueue=True
)

load_dotenv()

app = FastAPI(title="Assistente RAG de Infra")

# Log de inicialização da API
logger.info("Iniciando a aplicação Assistente RAG de Infra...")

# Inclui as rotas de routes.py no server principal
app.include_router(rotas_do_assistente)


@app.get("/")
def raiz():
    logger.info("Requisição recebida no endpoint raiz ('/')")
    return {"status": "API do Assistant RAG está online"}


@app.get("/health", status_code=200)
def health_check():
    """Endpoint de monitoramento para verificar a saúde da API e dependências."""
    chroma_path = os.getenv("CHROMA_PATH", "./chroma_db")
    
    checks = {
        "status": "healthy",
        "chroma_db": "healthy" if os.path.exists(chroma_path) else "unhealthy"
    }
    
    if checks["chroma_db"] == "unhealthy":
        logger.warning("Healthcheck executado: ChromaDB não encontrado.")
        return JSONResponse(status_code=503, content=checks)
        
    logger.info("Healthcheck executado com sucesso: API e ChromaDB OK")
    return checks