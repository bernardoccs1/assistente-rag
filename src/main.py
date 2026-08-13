from dotenv import load_dotenv
from fastapi import FastAPI

from src.api.routes import router as rotas_do_assistente

load_dotenv()

app = FastAPI(title="Assistente RAG de Infra")

# Inclui as rotas de routes.py no server principal
app.include_router(rotas_do_assistente)


@app.get("/")
def raiz():
    return {"status": "API do Assistant RAG está online"}