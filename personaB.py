import streamlit as st
import pandas as pd
import random
import streamlit.components.v1 as components

# Configurações da página Streamlit
st.set_page_config(
    page_title="Persona B Mimic Game",
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
    st.title("Persona B Card Game")

    # URL do Google Sheets CSV
    url = "https://docs.google.com/spreadsheets/d/1_9Sy_1nAVku52AeKUIDvjvJHMxFInMyGYWjM1Jw4jso"
    csv_url = url+"/export?format=csv"

    # Carrega os dados
    try:
        df = load_data(csv_url)
        st.success("Dados carregados com sucesso!")
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return  # Aborta a execução se não conseguir carregar os dados

    # Slider para controlar o tamanho da fonte
    font_size = st.sidebar.slider("Tamanho da Fonte:", min_value=0.8, max_value=2.0, value=1.2, step=0.1)

    # Estado para controlar a animação de virada
    if 'flipped' not in st.session_state:
        st.session_state.flipped = False

    # Botão para gerar uma nova carta
    if st.button("Próxima carta"):
        st.session_state.current_card = get_random_card(df)
        st.session_state.flipped = not st.session_state.flipped  # Inverte o estado para animar

    # Inicializa a carta na sessão, se não existir
    if 'current_card' not in st.session_state:
        st.session_state.current_card = get_random_card(df)

    # CSS para estilizar o card
    card_style = f"""
    <style>
    .card-container {{
        perspective: 1000px;
        width: 300px;
        height: 400px;
        margin: 20px auto;
    }}

    .card {{
        position: relative;
        width: 100%;
        height: 100%;
        transition: transform 0.8s;
        transform-style: preserve-3d;
    }}

    .card.flipped {{
        transform: rotateY(180deg);
    }}

    .card-face {{
        position: absolute;
        width: 100%;
        height: 100%;
        backface-visibility: hidden;
        display: flex;
        flex-direction: column;
        justify-content: flex-start;
        align-items: center;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        background-color: #f9f9f9;
    }}

    .card-front {{
        background-color: #f9f9f9;
        color: #333;
    }}

    .card-back {{
        background-color: #e9e9e9;
        color: #333;
        transform: rotateY(180deg);
        display: flex;
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        padding: 10px;
    }}

    .card-id {{
        border: 2px solid silver;
        padding: 5px 10px;
        border-radius: 5px;
        margin-bottom: 10px;
        background-color: white;
    }}

    .card-options {{
        list-style: none;
        padding: 0;
        margin: 0;
        width: 100%;
        text-align: center;
    }}

    .card-options li {{
        padding: 8px 12px;
        margin-bottom: 5px;
        border-radius: 5px;
        background-color: #fff;
        border: 1px solid #ddd;
        text-align: center;
        width: auto;
        box-sizing: border-box;
        font-size: {font_size}em; /* Tamanho da fonte dinâmico */
        display: inline-block;
        margin: 5px;
        overflow-wrap: break-word;
        word-break: break-all;
        max-width: 150px;
    }}

    .stButton>button {{
        background-color: #4CAF50;
        border: none;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 16px;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 12px;
    }}
    </style>
    """

    # Exibe o CSS
    st.markdown(card_style, unsafe_allow_html=True)

    # Exibe o card
    card_html = f"""
    <div class="card-container">
        <div class="card {{'flipped' if st.session_state.flipped else ''}}">
            <div class="card-face card-front">
                <h2>PERSONA B <br>seu imagem e ação<br>com temas bíblicos!</h2>
            </div>
            <div class="card-face card-back">
                <div class="card-id">{st.session_state.current_card['ID']}</div>
                <ul class="card-options">
                    <li>P: {st.session_state.current_card['Person or Animal']}</li>
                    <li>L: {st.session_state.current_card['Place or object']}</li>
                    <li>A: {st.session_state.current_card['Action']}</li>
                    <li>D: {st.session_state.current_card['Hard']}</li>
                    <li>M: {st.session_state.current_card['Mix']}</li>
                </ul>
            </div>
        </div>
    </div>
    """

    st.markdown(card_html, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
