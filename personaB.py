import streamlit as st
import pandas as pd
import random
import streamlit.components.v1 as components

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

# CSS para estilizar o card
card_style = """
<style>
.card-container {
    perspective: 1000px;
    width: 300px; /* Ajuste o tamanho conforme necessário */
    height: 400px; /* Ajuste o tamanho conforme necessário */
    margin: 20px auto;
}

.card {
    position: relative;
    width: 100%;
    height: 100%;
    transition: transform 0.8s;
    transform-style: preserve-3d;
}

.card.flipped {
    transform: rotateY(180deg);
}

.card-face {
    position: absolute;
    width: 100%;
    height: 100%;
    backface-visibility: hidden;
    display: flex;
    flex-direction: column;
    justify-content: flex-start; /* Alinha ao topo */
    align-items: center;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    background-color: #f9f9f9;
}

.card-front {
    background-color: #f9f9f9; /* Cor de fundo da frente */
    color: #333;
}

.card-back {
    background-color: #e9e9e9; /* Cor de fundo do verso */
    color: #333;
    transform: rotateY(180deg);
}

.card-id {
    border: 2px solid silver;
    padding: 5px 10px;
    border-radius: 5px;
    margin-bottom: 10px;
    background-color: white;
}

.card-options {
    list-style: none;
    padding: 0;
    margin: 0;
    width: 100%;
}

.card-options li {
    padding: 8px 12px;
    margin-bottom: 5px;
    border-radius: 5px;
    background-color: #fff;
    border: 1px solid #ddd;
    text-align: left;
    width: 100%;
    box-sizing: border-box;
}

/* Adicione um estilo para o botão */
.stButton>button {
    background-color: #4CAF50; /* Verde */
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
}
</style>
"""

# Main App
def main():
    st.title("Pictionary Card Game")

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

    # Estado para controlar a animação de virada
    if 'flipped' not in st.session_state:
        st.session_state.flipped = False

    # Botão para gerar uma nova carta
    if st.button("Gerar Nova Carta"):
        st.session_state.current_card = get_random_card(df)
        st.session_state.flipped = not st.session_state.flipped  # Inverte o estado para animar

    # Inicializa a carta na sessão, se não existir
    if 'current_card' not in st.session_state:
        st.session_state.current_card = get_random_card(df)

    # Exibe o CSS
    st.markdown(card_style, unsafe_allow_html=True)

    # Exibe o card
    card_html = f"""
    <div class="card-container">
        <div class="card {'flipped' if st.session_state.flipped else ''}">
            <div class="card-face card-front">
                <div class="card-id">ID: {st.session_state.current_card['ID']}</div>
                <h2>Pictionary!</h2>
            </div>
            <div class="card-face card-back">
                <div class="card-id">ID: {st.session_state.current_card['ID']}</div>
                <ul class="card-options">
                    <li>Pessoa ou Animal: {st.session_state.current_card['Person or Animal']}</li>
                    <li>Lugar ou Objeto: {st.session_state.current_card['Place or object']}</li>
                    <li>Ação: {st.session_state.current_card['Action']}</li>
                    <li>Difícil: {st.session_state.current_card['Hard']}</li>
                    <li>Diversos: {st.session_state.current_card['Mix']}</li>
                </ul>
            </div>
        </div>
    </div>
    """

    st.markdown(card_html, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
