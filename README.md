# Assistente RAG - Pipeline de Busca Semântica & LLM

![Python](https://img.shields.io/badge/Python-3.11-blue?logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-009688?logo=fastapi)
![LangChain](https://img.shields.io/badge/LangChain-Enabled-1C3C3C)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?logo=docker)
![CI/CD](https://img.shields.io/badge/CI%2FCD-GitHub_Actions-2088FF?logo=githubactions)

Aplicação backend desenvolvida em *Python (FastAPI)* que implementa uma arquitetura *RAG (Retrieval-Augmented Generation)*. O sistema realiza ingestão e processamento de documentos (PDFs/TXTs), gera embeddings vetoriais, realiza busca por similaridade semântica utilizando *ChromaDB* e orquestra a geração de respostas contextuais integrando a *API do Google Gemini* via *LangChain*.

---

## Arquitetura do Sistema

[ Documento PDF/TXT ] ──> [ Text Splitter ] ──> [ Google Embeddings ]
                                                        │
                                                        ▼
[ Usuário / Prompt ] ──> [ FastAPI ] ──> [ ChromaDB (Vector Store) ]
                               │                        │
                               │ (Contexto Relevante)   │
                               ▼                        │
                      [ Google Gemini API ] <───────────┘
                               │
                               ▼
                    [ Resposta Fundamentada ]

  Tecnologias Utilizadas
Linguagem & Framework API: Python 3.11 / FastAPI / Uvicorn

Orquestração de IA & LLM: LangChain / Google Gemini API

Vector Database: ChromaDB (Persistência e Busca Vetorial)

Conteinerização & Ambiente: Docker / Docker Compose

Qualidade & CI/CD: Pytest / Ruff / GitHub Actions

  Como Executar o Projeto
Pré-requisitos:
Docker e Docker Compose instalados.

Uma chave de API do Google Gemini (GOOGLE_API_KEY).

1. Clonar o repositório
Bash
git clone [https://github.com/bernardoccs1/assistente-rag.git](https://github.com/bernardoccs1/assistente-rag.git)
cd assistente-rag
2. Configurar Variáveis de Ambiente
Crie um arquivo .env na raiz do projeto com base no modelo:

Snippet de código
GOOGLE_API_KEY=sua_chave_api_aqui
3. Rodar via Docker Compose
Bash
docker-compose up --build -d
A API estará acessível em: http://localhost:8000

Documentação interativa Swagger: http://localhost:8000/docs

  Testes e CI/CD
O projeto conta com uma esteira automatizada de CI/CD via GitHub Actions (.github/workflows/ci.yml), garantindo:

Análise estática de código e linting com Ruff.

Execução de testes unitários e de integração com Pytest.

Validação do build do container Docker.

Para rodar os testes localmente:

Bash
pytest
   Próximos Passos (Roadmap de MLOps & Infra)
[ ] Implementar tracing e observabilidade de LLMs utilizando LangSmith / Arize Phoenix.

[ ] Criar etapa de avaliação automatizada da qualidade do RAG (métricas de faithfulness e relevance).

[ ] Provisionar infraestrutura na nuvem (AWS/GCP) via Terraform (IaC).

Desenvolvido por Bernardo Silveira.
