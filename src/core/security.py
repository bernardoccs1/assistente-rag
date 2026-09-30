"""Controles de segurança da API e validação de entrada do usuário."""

from __future__ import annotations

import hmac
import os
import re

from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)
MAX_QUESTION_CHARS = int(os.getenv("MAX_QUESTION_CHARS", "4000"))

# A detecção é deliberadamente conservadora: bloquear instruções de override
# explícitas, sem tentar "sanitizar" o texto e alterar a pergunta original.
_INJECTION_PATTERNS = (
    re.compile(
        r"\b(ignore|disregard|forget)\b.{0,80}\b(previous|prior|above|system)\b",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"\b(reveal|show|print|repeat|expose)\b.{0,80}"
        r"\b(system prompt|hidden prompt|instructions?)\b",
        re.IGNORECASE | re.DOTALL,
    ),
    re.compile(
        r"\b(jailbreak|developer mode|dan mode|"
        r"bypass (?:your )?(?:rules|instructions|safety))\b",
        re.IGNORECASE,
    ),
    re.compile(
        r"(?:</?system>|</?developer>|\[INST\]|<<SYS>>)",
        re.IGNORECASE,
    ),
)


def require_api_key(api_key: str | None = Security(API_KEY_HEADER)) -> str:
    """Valida a chave configurada sem revelar qual parte falhou."""
    expected = os.getenv("RAG_API_KEY")
    if not expected:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Autenticação da API não está configurada.",
        )
    if not api_key or not hmac.compare_digest(api_key, expected):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credencial inválida.",
            headers={"WWW-Authenticate": "API key"},
        )
    return api_key


def validate_question(text: str) -> str:
    """Valida texto sem modificar o conteúdo que será enviado ao RAG."""
    normalized = text.strip()
    if not normalized:
        raise HTTPException(status_code=422, detail="A pergunta não pode ser vazia.")
    if len(normalized) > MAX_QUESTION_CHARS:
        raise HTTPException(
            status_code=413,
            detail=f"A pergunta excede o limite de {MAX_QUESTION_CHARS} caracteres.",
        )
    if any(pattern.search(normalized) for pattern in _INJECTION_PATTERNS):
        raise HTTPException(
            status_code=400,
            detail="A pergunta contém um padrão de prompt injection não permitido.",
        )
    return normalized


def contains_prompt_injection(text: str) -> bool:
    """Expõe a decisão para testes sem acoplar testes à implementação das regexes."""
    return any(pattern.search(text) for pattern in _INJECTION_PATTERNS)