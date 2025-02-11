import streamlit as st
import pandas as pd
import random
import time  # Para simular o tempo de jogo
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

# Start App
def start():
    st.title("Persona B Card Game")

    # URL do Google Sheets CSV
    url = "https://docs.google.com/spreadsheets/d/1_9Sy_1nAVku52AeKUIDvjvJHMxFInMyGYWjM1Jw4jso"
    csv_url = url+"/export?format=csv"

    # Carrega os dados
    try:
        df = load_data(csv_url)
        # st.success("Dados carregados com sucesso!")
    except Exception as e:
        st.error(f"Erro ao carregar os dados: {e}")
        return  # Aborta a execução se não conseguir carregar os dados

    # Estado para controlar a animação de virada
    if 'flipped' not in st.session_state:
        st.session_state.flipped = False

    # Função para verificar o estado da carta
    def handle_card_action():
        if st.session_state.flipped:
            # Já está virado, então apenas desvira
            st.session_state.flipped = False
        else:
            # Se a carta não estiver virada, gera uma nova carta e vira
            st.session_state.current_card = get_random_card(df)
            st.session_state.flipped = True


    # Botão para gerar uma nova carta
    if st.button("Próximo jogador"):
       handle_card_action()


    # Inicializa a carta na sessão, se não existir
    if 'current_card' not in st.session_state:
        st.session_state.current_card = get_random_card(df)

    # CSS para estilizar o card
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
        display: flex; /* Alterado para flex */
        justify-content: center; /* Centraliza horizontalmente */
        align-items: center;    /* Centraliza verticalmente */
        font-size: 1.5em;       /* Aumenta o tamanho da fonte */
    }
    
    .card-back {
        background-color: #e9e9e9; /* Cor de fundo do verso */
        color: #7C8D9E;
        text-align: center;
        transform: rotateY(180deg);
        display: flex; /* Alterado para flex */
        flex-direction: row;
        flex-wrap: wrap;
        justify-content: center;
        align-items: center;
        padding: 10px;
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
        font-size: 1.2em;          /* Aumentado o tamanho da fonte */
        display: inline-block;    /* Para espalhar horizontalmente */
        margin: 5px;
    }
    
    /* Adicione um estilo para o botão */
    .stButton>button {
        background-color: #5D6770;
        border: 3px solid #7C8D9E;
        color: white;
        padding: 15px 32px;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        font-size: 100%;
        margin: 4px 2px;
        cursor: pointer;
        border-radius: 15px;
    }
    </style>
    """
    
    # Exibe o CSS
    st.markdown(card_style, unsafe_allow_html=True)

    # Exibe o card
    card_html = f"""
    <div class="card-container">
        <div class="card {'flipped' if st.session_state.flipped else ''}">
            <div class="card-face card-front">
                <h2>PERSONA B</h2>
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

def main():
    st.title("Menu Game Card")

    # Opções do menu
    num_equipes = st.slider("Número de Equipes", min_value=1, max_value=10, value=2)
    tempo_jogo = st.number_input("Tempo (minutos)", min_value=1, max_value=60, value=10)

    # Botão Iniciar
    if st.button("Iniciar"):
        st.write(f"Jogo iniciado com {num_equipes} equipes e tempo de {tempo_jogo} minutos!")
        # Simulação do jogo (substitua com a lógica real do seu jogo)
        with st.empty():  # Cria um espaço vazio para atualizações
            for i in range(tempo_jogo * 60):  # Simula segundos
                time.sleep(1)  # Pausa de 1 segundo
                tempo_restante = tempo_jogo * 60 - i
                minutos = tempo_restante // 60
                segundos = tempo_restante % 60
                st.write(f"Tempo restante: {minutos:02d}:{segundos:02d}")
        st.success("Fim do jogo!")


if __name__ == "__main__":
    main()
