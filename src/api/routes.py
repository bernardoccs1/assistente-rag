import time

from fastapi import APIRouter, Depends, HTTPException, Request
from loguru import logger
from pydantic import BaseModel, Field
from slowapi import Limiter
from slowapi.util import get_remote_address

from src.core.rag_engine import get_infra_assistant_chain
from src.core.security import require_api_key, validate_question

router = APIRouter()
limiter = Limiter(key_func=get_remote_address)


class PerguntaSchema(BaseModel):
    texto: str = Field(..., min_length=1)


@router.post("/perguntar")
@limiter.limit("10/minute")
def perguntar(
    request: Request,
    dados: PerguntaSchema,
    _: str = Depends(require_api_key),
):
    pergunta = validate_question(dados.texto)
    logger.info("Nova pergunta recebida com {} caracteres", len(pergunta))
    inicio = time.time()

    try:
        chain = get_infra_assistant_chain()
        resultado = chain.invoke(pergunta)

        if isinstance(resultado, dict):
            resposta_texto = resultado.get("result", resultado.get("answer", str(resultado)))
        else:
            resposta_texto = str(resultado)

        tempo_total = round(time.time() - inicio, 2)
        logger.info("Resposta gerada em {}s com sucesso", tempo_total)

        return {
            "resposta": resposta_texto,
            "tempo_execucao": tempo_total,
        }

    except HTTPException:
        raise
    except Exception:
        logger.exception("Erro não tratado ao processar a pergunta")
        raise HTTPException(
            status_code=500, detail="Erro interno ao processar a consulta RAG."
        )