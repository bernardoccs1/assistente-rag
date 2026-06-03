import os
from dotenv import load_dotenv
load_dotenv()

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

# Caminho onde a DB Chroma foi salva pelo ingest.py
PROCESSED_DATA_DIR = "data/processed/" 

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

def get_infra_assistant_chain():
    # Reconexão com DB vetorial: Instancia o mesmo modelo de embeddings no ingest
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    # Conecta o ChromaDB apontando para a pasta física
    db = Chroma(persist_directory=PROCESSED_DATA_DIR, embedding_function=embeddings)

    # Transforma o DB em um retriever
    # search_kwargs define que serão trazidos os 3 chunks de texto mais semelhantes a pergunta
    retriever = db.as_retriever(search_kwargs={"k": 3})

    # Inicialização da LLM: Modelo de Chat Gemini
    # api_version="v1" garante o uso de rota estável comercial da Google
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash", 
        temperature=0.1,
        api_version="v1"
    )

    # Engenharia de Prompt: Modelo onde pergunta e resposta são estruturados juntos
    # Evita enviar mensagens separadas, contonando bugs de payload do SDK
    prompt_estruturado = (
        "Instrução: Você é um engenheiro de plataforma especialista em AWS, Docker, Git e automações.\n"
        "Use os seguintes trechos de contexto recuperados para responder à pergunta.\n"
        "Se você não souber a resposta ou se o contexto não disser, diga explicitamente que "
        "não tem essa informação na base interna.\n\n"
        "Contexto:\n{context}\n\n"
        "Pergunta do Usuário: {input}\n\n"
        "Resposta:"
    )

    prompt = ChatPromptTemplate.from_template(prompt_estruturado)

    # Construção da Pipeline RAG (LangChain Expression Language - LCEL)
    # context: pega a entrada, passa por retriever e formata para texto
    # response: repassa a pergunta original do usuário adiante no processo
    rag_chain = (
        {
            "context": retriever | format_docs,
            "input": RunnablePassthrough()
        }
        | prompt                # Junta contexto e modelo da pergunta no prompt
        | llm                   # Envia o prompt montado ao Gemini
        | StrOutputParser()     # Converte a resposta bruta do objeto da IA em uma str limpa de texto
    )

    return rag_chain

if __name__ == "__main__":
    chain = get_infra_assistant_chain()

    # pergunta-teste simulando interação de usuário
    pergunta = "Me explique o que é um Docker?"
    print(f"\nPergunta: {pergunta}\n")

    # Dispara execução do fluxo RAG
    response = chain.invoke(pergunta)

    # Exibe o veredito final
    print("Resposta do Assistente:")
    print(response)