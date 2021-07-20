import streamlit as st
import streamlit.components.v1 as components
from filometro import update_data, plot_map

_counter = 0
st.set_page_config(layout="wide")
st.title('Mapa Filômetro SP')

@st.cache(suppress_st_warning=True)
def get_data():
    return update_data()

st.write("Localização dos postos de vacinação da Covid-19 na cidade de São Paulo")


if st.button('Atualizar'):
    _counter += 1
st.markdown(
    """
    <style>
    canvas {
    max-width: 100%!important;
    height: auto!important;
    </style>
    """,
    unsafe_allow_html=True)

data = get_data()
map = plot_map(data)
components.html(map._repr_html_(), height=600)