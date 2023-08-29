import pandas as pd
import streamlit as st


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
    
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size:24px;
        text-align: center;
        place-items: center;

    }
    
    .css-3mmywe.e15ugz7a0 {
        
        place-items: center;
        align-content: center;
        
    }
    
    tr {
        
        font-size: 16px;
        color: white;
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

def head2head(dados, person1, person2, metrica):
    
    person1_db = dados[dados['NOME'] == person1]
    person2_db = dados[dados['NOME'] == person2]
    
    if (person2_db[metrica].sum() < person1_db[metrica].sum()):
        st.markdown(f"**{metrica.title()}: {person1.title()} leva: {person1_db[metrica].sum()} :crown:**")

    elif (person2_db[metrica].sum() > person1_db[metrica].sum()):
        st.markdown(f"**{metrica.title()}: {person2.title()} leva: {person2_db[metrica].sum()} :crown:**")

    elif (person2_db[metrica].sum() == person1_db[metrica].sum()):
        st.markdown(f"**{metrica.title()}: EMPATE**")

def RankingTotal (dados):
    
    result = dados.groupby('NOME').apply(lambda x: x.GOLS.sum()*0.5 + x.PRESENÇA.sum()*0.1 + x.ASSISTÊNCIAS.sum()*0.4).sort_values(ascending=False)
    
    result = result.to_frame().reset_index()
    
    result.columns = ['Nome', 'Score']
    
    def format_score(score):
        return f"{score:.2f}"

    result['Posição'] = result.index + 1
    
    st.title("All Time Ranking")
    
    view = result.style.hide(axis="index")
    
    view.set_table_styles([
    {'selector': "th", 'props': [("font-weight", "bold"), ("text-transform", "capitalize")]},])
    
    view.format(lambda x: f"<i title='tooltip'>{x}</i>", 'Posição')
    
    cols1, cols2 = st.columns(2)
    
    with cols1:
        st.markdown(view.to_html(), unsafe_allow_html=True)
    with cols2:
        st.write("Os pesos usados foram, 50% por Gol;  10% por presença e 40% por Assistência")
    
    
    return()

RankingTotal(dados)

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
            head2head(dados, person1, person2, 'MVP')
