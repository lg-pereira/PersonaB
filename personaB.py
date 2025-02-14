import streamlit as st
import pandas as pd
import random
import time  # Para simular o tempo de jogo
import streamlit.components.v1 as components
import numpy as np

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

def start_timer(tempo_segundos, start_sound, end_sound):
    
    # Contagem Regressiva
    countdown_placeholder = st.empty()  # Para atualizar a contagem regressiva
    for i in range(10, 0, -1):
        countdown_placeholder.write(f"Começando em: {i}...")
        time.sleep(1)
    # countdown_placeholder.write("VALENDO!")

    if start_sound:
        audio_start_placeholder = st.empty()
        try:
            # Renderiza o áudio dentro do placeholder
            with audio_start_placeholder:
                st.audio("assets/start.mp3", format="audio/mp3", start_time=0, autoplay=True)
        except:
            st.warning("Não foi possível tocar a buzina de início")

    for i in range(tempo_segundos, -1, -1): #contagem do tempo do jogo
        minutos_restantes = i // 60
        segundos_restantes = i % 60
        countdown_placeholder.write(f"**TIMER: {minutos_restantes:02d}:{segundos_restantes:02d}**")
        time.sleep(1)
        
    if end_sound:
        # Placeholder para o áudio de fim
        audio_end_placeholder = st.empty()
        try:
            # Renderiza o áudio dentro do placeholder
            with audio_end_placeholder:
                st.audio("assets/looser.mp3", format="audio/mp3", start_time=0, autoplay=True)
        except:
            st.warning("Não foi possível tocar a buzina de fim")

def main():
    st.title("Game Persona B 📖")
    
    with st.container():
       
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
    
        # Inicializa a carta na sessão, se não existir
        if 'current_card' not in st.session_state:
            st.session_state.current_card = get_random_card(df)
            
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

    with st.sidebar:
        st.header("Configurações do Jogo")
        # Opção de tempo em segundos (30 a 120)
        tempo_segundos = st.slider("Tempo (segundos)", min_value=15, max_value=120, value=60)

        # Converter segundos em minutos e segundos para exibição
        minutos = tempo_segundos // 60
        segundos = tempo_segundos % 60

        st.write(f"Tempo selecionado: {minutos:02d}:{segundos:02d}")

        play_start_sound = st.checkbox("Tocar som para iniciar", value="True")
        play_end_sound = st.checkbox("Som de fim do tempo", value="True")
        
        st.title("Instruções do Jogo")
        st.write("Cclique _primeiro em **STOP** e depois **START**_ para iniciar o game.  \n Ao clicar **START** será iniciado um timer de 10s para preparação e depois um timer com o tempo escolhido aqui nas opções.")
        st.write("Clique em **STOP** para parar o tempo, _**STOP** novamente para devolver a carta_ e depois em **START** para uma nova carta.")
        st.write("Cada carta tem 5 categorias:  \n [P]essoa ou animal  \n [L]ugar ou objeto  \n [A]ção  \n [D]ifícil  \n [M]ix")
        st.write("  \n Divirta-se desenhando ou fazendo mímicas com seus amigos!")

    col1, col2, col3 = st.columns([1,2,1])  

    with col1:
        with st.container():
            if st.button("START"):
                start_timer(tempo_segundos, play_start_sound, play_end_sound)    
    
    with col2:
        with st.container():   # Botão para gerar uma nova carta
            if st.button("STOP"):
               handle_card_action()
    


if __name__ == "__main__":
    main()
