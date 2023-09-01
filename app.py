import pandas as pd
import streamlit as st
import datetime
import locale

# Set the locale to Portuguese (Brazil)
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')  # Use 'pt_PT.UTF-8' for Portuguese (Portugal)



st.set_page_config(
    layout="wide",
    page_title = 'Fut Iate',
    page_icon='https://www.icrj.com.br/iate/images/logo/logo60.png')
    
st.markdown("""
    <style>
    p {
        font-size:20px;
        place-items: center;

    }
    
    .st-af {
        font-size: 19px;
    }
    
    .css-10trblm.eqr7zpz0 {
        
        font-size:25px;
    }
    
    code {
        color: rgb(9, 171, 59);
        overflow-wrap: break-word;
        font-size: 20px;
    }   
    
    .stMarkdown {
    display: grid;
    place-items: center;
    }
    
    button{
        display: grid;
        place-items: center;
        
    }
    
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] {
        font-size:24px;
        text-align: center;
        place-items: center;

    }
    
    .css-q8sbsg.eqr7zpz4 {
        
        font-size:24px;
        text-align: center;
        place-items: center;
        
    }
    
    .css-10trblm.eqr7zpz0 {
        
        font-size:40px;
        text-align: center;
        place-items: center;
        
    }
    
    .css-3mmywe.e15ugz7a0 {
        
        place-items: center;
        align-content: center;
        
    }
    
    h2 {text-align: center;}
    </style>
    """, unsafe_allow_html=True)

sheet_id = '12_kJDzA7pdejayJ6Hs7tsxJ7ieaUV4-vQ7coBE1BeEM'
sheet_name = 'Ranking'

url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
dados = pd.read_csv(url)

st.markdown(
    "# Fut Iate :crown: :trophy:"
)

def stable_matching(ranking):
    team_size = 5
    players = ranking['Nome'].tolist()
    scores = ranking['Score'].tolist()
    
    n = len(players)
    proposals = [-1] * n
    engaged = [-1] * n
    preferences = {players[i]: [(scores[i], i) for i in range(n)] for i in range(n)}
    
    while -1 in engaged:
        free_player = engaged.index(-1)
        for _, preferred_player_idx in preferences[players[free_player]]:
            if proposals[preferred_player_idx] == -1:
                engaged[free_player] = preferred_player_idx
                proposals[preferred_player_idx] = free_player
                break
            else:
                current_partner_idx = proposals[preferred_player_idx]
                if preferences[players[preferred_player_idx]].index((scores[free_player], free_player)) < preferences[players[preferred_player_idx]].index((scores[current_partner_idx], current_partner_idx)):
                    engaged[free_player] = preferred_player_idx
                    proposals[preferred_player_idx] = free_player
                    engaged[current_partner_idx] = -1
                    break
            
    teams = []
    substitutes = []
    
    for i in range(0, n, team_size):
        
        team_players = players[i:i+team_size]
        
        if len(team_players) < team_size:
            substitutes.extend(team_players)
        else:
            teams.append(team_players)
    
    st.markdown(f"**Time 1: {' | '.join(teams[0])}**")
    st.markdown(f"**Time 2: {' | '.join(teams[1])}**")
    st.markdown(f"**Substitutos: {' | '.join(substitutes)}**")
    return teams, substitutes
    
import random

def form_random_teams_with_substitutes(ranking):
    
    team_size = 5
    players = ranking['Nome'].tolist()
    
    random.shuffle(players)  # Shuffle the list of players randomly
    num_teams = len(players) // team_size
    teams = [players[i:i+team_size] for i in range(0, len(players), team_size)]
    substitutes = players[num_teams * team_size:]  # Any remaining players are substitutes

    st.markdown(f"**Time 1: {' | '.join(teams[0])}**")
    st.markdown(f"**Time 2: {' | '.join(teams[1])}**")
    st.markdown(f"**Substitutos: {' | '.join(substitutes)}**")

    return teams, substitutes

def head2head(dados, person1, person2, metrica):
    
    person1_db = dados[dados['NOME'] == person1]
    person2_db = dados[dados['NOME'] == person2]
    
    person2_ratio = person2_db[metrica].sum()/person2_db.PRESENÇA.sum()
    person1_ratio = person1_db[metrica].sum()/person2_db.PRESENÇA.sum()

    if (person2_ratio < person1_ratio):
        st.markdown(f"**{metrica.title()}:\n {person1.title()} | {person1_db[metrica].sum()} {metrica} em {person1_db['PRESENÇA'].sum()} jogo(s) :crown:**")

    elif (person2_ratio > person1_ratio):
        st.markdown(f"**{metrica.title()}:\n {person2.title()} | {person2_db[metrica].sum()} {metrica} em {person2_db['PRESENÇA'].sum()} jogo(s) :crown:**")

    elif (person2_ratio == person1_ratio):
        st.markdown(f"**{metrica.title()}:\n EMPATE**")

