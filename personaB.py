import streamlit as st
import pandas as pd
import random
import unicodedata
import re

# Funções utilitárias

@st.cache_data  # Cache para melhorar o desempenho do carregamento dos dados
def load_data(url):
    """Carrega os dados do CSV do Google Sheets."""
    df = pd.read_csv(url)
    # Limpa os nomes das colunas
    df.columns = [normalize_text(col) for col in df.columns]
    # Limpa os dados em cada coluna (exceto 'ID', assumindo que ID é numérico)
    for col in df.columns:
        if col != 'ID':
            df[col] = df[col].astype(str).apply(normalize_text) # Garante que é string antes de normalizar
    return df


def get_random_card(df):
    """Seleciona uma carta aleatória do baralho."""
    return df.sample(n=1).iloc[0]  # Retorna a linha como uma Series

def normalize_text(text):
    """Remove acentos e caracteres especiais."""
    if not isinstance(text, str):
        return text  # Se não for string, retorna sem modificar

    text = str(text)  # Garante que é uma string
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('utf-8')
    text = re.sub(r'[^\w\s-]', '', text).strip()  # Remove pontuações e caracteres especiais (mantém espaços e hífens)
    return text

# Configurações da página Streamlit
st.set_page_config(
    page_title="Pictionary Card Game",
    page_icon=":pencil2:",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
    st.markdown(f"<h4 style='text-align: left;'>Ação: {st.session_state.current_card['Acao']}</h4>", unsafe_allow_html=True) # Corrigi o nome da coluna aqui
    st.markdown(f"<h4 style='text-align: left;'>Dificil: {st.session_state.current_card['Dificil']}</h4>", unsafe_allow_html=True) # Corrigi o nome da coluna aqui
    st.markdown(f"<h4 style='text-align: left;'>Diversos: {st.session_state.current_card['Diversos']}</h4>", unsafe_allow_html=True)


if __name__ == "__main__":
    main()
