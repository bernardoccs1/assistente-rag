import time
from fastapi import APIRouter, HTTPException
from loguru import logger
from pydantic import BaseModel

from src.core.rag_engine import get_infra_assistant_chain

router = APIRouter()


class PerguntaSchema(BaseModel):
    texto: str


@router.post("/perguntar")
def perguntar(dados: PerguntaSchema):
    logger.info(f"Nova pergunta recebida: '{dados.texto}'")
    inicio = time.time()

    try:
        # 1. Obtém a cadeia do RAG e executa a pergunta
        chain = get_infra_assistant_chain()
        resultado = chain.invoke(dados.texto)

        # 2. Trata a resposta (caso o retorno seja um objeto complexo ou string simples)
        if isinstance(resultado, dict):
            resposta_texto = resultado.get("result", resultado.get("answer", str(resultado)))
        else:
            resposta_texto = str(resultado)

        tempo_total = round(time.time() - inicio, 2)
        logger.info(f"Resposta gerada em {tempo_total}s com sucesso.")

        return {
            "resposta": resposta_texto,
            "tempo_execucao": tempo_total
        }

    except Exception as e:
        logger.error(f"Erro ao processar a pergunta: {str(e)}")
        raise HTTPException(
            status_code=500, detail="Erro interno ao processar a consulta RAG."
        )