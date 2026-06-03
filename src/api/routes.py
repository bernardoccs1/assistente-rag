from fastapi import APIRouter
from pydantic import BaseModel
from src.core.rag_engine import get_infra_assistant_chain

# Criação do roteador de rotas
router= APIRouter()

# Validação do formato que a pergunta deve chegar (pydantic)
class PerguntaSchema(BaseModel):
    texto: str

# Criação da rota que receberá as perguntas via POST
@router.post("/perguntar")
def perguntar(dados: PerguntaSchema):
    chain= get_infra_assistant_chain()
    resposta= chain.invoke(dados.texto)
    return {"texto": resposta}