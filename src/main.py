import streamlit as st
import streamlit.components.v1 as components
from filometro import update_data, plot_map, add_categorical_legend

_counter = 0
st.set_page_config(layout="wide", page_title='Mapa Filometrô SP', page_icon=':syringe:')
st.title('Mapa Filômetro SP')

@st.cache(suppress_st_warning=True)
def get_data():
    return update_data()

st.write("Localização dos postos de vacinação da Covid-19 na cidade de São Paulo")

col1, col2 = st.beta_columns(2)
container = st.beta_container()
if col1.button('Atualizar'):
    _counter += 1
legend = col2.checkbox('Legenda', value=True)

data = get_data()
map = plot_map(data, legend)

container.markdown(map._repr_html_(), unsafe_allow_html=True)
st.markdown("""Dados extraídos do [Filômetro Vacina Sampa](https://deolhonafila.prefeitura.sp.gov.br/)   
            Código disponível em: [Github](http://www.github.com/gabrielmpaula/mapa-filometro-saopaulo/)""")