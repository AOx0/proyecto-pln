import cleaner
import numpy as np
import pandas as pd
import plotly

import streamlit as st


@st.cache_data
def get_bert() -> plotly.graph_objects.Figure:
    with open("resources/tsne_bert.json", "r") as bert:
        return plotly.io.from_json(bert.read())


@st.cache_data
def get_spacy_clean() -> plotly.graph_objects.Figure:
    with open("resources/tsne_spacy_clean.json", "r") as spacy:
        return plotly.io.from_json(spacy.read())

@st.cache_data
def get_tfidf_clean() -> plotly.graph_objects.Figure:
    with open("resources/tsne_tfidf_clean.json", "r") as tfidf:
        return plotly.io.from_json(tfidf.read())


# with st.sidebar:
    # st.title("Hola, Mundo!")

"""
# CodeBERT
CodeBERT es un modelo pre-entrenado de Microsoft especializado para
tareas que involucran embeddings de código
"""
st.plotly_chart(get_bert())

"""
# TF-IDF
"""
st.plotly_chart(get_tfidf_clean())

"""
# spaCy
"""
st.plotly_chart(get_spacy_clean())
