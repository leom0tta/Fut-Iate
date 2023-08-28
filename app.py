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
    
    h2 {text-align: center;}
    </style>
    """, unsafe_allow_html=True)

sheet_id = '12_kJDzA7pdejayJ6Hs7tsxJ7ieaUV4-vQ7coBE1BeEM'
sheet_name = 'Ranking'

url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}'
dados = pd.read_csv(url)

st.markdown(
    "# Fut Iate Rankings :crown: :trophy:"
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
