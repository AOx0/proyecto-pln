import streamlit as st

@st.cache_data
def setup() -> int:
    return 0

setup()

st.title("Hola, Mundo!")
