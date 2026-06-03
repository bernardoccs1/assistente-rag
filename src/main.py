from dotenv import load_dotenv
load_dotenv()

import os
from src.api.routes import router as rotas_do_assistente
from fastapi import FastAPI

app = FastAPI(title= "Assistente RAG de Infra")

# Inclui as rotas de routes.py no server principal
app.include_router(rotas_do_assistente)

@app.get("/")
def raiz():
    return {"status": "API do Assistant RAG está online"}