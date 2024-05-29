import pandas as pd
import plotly

import streamlit as st


@st.cache_data
def get_unigrams() -> plotly.graph_objects.Figure:
    with open("resources/unigrams_words.json", "r") as fig:
        return plotly.io.from_json(fig.read())

@st.cache_data
def get_bigrams() -> plotly.graph_objects.Figure:
    with open("resources/bigrams_words.json", "r") as fig:
        return plotly.io.from_json(fig.read())

@st.cache_data
def get_trigrams() -> plotly.graph_objects.Figure:
    with open("resources/trigrams_words.json", "r") as fig:
        return plotly.io.from_json(fig.read())

# @st.cache_data
# def get_image() -> plotly.graph_objects.Figure:
#     with open("resources/trigrams_words.json", "r") as fig:
#         return plotly.io.from_json(fig.read())


"""
# N-Grams
"""
st.image("resources/mapas.png")
st.plotly_chart(get_unigrams())
st.plotly_chart(get_bigrams())
st.plotly_chart(get_trigrams())
