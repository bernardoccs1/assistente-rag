import streamlit as st
import warnings
import requests

# Silencia avisos de depreciação irritantes de bibliotecas externas
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")
warnings.filterwarnings("ignore", category=DeprecationWarning)

st.set_page_config(page_title= "RAG ASSIST", layout= "centered")

st.title=("RAG Docker Assist")

# Verifica se "messages" existe, se não existir, cria uma lista vazia
if "messages" not in st.session_state:
    st.session_state.messages= []

# Mostra mensagens do histórico das conversas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        # Cria a bolha visual do user.
        st.markdown(message["content"])

# Responde ao input do user
if prompt:= st.chat_input("Ask your Docker related question."):
    with st.chat_message("user"):
        st.markdown(prompt)
    # Salva a pergunta do usuário no histórico
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Cria a bolha visual do assistente que vai segurar a resposta da API
    with st.chat_message("assistant"):
        with st.spinner("Preparando sua resposta..."):
            try:
                API_url= "http://api:8000/perguntar"
                payload= {"texto": prompt}
                # Faz a chamada HTTP POST para o container da API FastAPI
                response= requests.post(API_url, json= payload)

                if response.status_code == 200:
                    resultado=response.json()
                    # Extrai o texto gerado pelo Gemini no backend
                    texto_resposta= resultado.get("texto", "Erro ao recuperar chave 'texto'.")
                    # Exibe o texto na tela dentro da bolha do assistente
                    st.markdown(texto_resposta)
                    # Salva a resposta da IA na memória do Streamlit
                    st.session_state.messages.append({"role": "assistant", "content": texto_resposta})
 
                else:
                    st.error("Erro no servidor: Código {response.status_code}")
                    st.write(response.text)

            except requests.exceptions.ConnectionError:
                st.error("Não foi possível se conectar ao backend")
            except requests.exceptions.Timeout:
                st.error("A requisição demorou mais que o esperado (Timeout)")
    