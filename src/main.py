import streamlit as st
import streamlit.components.v1 as components
from filometro import update_data, plot_map


counter = 0
st.set_page_config(layout="wide")

@st.cache(suppress_st_warning=True)
def get_data():
    return update_data()

st.write("Localização dos postos de vacinação da Covid-19 na cidade de São Paulo")

data = get_data()
map = plot_map(data)
components.html(map._repr_html_(), height=700)

if st.button('Atualizar'):
    counter += 1

# create_map(data, -23.80128, -46.658112, 10)
