import streamlit as st
from datetime import datetime
from filometro import update_data, plot_map, add_categorical_legend


st.set_page_config(layout="wide", page_title='Mapa Filometrô SP', page_icon=':syringe:')
st.title('Mapa Filômetro SP')
_counter = 0
@st.cache(suppress_st_warning=True)
def get_data(_counter):
    data = update_data()
    map_clean, map_leg = plot_map(data)
    return map_clean, map_leg, datetime.now().date

map_clean, map_leg, update_time = get_data(_counter)

st.write("Localização dos postos de vacinação da Covid-19 na cidade de São Paulo")

st.markdown("""Dados extraídos do [Filômetro Vacina Sampa](https://deolhonafila.prefeitura.sp.gov.br/)   
            Código disponível no [Github](http://www.github.com/gabrielmpaula/mapa-filometro-saopaulo/)   
            """)

col1, col2 = st.beta_columns(2)
if col1.button('Atualizar'):
    _counter += 1
legend = col2.checkbox('Legenda', value=True)

if legend:
    st.markdown(map_leg, unsafe_allow_html=True)
else:
    st.markdown(map_clean, unsafe_allow_html=True)

st.markdown(f'Última atualização {update_time.strftime("%d-%m-%Y")}')
