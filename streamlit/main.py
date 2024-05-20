import cleaner
import numpy as np
import pandas as pd
import plotly

import streamlit as st


@st.cache_data
def get_bert() -> plotly.graph_objects.Figure:
    with open("resources/tsne_bert_250.json", "r") as bert:
        return plotly.io.from_json(bert.read())


@st.cache_data
def get_spacy() -> plotly.graph_objects.Figure:
    with open("resources/tsne_spacy.json", "r") as spacy:
        return plotly.io.from_json(spacy.read())


with st.sidebar:
    st.title("Hola, Mundo!")

"""
# CodeBERT
CodeBERT es un modelo pre-entrenado de Microsoft especializado para
tareas que involucran embeddings de código
"""
st.plotly_chart(get_bert())

"""
# spaCy
Podemos ver cómo spaCy también logra proveer embeddings que facilitan la
distinción entre los tipos de lenguajes del _dataset_
"""
st.plotly_chart(get_spacy())