def RankingTotal (dados, pesoGols, pesoAssists, pesoPresença):
    
    
    if(pesoGols + pesoAssists + pesoPresença != 1):
        st.error('Pesos não somam 1')
    else:
        
        result = dados.groupby('NOME').apply(lambda x: (x.GOLS.sum()/x.PRESENÇA.sum())*pesoGols + x.PRESENÇA.sum()*pesoPresença + (x.ASSISTÊNCIAS.sum()/x.PRESENÇA.sum())*pesoAssists).sort_values(ascending=False)
        
        result = result.to_frame().reset_index()
        
        result.columns = ['NOME', 'Score']
        
        result = pd.merge(dados.groupby('NOME').sum(['GOLS', 'ASSISTÊNCIAS', 'PRESENÇA']), result, on='NOME')

        def format_score(score):
            return f"{score:.2f}"

        result.sort_values('Score', inplace=True, ascending=False)
        result.reset_index(inplace = True, drop=True)
        result['Posição'] = result.index + 1
        result = result[['NOME', 'GOLS', 'ASSISTÊNCIAS', 'PRESENÇA', 'Score', 'Posição']]
        
        result.columns = ['Nome', 'Gols', 'Assistências', 'Presença','Score', 'Posição']
        result['Score'] = result['Score'].apply(lambda x: round(x, 2))  
        view = result.style.hide(axis="index")
        
        view.set_table_styles([
        {'selector': "th", 'props': [("font-weight", "bold"), ("text-transform", "capitalize")]},])
        
        view.format(lambda x: f"<i title='tooltip'>{x}</i>", 'Posição')
            
        st.markdown(view.to_html(), unsafe_allow_html=True)
        return(result)
tab1, tab2 = st.tabs(['# Ranking All-Time', "# Ranking Mensal"])

with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
        pesoGols = st.number_input('Peso de Gols', min_value=0.,max_value=1., value = 0.4)
    with col2:
        pesoAssistências = st.number_input('Peso de Assistências', min_value=0.,max_value=1.,value = 0.3)
    with col3:
        pesoPresença = st.number_input('Peso de Presença', min_value=0.,max_value=1.,value = 0.3)
        
    ranking = RankingTotal(dados,pesoGols,pesoAssistências,pesoPresença)

with tab2:

    dateRef = st.date_input('Data de Referência', pd.to_datetime(dados['DATA']).unique()[-1])
    
    dt = dados[dados['DATA'].apply(lambda x: pd.to_datetime(x).month) == dateRef.month]
    
    st.write('Mês de Referência: ', dateRef.strftime('%m-%Y').title())
    
    col1, col2, col3 = st.columns(3)
    with col1:
        pesoGols1 = st.number_input('Peso de Gols - mensal', min_value=0.,max_value=1., value = 0.4)
    with col2:
        pesoAssistências2 = st.number_input('Peso de Assistências - mensal', min_value=0.,max_value=1.,value = 0.3)
    with col3:
        pesoPresença3 = st.number_input('Peso de Presença - mensal', min_value=0.,max_value=1.,value = 0.3)
    
    if (dt.empty):
        st.error('Ainda não tiveram partidas esse Mês')
    else:
        ranking = RankingTotal(dt,pesoGols1,pesoAssistências2,pesoPresença3)
    
with st.sidebar:
    with st.expander("# Head-To-Head"):
        st.markdown("## Head-to-head :rage:")
        with st.form(key="head2head"):
            person1 = st.selectbox("Player 1: ", dados['NOME'].unique())
            person2 = st.selectbox("Player 2: ", [el for el in dados['NOME'].unique() if el != person1])
            submit_head2head = st.form_submit_button(label="Submit")
            
            if(submit_head2head):
                head2head(dados, person1, person2, 'GOLS')
                head2head(dados, person1, person2, 'PRESENÇA')
                head2head(dados, person1, person2, 'ASSISTÊNCIAS')
                
    with st.expander('# Seletor de Times'):
        st.markdown("## Usando Stable Matching de Gale-Shapley :computer:")
        with st.form(key="Gale-Shapley"):
            submit_stable = st.form_submit_button(label="Bater Time")
            if(submit_stable):
                stable_matching(ranking)
            
        st.markdown("## Random Selector :1234:")
        with st.form(key="Random"):

            submit_random = st.form_submit_button(label="Time Random")
            if(submit_random):
                
                form_random_teams_with_substitutes(ranking)
