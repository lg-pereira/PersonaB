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
    color: #7EA1C5;
    text-align: center;
    display: inline-block; /* Para espalhar horizontalmente */
}

.card-back {
    background-color: #e9e9e9; /* Cor de fundo do verso */
    color: #7C8D9E;
    text-align: center;
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
    border: 3px solid #ddd;
    text-align: left;
    width: 90%;
    box-sizing: border-box;
    font-size: 100%;   /* Adicionado tamanho da fonte */
    display: inline-block; /* Para espalhar horizontalmente */
    margin: 5px;         /* Adicionado margem */
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

    # Exibe o CSS
    st.markdown(card_style, unsafe_allow_html=True)

    # Exibe o card
    card_html = f"""
    <div class="card-container">
        <div class="card {'flipped' if st.session_state.flipped else ''}">
            <div class="card-face card-front">
                <h2>PERSONA B <br>IMAGEM E AÇÃO<br>COM TEMAS BÍBLICOS!</h2>
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
