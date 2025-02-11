import streamlit as st
import pandas as pd
import random

# Configurações da página Streamlit
st.set_page_config(
    page_title="Pictionary Card Game",
    page_icon=":pencil2:",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Funções utilitárias

@st.cache_data  # Cache para melhorar o desempenho do carregamento dos dados
def load_data(url):
    """Carrega os dados do CSV do Google Sheets."""
    df = pd.read_csv(url)
    return df

def get_random_card(df):
    """Seleciona uma carta aleatória do baralho."""
    return df.sample(n=1).iloc[0]  # Retorna a linha como uma Series


# Main App
def main():
    st.title("Pictionary Card Game")

    # URL do Google Sheets CSV
    csv_url = "https://docs.google.com/spreadsheets/d/1_9Sy_1nAVku52AeKUIDvjvJHMxFInMyGYWjM1Jw4jso/export?format=csv"

    # Carrega os dados
    try:
        df = load_data(csv_url)
        st.success("Dados carregados com sucesso!")
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return  # Aborta a execução se não conseguir carregar os dados

    # Botão para gerar uma nova carta
    if st.button("Gerar Nova Carta"):
        st.session_state.current_card = get_random_card(df)

    # Inicializa a carta na sessão, se não existir
    if 'current_card' not in st.session_state:
        st.session_state.current_card = get_random_card(df)


    # Exibe a carta
    st.header("Carta para Desenhar")
    st.subheader(f"ID: {st.session_state.current_card['ID']}")
    st.markdown(f"<h4 style='text-align: left;'>Pessoa ou Animal: {st.session_state.current_card['Pessoa ou animal']}</h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: left;'>Lugar ou Objeto: {st.session_state.current_card['Lugar ou objeto']}</h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: left;'>Ação: {st.session_state.current_card['Ação']}</h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: left;'>Difícil: {st.session_state.current_card['Difícil']}</h4>", unsafe_allow_html=True)
    st.markdown(f"<h4 style='text-align: left;'>Diversos: {st.session_state.current_card['Diversos']}</h4>", unsafe_allow_html=True)



if __name__ == "__main__":
    main()
