import pytz
import streamlit as st
from datetime import datetime, timedelta
from filometro import update_data, plot_map, add_categorical_legend

brtz = pytz.timezone('America/Sao_Paulo')

st.set_page_config(layout="wide", page_title='Mapa Filometrô SP', page_icon=':syringe:')
st.title('Mapa Filômetro SP')

@st.cache(ttl=300, suppress_st_warning=True, show_spinner=False)
def get_data():
    counter = 0
    data = update_data()
    map_clean, map_leg = plot_map(data)
    brt_time = datetime.now().astimezone(brtz)
    return map_clean, map_leg, brt_time

map_clean, map_leg, update_time = get_data()

st.write("Localização dos postos de vacinação da Covid-19 na cidade de São Paulo")

st.markdown("""Dados extraídos do [Filômetro Vacina Sampa](https://deolhonafila.prefeitura.sp.gov.br/)   
            Código disponível no [Github](http://www.github.com/gabrielmpaula/mapa-filometro-saopaulo/)   
            """)

col1, col2, col3 = st.beta_columns(3)
if col1.button('Atualizar'):
    st.caching.clear_cache()
legend = col2.checkbox('Legenda', value=True)
col3.markdown(f'Última atualização {update_time.strftime("%d-%m-%Y %H:%M:%S")}')

if legend:
    st.markdown(map_leg, unsafe_allow_html=True)
else:
    st.markdown(map_clean, unsafe_allow_html=True)
