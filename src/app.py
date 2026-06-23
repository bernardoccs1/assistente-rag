import streamlit as st
import warnings
import requests

# Silencia avisos de depreciação irritantes de bibliotecas externas
warnings.filterwarnings("ignore", category=UserWarning, module="transformers")
warnings.filterwarnings("ignore", category=DeprecationWarning)

st.set_page_config(page_title= "RAG ASSIST", layout= "centered")

st.title=("RAG Docker Assist")
st.write("Ask any Docker related question")

prompt= st.text_input("Use this workspace to ask your Docker questions")
api_button= st.button("Send question")

st.divider()

API_url= "http://api:8000/perguntar"

if prompt and api_button:
    with st.spinner("Documentos sendo processados: "):
        try:
            payload= {"texto": prompt}

            response= requests.post(API_url, json= payload)

            if response.status_code == 200:
                resultado= response.json()

                st.subheader("Assist: ")
                st.markdown(resultado.get("texto", "Erro ao recuperar chave 'texto'."))
            
            else:
                st.error("Erro no servidor: Código {response.status_code}")
                st.write(response.text)

        except requests.exceptions.ConnectionError:
            st.error("Não foi possível se conectar ao backend")